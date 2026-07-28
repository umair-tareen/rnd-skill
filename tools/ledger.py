"""ledger.py -- deterministic bookkeeping for a /rnd thesis file.

Spec: SPEC.md at the repo root (SS I.1 schema).
Format: ai-codex FORMAT.md (github skibidiskib/Ai-codex) - fixed SS-sections,
pipe tables, monotonic ids, status cells, one-file <= 500 lines.

Why this exists: /rnd runs must NOT re-derive the world every time. The model
supplies judgment (claim text, verdicts, which falsifier flipped); this module
does the mechanical, non-hallucinated file operations around that judgment --
assigning ids, writing rows, enforcing invariants, keeping the file inside the
one-file line budget. STDLIB ONLY.

Thesis file sections, fixed order (never reordered):
    SS T THESIS  - the verdict, DERIVED from SS C (never hand-set elsewhere)
    SS C CLAIMS  - pipe table: id | st | claim | conf | falsifier | source | seen
                   id: C1, C2, ... monotonic, never reused. '*' suffix = load-bearing.
                   st: V verified / A assumed / R refuted (kept, never deleted) / O open.
    SS F FLIPS   - pre-registered kill conditions that would flip the verdict
    SS Q OPEN    - open questions not yet investigated
    SS D DIFF    - append-only pipe table: run | date | delta | verdict | cost
    SS M METER   - cost accounting (free-form key: value lines)
    SS B BUGS    - backprop log: id | date | cause | fix->invariant

Pipe-table cell rules (FORMAT.md): literal '|' escaped as '\\|', empty cell
is '-', cells are trimmed.

Invariants this module enforces mechanically (see SPEC SS V):
    V2 - a claim with no source can never be load-bearing and is forced to
         st='A' (assumed), regardless of what the caller asked for.
    V4 - refuted claims (st=R) are kept in SS C forever, never deleted.
    V8 - every run's diff append + meter update survives a crash (atomic write).
    V9 - file > 500 lines -> compact SS D oldest-first, never split the file.

Public API = the module's function signatures; CLI = `ledger.py --help`.
Both are the source of truth: a hand-kept copy here went stale (it listed 3
of 12 subcommands and none of the mutation API), which is why it is gone.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
from datetime import date as _date
from pathlib import Path

# ---------------------------------------------------------------------------
# fixed schema (SPEC SS I.1 / ai-codex FORMAT.md)
# ---------------------------------------------------------------------------

MAX_LINES = 500  # V9: one-file rule; compact SS D oldest-first past this

# internal field names (dict keys) per table section, in column order.
FIELDS = {
    "C": ["id", "st", "cls", "claim", "conf", "falsifier", "source", "seen"],
    "F": ["id", "condition", "last_checked", "holds"],
    "Q": ["id", "st", "question", "blast", "cites", "closed_by"],
    "D": ["run", "date", "delta", "verdict", "cost"],
    "B": ["id", "date", "cause", "fix"],
}
# the literal header row text written to the file (FORMAT.md examples).
HEADERS = {
    "C": ["id", "st", "cls", "claim", "conf", "falsifier", "source", "seen"],
    "F": ["id", "if this becomes true -> verdict flips to", "last-checked", "holds?"],
    "Q": ["id", "st", "question", "blast", "cites", "closed_by"],
    "D": ["run", "date", "delta", "verdict", "cost"],
    "B": ["id", "date", "cause", "fix->invariant"],
}
# Columns added AFTER theses already existed in the wild. A file whose header
# lacks one is parsed without it (default '-') instead of shifting every cell
# one place left, which would silently scramble every row. render() always
# writes the current schema, so any mutation upgrades the file in place.
OPTIONAL_FIELDS = {"C": ("cls",), "Q": ("closed_by",)}

VALID_CLAIM_ST = {"V", "A", "R", "O"}

# V10 -- claim CLASS: what KIND of evidence could ever settle this claim.
# The point: research tools verify what a desk can reach, so a thesis drifts
# toward confident world-claims and assumed customer-claims without anyone
# noticing. Classing them makes that visible, and makes it impossible for
# desk research to pass itself off as demand validation.
# world: settled by desk research (competitors, regulation, pricing, tech)
# customer: settled ONLY by buyer contact (will they pay, are they reachable)
# internal: settled by our own data (our hours, capacity, unit economics)
VALID_CLAIM_CLS = {"world", "customer", "internal"}
# A customer-class claim goes st='V' only when its source is a BUYER
# INTERACTION (a reply, a booked call, a signature, a payment). A research
# comparable is a world-class source and can never verify a customer claim.
# ENFORCED: to mark a customer claim V, the source must carry a typed
# evidence tag -- `buyer:reply|call|signature|payment <detail>`. The tool
# verifies the TAG, not the truth of the detail: it enforces that the
# question "did a buyer actually settle this?" is asked in a checkable form.
# The stamp is tamper-EVIDENT, not a lie detector.
# V15 -- the evidence LADDER: each tier carries a tool-enforced confidence
# CAP for customer claims. A waitlist signup is real buyer signal, but it is
# not a signed order; the cap keeps weak signal from laundering into strong.
BUYER_EVIDENCE_CAPS = {
    "signup": 0.40,      # waitlist join, preorder intent, ad-driven CPL
    "reply": 0.50,       # a prospect replied with genuine interest
    "call": 0.65,        # a booked AND held discovery/demo call
    "signature": 0.85,   # signed pilot / LOI / contract
    "payment": 0.95,     # money moved
}
VALID_BUYER_EVIDENCE = set(BUYER_EVIDENCE_CAPS)
_BUYER_EVIDENCE_RE = re.compile(
    r"^\s*buyer:(signup|reply|call|signature|payment)\b", re.IGNORECASE)


def has_buyer_evidence(source) -> bool:
    """True if a source string carries the typed buyer-interaction tag."""
    return bool(_BUYER_EVIDENCE_RE.match(str(source or "")))


def buyer_evidence_tier(source):
    """The ladder tier named in a buyer: tag, or None."""
    m = _BUYER_EVIDENCE_RE.match(str(source or ""))
    return m.group(1).lower() if m else None


def _clamp_customer_conf(claim_dict) -> bool:
    """V15: cap a customer claim's confidence at its evidence tier's
    ceiling. Returns True if a clamp happened (callers report it loudly -
    a silent clamp would be a prose rule wearing a code costume)."""
    if (claim_dict.get("cls") != "customer"
            or (claim_dict.get("st") or "").upper() != "V"):
        return False
    tier = buyer_evidence_tier(claim_dict.get("source"))
    if tier is None or claim_dict.get("conf") is None:
        return False
    cap = BUYER_EVIDENCE_CAPS[tier]
    if claim_dict["conf"] > cap:
        claim_dict["conf"] = cap
        return True
    return False


_V10_MSG = ("V10: a customer claim can only be VERIFIED by a typed buyer "
            "interaction. Prefix the source with buyer:reply|call|signature|"
            "payment (e.g. source='buyer:call 3 demos booked 2026-08-01'), "
            "or keep st='A' until a buyer actually settles it.")
SECTION_HEADING = {
    "T": "## §T THESIS",
    "C": "## §C CLAIMS",
    "F": "## §F FLIPS",
    "Q": "## §Q OPEN",
    "D": "## §D DIFF",
    "M": "## §M METER",
    "B": "## §B BUGS",
}
SECTION_ORDER = ["T", "C", "F", "Q", "D", "M", "B"]


def fix_console_encoding() -> None:
    """UTF-8 stdout/stderr so SS/arrow glyphs never crash a cp1252 console.
    Shared by every tool in this package (ponytail: one home, four callers)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def _today() -> str:
    return _date.today().isoformat()


# ---------------------------------------------------------------------------
# pipe-table cell rules: escape literal '|' as '\|', empty cell = '-', trim
# ---------------------------------------------------------------------------

def _escape_cell(value) -> str:
    s = "" if value is None else str(value)
    s = s.replace("|", "\\|").strip()
    return s if s else "-"


def _split_row(line: str) -> list:
    """Split one pipe-table row on UNESCAPED '|', then unescape+trim cells."""
    parts = re.split(r"(?<!\\)\|", line)
    return [p.strip().replace("\\|", "|") for p in parts]


def _join_row(cells) -> str:
    return " | ".join(_escape_cell(c) for c in cells)


def _fmt_num(x) -> str:
    if x is None:
        return "-"
    if isinstance(x, int):
        return str(x)
    s = f"{float(x):.6f}".rstrip("0").rstrip(".")
    return s if s else "0"


# ---------------------------------------------------------------------------
# parsing: split the file into SS-sections, then into rows
# ---------------------------------------------------------------------------

_SECTION_RE = re.compile(r"^##\s*§([A-Z])\s+\S.*$")
_TITLE_RE = re.compile(r"^#\s+THESIS:\s*(.+)$")
_VERDICT_RE = re.compile(
    r"^verdict:\s*(?P<verdict>.+?)\s*\(conf\s*(?P<conf>[^)]*)\)\s*"
    r"·\s*as-of run\s*(?P<run>\S+)\s*·\s*(?P<date>[^·]+?)\s*(?:·.*)?$"
)


def _split_sections(text: str) -> dict:
    """{section_letter: [body lines]} split on '## SSX NAME' headings."""
    out = {s: [] for s in SECTION_ORDER}
    cur = None
    for line in text.splitlines():
        m = _SECTION_RE.match(line.strip())
        if m:
            cur = m.group(1)
            continue
        if cur is not None and cur in out:
            out[cur].append(line)
    return out


def _parse_preamble(text: str) -> dict:
    title, slug, created = "", "", ""
    for line in text.splitlines():
        if line.startswith("## §"):
            break
        m = _TITLE_RE.match(line.strip())
        if m:
            title = m.group(1).strip()
        elif line.strip().startswith("slug:"):
            slug = line.split(":", 1)[1].strip()
        elif line.strip().startswith("created:"):
            created = line.split(":", 1)[1].strip()
    return {"title": title, "slug": slug, "created": created}


def _parse_thesis(body_lines) -> dict:
    v = {"verdict": "open", "conf": None, "run": 0, "date": _today(), "one_line": "-"}
    for line in body_lines:
        s = line.strip()
        if not s:
            continue
        m = _VERDICT_RE.match(s)
        if m:
            conf_raw = m.group("conf").strip()
            run_raw = m.group("run").strip()
            v["verdict"] = m.group("verdict").strip()
            v["conf"] = None if conf_raw in ("", "-") else float(conf_raw)
            v["run"] = 0 if run_raw in ("", "-") else int(run_raw)
            v["date"] = m.group("date").strip()
        elif s.startswith("one-line:"):
            v["one_line"] = s.split(":", 1)[1].strip()
    return v


def _effective_fields(body_lines, section) -> list:
    """The column list THIS file actually uses, for sections that have gained
    columns since older theses were written. Decided by the header row, by
    name -- never by counting cells, which would guess wrong on a row that
    happens to contain an escaped pipe."""
    fields = list(FIELDS[section])
    optional = OPTIONAL_FIELDS.get(section)
    if not optional:
        return fields
    data_lines = [l for l in body_lines if l.strip() != ""]
    if not data_lines:
        return fields
    header = {c.strip().lower() for c in _split_row(data_lines[0])}
    return [f for f in fields if f not in optional or f in header]


def _parse_table(body_lines, fields, canonical=None) -> list:
    """First non-empty line is the header row (skipped); rest are data rows.
    `fields` is the file's effective column list; every row is then padded out
    to `canonical` so callers always see the full current schema."""
    data_lines = [l for l in body_lines if l.strip() != ""]
    rows = []
    for line in data_lines[1:]:
        cells = _split_row(line)
        if len(cells) < len(fields):
            cells += ["-"] * (len(fields) - len(cells))
        row = dict(zip(fields, cells[: len(fields)]))
        for f in (canonical or fields):
            row.setdefault(f, "-")
        rows.append(row)
    return rows


def _parse_section_table(body_lines, section) -> list:
    return _parse_table(body_lines, _effective_fields(body_lines, section),
                        canonical=FIELDS[section])


def _parse_claims(body_lines) -> list:
    rows = _parse_section_table(body_lines, "C")
    claims = []
    for r in rows:
        raw_id = r["id"]
        load_bearing = raw_id.endswith("*")
        cid = raw_id[:-1] if load_bearing else raw_id
        conf_raw = r["conf"]
        conf = None if conf_raw in ("", "-") else float(conf_raw)
        claims.append({
            "id": cid,
            "load_bearing": load_bearing,
            "st": r["st"],
            "cls": (r.get("cls") or "-").strip().lower(),
            "claim": r["claim"],
            "conf": conf,
            "falsifier": r["falsifier"],
            "source": r["source"],
            "seen": r["seen"],
        })
    return claims


# ---------------------------------------------------------------------------
# V10: demand status -- DERIVED, never stored, so it can never go stale
# ---------------------------------------------------------------------------

def demand_status(doc: dict) -> dict:
    """Is this verdict resting on unvalidated demand?

    Counts the customer-class claims (the ones only a buyer can settle) and
    reports whether any is VERIFIED. Refuted claims don't count either way --
    a killed customer claim is neither support nor an open assumption.

    Returns {total, verified, assumed, unclassified, unvalidated, flag}.
    `flag` is the string render() stamps onto the §T verdict line, or None
    when there is nothing to warn about.
    """
    claims = doc.get("claims") or []
    cust = [c for c in claims if (c.get("cls") or "").lower() == "customer"
            and (c.get("st") or "").upper() != "R"]
    verified = [c for c in cust if (c.get("st") or "").upper() == "V"
                and has_buyer_evidence(c.get("source"))]
    assumed = [c for c in cust if (c.get("st") or "").upper() in ("A", "O")]
    unclassified = [c for c in claims if (c.get("cls") or "-") in ("-", "")
                    and (c.get("st") or "").upper() != "R"]

    flag = None
    if cust and not verified:
        ids = ",".join(c["id"] for c in assumed) or "-"
        flag = (f"demand-UNVALIDATED: {len(cust)} customer claim(s), 0 verified "
                f"by buyer contact ({ids})")
    elif not cust and claims:
        flag = "demand-UNTESTED: no customer-class claim exists yet"

    return {
        "total": len(cust),
        "verified": len(verified),
        "assumed": len(assumed),
        "unclassified": len(unclassified),
        "unvalidated": bool(flag),
        "flag": flag,
    }


def _parse_diffs(body_lines) -> list:
    rows = _parse_table(body_lines, FIELDS["D"])
    for r in rows:
        try:
            r["run"] = int(r["run"])
        except ValueError:
            pass
    return rows


def _parse_meter(body_lines) -> dict:
    meter = {}
    for line in body_lines:
        s = line.strip()
        if not s or ":" not in s:
            continue
        k, val = s.split(":", 1)
        meter[k.strip()] = val.strip()
    return meter


def parse(path) -> dict:
    """Parse a thesis file into a dict: {title, slug, created, verdict,
    claims, flips, opens, diffs, meter, bugs}. `verdict` is itself a dict
    {verdict, conf, run, date, one_line}. Each of claims/flips/opens/diffs/
    bugs is a list of row-dicts; meter is a flat key->value dict.
    """
    text = Path(path).read_text(encoding="utf-8")
    sections = _split_sections(text)
    doc = _parse_preamble(text)
    doc["verdict"] = _parse_thesis(sections["T"])
    doc["claims"] = _parse_claims(sections["C"])
    doc["flips"] = _parse_section_table(sections["F"], "F")
    doc["opens"] = _parse_section_table(sections["Q"], "Q")
    doc["diffs"] = _parse_diffs(sections["D"])
    doc["meter"] = _parse_meter(sections["M"])
    doc["bugs"] = _parse_section_table(sections["B"], "B")
    return doc


# ---------------------------------------------------------------------------
# rendering: doc -> stable text (the inverse of parse)
# ---------------------------------------------------------------------------

def render(doc: dict) -> str:
    """Serialize a doc dict (as returned/mutated from parse()) back to the
    fixed-section markdown text. parse(render(doc)-written-to-a-file) round-
    trips to the same doc (modulo cell whitespace normalization).
    """
    lines = []
    lines.append(f"# THESIS: {doc.get('title', '')}")
    lines.append(f"slug: {doc.get('slug', '')}")
    lines.append(f"created: {doc.get('created') or _today()}")
    lines.append("")

    lines.append(SECTION_HEADING["T"])
    v = doc.get("verdict") or {}
    conf_s = _fmt_num(v.get("conf"))
    run = v.get("run", 0) or 0
    date = v.get("date") or _today()
    # V10: the demand flag is DERIVED from §C on every write. It is never
    # stored and never hand-set, so it cannot drift from the claims and it
    # cannot be quietly deleted -- the next mutation puts it straight back.
    flag = demand_status(doc)["flag"]
    verdict_line = (f"verdict: {v.get('verdict', 'open')} (conf {conf_s}) · "
                    f"as-of run {run} · {date}")
    if flag:
        verdict_line += f" · ⚠ {flag}"
    lines.append(verdict_line)
    lines.append(f"one-line: {v.get('one_line', '-')}")
    lines.append("")

    lines.append(SECTION_HEADING["C"])
    lines.append(_join_row(HEADERS["C"]))
    for c in doc.get("claims", []):
        cid = c["id"] + ("*" if c.get("load_bearing") else "")
        lines.append(_join_row([
            cid, c.get("st", "O"), c.get("cls", "-"), c.get("claim", "-"),
            _fmt_num(c.get("conf")),
            c.get("falsifier", "-"), c.get("source", "-"), c.get("seen", "-"),
        ]))
    lines.append("")

    lines.append(SECTION_HEADING["F"])
    lines.append(_join_row(HEADERS["F"]))
    for f in doc.get("flips", []):
        lines.append(_join_row([f.get(k, "-") for k in FIELDS["F"]]))
    lines.append("")

    lines.append(SECTION_HEADING["Q"])
    lines.append(_join_row(HEADERS["Q"]))
    for q in doc.get("opens", []):
        lines.append(_join_row([q.get(k, "-") for k in FIELDS["Q"]]))
    lines.append("")

    lines.append(SECTION_HEADING["D"])
    lines.append(_join_row(HEADERS["D"]))
    for d in doc.get("diffs", []):
        lines.append(_join_row([d.get(k, "-") for k in FIELDS["D"]]))
    lines.append("")

    lines.append(SECTION_HEADING["M"])
    meter = doc.get("meter") or {"fixed": "-", "marginal": "-", "total": "-", "trim": "-"}
    for k, val in meter.items():
        lines.append(f"{k}: {val}")
    lines.append("")

    lines.append(SECTION_HEADING["B"])
    lines.append(_join_row(HEADERS["B"]))
    for b in doc.get("bugs", []):
        lines.append(_join_row([b.get(k, "-") for k in FIELDS["B"]]))

    return "\n".join(lines) + "\n"


def _atomic_write(path, text: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, p)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _write(path, doc: dict) -> None:
    _atomic_write(path, render(doc))


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------

def new(slug: str, title: str) -> str:
    """Return a fresh thesis template (text, not yet written to disk)."""
    doc = {
        "title": title,
        "slug": slug,
        "created": _today(),
        "verdict": {"verdict": "open", "conf": None, "run": 0,
                    "date": _today(), "one_line": "-"},
        "claims": [],
        "flips": [],
        "opens": [],
        "diffs": [],
        "meter": {"fixed": "-", "marginal": "-", "total": "-", "trim": "-"},
        "bugs": [],
    }
    return render(doc)


def _norm_cls(cls) -> str:
    """Validate/normalize a claim class. '-'/None = unclassified (allowed, so
    older theses still parse and write, but reported by demand_status)."""
    c = (cls or "-").strip().lower()
    if c in ("", "-"):
        return "-"
    if c not in VALID_CLAIM_CLS:
        raise ValueError(
            f"cls must be one of {sorted(VALID_CLAIM_CLS)} or '-', got {cls!r}")
    return c


def add_claim(path, claim: str, st: str, conf, falsifier: str = "-",
              source: str = "-", load_bearing: bool = False,
              seen: str = None, cls: str = "-") -> str:
    """Append a new SS C claim row. Returns the assigned id (e.g. 'C4' or 'C4*').

    Ids are monotonic and never reused (max existing Cn + 1).
    V2 guard: a claim with no source can never be load-bearing and is
    force-downgraded to st='A' (assumed), regardless of what was asked for.
    `cls` (V10) is world / customer / internal -- what kind of evidence could
    settle it. See VALID_CLAIM_CLS.
    """
    st = (st or "").upper().strip()
    if st not in VALID_CLAIM_ST:
        raise ValueError(f"st must be one of {sorted(VALID_CLAIM_ST)}, got {st!r}")
    cls = _norm_cls(cls)

    doc = parse(path)

    has_source = source not in (None, "", "-")
    if not has_source:
        st = "A"
        load_bearing = False
    if cls == "customer" and st == "V" and not has_buyer_evidence(source):
        raise ValueError(_V10_MSG)
    _pending_clamp = {"cls": cls, "st": st, "source": source,
                      "conf": None if conf in (None, "", "-") else float(conf)}
    if _clamp_customer_conf(_pending_clamp):
        conf = _pending_clamp["conf"]   # V15 cap applied; CLI reports it

    next_n = 1
    for c in doc["claims"]:
        m = re.match(r"C(\d+)$", c["id"])
        if m:
            next_n = max(next_n, int(m.group(1)) + 1)
    cid = f"C{next_n}"

    doc["claims"].append({
        "id": cid,
        "load_bearing": bool(load_bearing),
        "st": st,
        "cls": cls,
        "claim": claim,
        "conf": None if conf in (None, "", "-") else float(conf),
        "falsifier": falsifier or "-",
        "source": source or "-",
        "seen": seen or _today(),
    })
    _write(path, doc)
    return cid + ("*" if load_bearing else "")


def set_verdict(path, verdict: str, conf, run: int, date: str, one_line: str) -> None:
    """Rewrite SS T THESIS. V1: the verdict is DERIVED from SS C by the
    caller's judgment (this library never grades it) -- this just performs
    the mechanical, exact-format rewrite of the two SS T lines.
    """
    doc = parse(path)
    doc["verdict"] = {
        "verdict": verdict,
        "conf": None if conf in (None, "", "-") else float(conf),
        "run": int(run),
        "date": date,
        "one_line": one_line,
    }
    _write(path, doc)


def append_diff(path, run: int, date: str, delta: str, verdict: str, cost: str) -> None:
    """Append one SS D row. Append-only (V4/V8): never edits/removes prior rows."""
    doc = parse(path)
    doc["diffs"].append({
        "run": int(run), "date": date, "delta": delta,
        "verdict": verdict, "cost": cost,
    })
    _write(path, doc)


def set_claim(path, cid, st=None, conf=None, falsifier=None,
              source=None, load_bearing=None, claim=None, cls=None) -> bool:
    """Revise an existing §C claim in place - the recheck/diff loop's V→R /
    conf± update. Only the fields you pass change. Re-applies the V2 guard:
    a claim left with no source is forced st='A' and load_bearing stripped.
    Returns True if a claim matched cid (with or without a trailing '*'),
    False if not found. Log the change in §D via append_diff()."""
    want = cid.rstrip("*")
    doc = parse(path)
    hit = next((c for c in doc["claims"] if c["id"] == want), None)
    if hit is None:
        return False
    if st is not None:
        st = st.upper().strip()
        if st not in VALID_CLAIM_ST:
            raise ValueError(f"st must be one of {sorted(VALID_CLAIM_ST)}, got {st!r}")
        hit["st"] = st
    if cls is not None:
        hit["cls"] = _norm_cls(cls)
    if claim is not None:
        hit["claim"] = claim
    if conf is not None:
        hit["conf"] = None if conf in ("", "-") else float(conf)
    if falsifier is not None:
        hit["falsifier"] = falsifier or "-"
    if source is not None:
        hit["source"] = source or "-"
    if load_bearing is not None:
        hit["load_bearing"] = bool(load_bearing)
    if hit["source"] in (None, "", "-"):   # V2 guard
        hit["st"] = "A"
        hit["load_bearing"] = False
    if (hit.get("cls") == "customer" and hit["st"] == "V"
            and not has_buyer_evidence(hit["source"])):   # V10 guard
        raise ValueError(_V10_MSG)
    _clamp_customer_conf(hit)                              # V15 cap
    _write(path, doc)
    return True


def set_open(path, qid, st=None, question=None, blast=None, cites=None,
             closed_by=None) -> bool:
    """Update a §Q open-question row (e.g. mark st '.'→'x' when answered).
    Returns True if matched. Promote the actual answer to a §C claim via
    add_claim(), then pass that claim id as `closed_by` -- that link is what
    lets the yield meter tell a question closed on EVIDENCE from one closed
    on a guess, which is otherwise invisible once st flips to 'x'."""
    doc = parse(path)
    hit = next((q for q in doc["opens"] if q["id"] == qid), None)
    if hit is None:
        return False
    for k, v in (("st", st), ("question", question), ("blast", blast),
                 ("cites", cites), ("closed_by", closed_by)):
        if v is not None:
            hit[k] = v
    _write(path, doc)
    return True


def set_flip(path, fid, last_checked=None, holds=None, condition=None) -> bool:
    """Record a §F flip re-check: stamp last_checked + holds (y/n/untested).
    Returns True if matched."""
    doc = parse(path)
    hit = next((f for f in doc["flips"] if f["id"] == fid), None)
    if hit is None:
        return False
    for k, v in (("last_checked", last_checked), ("holds", holds), ("condition", condition)):
        if v is not None:
            hit[k] = v
    _write(path, doc)
    return True


# ---------------------------------------------------------------------------
# V16 retro: score the thesis's OWN track record, not the world's
# ---------------------------------------------------------------------------

def retro_report(doc: dict, today=None) -> dict:
    """How well has this thesis predicted? Mechanical; no model judgment.

    A ledger that re-checks the world every run and never re-checks itself
    has a hole where its own thesis lives. This is that check.
    """
    claims = doc.get("claims") or []
    diffs = [d for d in (doc.get("diffs") or []) if isinstance(d.get("run"), int)]
    diffs.sort(key=lambda d: d["run"])

    refuted = [c for c in claims if (c.get("st") or "").upper() == "R"]
    verified = [c for c in claims if (c.get("st") or "").upper() == "V"]
    assumed = [c for c in claims if (c.get("st") or "").upper() == "A"]
    confs = [c["conf"] for c in verified if c.get("conf") is not None]
    mean_v_conf = (sum(confs) / len(confs)) if confs else None
    settled = len(verified) + len(refuted)
    refute_rate = (len(refuted) / settled) if settled else None

    # calibration gap: a claim marked V at mean conf X implies a refutation
    # rate near (1 - X). Positive gap = overconfident.
    calib_gap = None
    if mean_v_conf is not None and refute_rate is not None:
        calib_gap = round(refute_rate - (1 - mean_v_conf), 3)

    verdicts = [d.get("verdict", "-") for d in diffs]
    flips_never = [f for f in (doc.get("flips") or [])
                   if (f.get("holds") or "").strip().lower() in ("untested", "", "-", "?")]
    flip_ages = []
    for f in flips_never:
        age = _days_since(f.get("last_checked"), today)
        if age is not None:
            flip_ages.append((f["id"], age))

    def _last_seen(pred):
        ds = [_days_since(c.get("seen"), today) for c in claims if pred(c)]
        ds = [d for d in ds if d is not None]
        return min(ds) if ds else None

    days_since_buyer = _last_seen(
        lambda c: c.get("cls") == "customer" and has_buyer_evidence(c.get("source")))
    days_since_world = _last_seen(lambda c: c.get("cls") == "world")

    return {
        "slug": doc.get("slug") or "-",
        "runs": len(diffs),
        "claims": len(claims),
        "verified": len(verified), "assumed": len(assumed), "refuted": len(refuted),
        "mean_verified_conf": None if mean_v_conf is None else round(mean_v_conf, 3),
        "refutation_rate": None if refute_rate is None else round(refute_rate, 3),
        "calibration_gap": calib_gap,
        "verdict_history": verdicts,
        "verdict_flipped": len(set(verdicts)) > 1,
        "flips_never_tested": flip_ages,
        "days_since_buyer_evidence": days_since_buyer,
        "days_since_world_claim": days_since_world,
        "demand_unvalidated": demand_status(doc)["unvalidated"],
    }


def render_retro(r: dict) -> str:
    L = [f"RETRO {r['slug']} - {r['runs']} run(s), {r['claims']} claims", ""]
    L.append(f"  settled: {r['verified']} verified / {r['refuted']} refuted"
             f" ({r['assumed']} still assumed)")
    if r["mean_verified_conf"] is not None:
        L.append(f"  stated confidence on verified claims: {r['mean_verified_conf']}")
    if r["refutation_rate"] is not None:
        L.append(f"  refutation rate: {r['refutation_rate']}")
    if r["calibration_gap"] is not None:
        if r["calibration_gap"] > 0.15:
            L.append(f"  !! OVERCONFIDENT by {r['calibration_gap']}: claims were "
                     f"refuted more often than their confidence implied")
        elif r["calibration_gap"] < -0.15:
            L.append(f"  ~  underconfident by {abs(r['calibration_gap'])}: "
                     f"claims survived better than stated")
        else:
            L.append(f"  calibration gap {r['calibration_gap']} (within +/-0.15)")
    if r["verdict_history"]:
        L.append(f"  verdict history: {' -> '.join(r['verdict_history'])}"
                 + ("  (CHANGED)" if r["verdict_flipped"] else "  (never moved)"))
        if not r["verdict_flipped"] and r["runs"] >= 3:
            L.append("  !! a verdict that never moved across 3+ runs is either "
                     "well-founded or unfalsifiable in practice - check which")
    for fid, age in r["flips_never_tested"]:
        L.append(f"  !! {fid} pre-registered {age}d ago and NEVER tested")
    b, w = r["days_since_buyer_evidence"], r["days_since_world_claim"]
    if w is not None and b is None:
        L.append(f"  !! last world claim {w}d ago; buyer evidence: NEVER. "
                 f"This thesis has only ever been desk-checked.")
    elif w is not None and b is not None:
        L.append(f"  last world claim {w}d ago; last buyer evidence {b}d ago")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# staleness: make an untested flip LOUD instead of merely recorded
# ---------------------------------------------------------------------------

def _days_since(iso_date, today=None):
    """Whole days between an ISO date and today. None if unparseable."""
    m = re.search(r"(\d{4}-\d{2}-\d{2})", str(iso_date or ""))
    if not m:
        return None
    try:
        then = _date.fromisoformat(m.group(1))
    except ValueError:
        return None
    now = _date.fromisoformat(today) if today else _date.today()
    return (now - then).days


def stale_report(doc: dict, days: int = 7, today=None) -> dict:
    """What in this thesis has gone unexamined?

    The failure this exists to stop: a ledger records everything faithfully and
    is then never read, so a pre-registered flip condition can sit `untested`
    for weeks while work continues around it. Recording a thing is not the same
    as surfacing it. NEVER-checked outranks stale-by-age -- a flip nobody has
    ever tested is worse than one tested a while ago, and it is the exact case
    that hides in plain sight.
    """
    never, stale_flips = [], []
    for f in doc.get("flips") or []:
        holds = (f.get("holds") or "").strip().lower()
        age = _days_since(f.get("last_checked"), today)
        if holds in ("untested", "", "-", "?"):
            never.append({"id": f["id"], "condition": f.get("condition", "-"),
                          "age": age})
        elif age is not None and age >= days:
            stale_flips.append({"id": f["id"], "condition": f.get("condition", "-"),
                                "age": age})

    stale_claims = []
    for c in doc.get("claims") or []:
        if not c.get("load_bearing") or (c.get("st") or "").upper() == "R":
            continue
        age = _days_since(c.get("seen"), today)
        if age is not None and age >= days:
            stale_claims.append({"id": c["id"], "claim": c.get("claim", "-"),
                                 "age": age, "st": c.get("st")})

    open_high = [{"id": q["id"], "question": q.get("question", "-"),
                  "blast": q.get("blast", "-")}
                 for q in doc.get("opens") or []
                 if (q.get("st") or "").strip() in (".", "~")
                 and (q.get("blast") or "").strip().lower() in ("high", "hi")]

    ds = demand_status(doc)
    return {
        "slug": doc.get("slug") or "-",
        "days": days,
        "never_checked": never,
        "stale_flips": stale_flips,
        "stale_claims": stale_claims,
        "open_high": open_high,
        "demand": ds,
        "any": bool(never or stale_flips or stale_claims or open_high or ds["flag"]),
    }


def render_stale(rep: dict) -> str:
    if not rep["any"]:
        return f"{rep['slug']}: nothing stale (threshold {rep['days']}d)"
    lines = [f"{rep['slug']}: NEEDS ATTENTION (threshold {rep['days']}d)"]
    for f in rep["never_checked"]:
        age = f" [pre-registered {f['age']}d ago]" if f["age"] is not None else ""
        lines.append(f"  !! {f['id']} NEVER TESTED{age}: {f['condition']}")
    for f in rep["stale_flips"]:
        lines.append(f"  ~  {f['id']} last checked {f['age']}d ago: {f['condition']}")
    for c in rep["stale_claims"]:
        lines.append(f"  ~  {c['id']} load-bearing, {c['age']}d old ({c['st']}): "
                     f"{c['claim'][:70]}")
    for q in rep["open_high"]:
        lines.append(f"  ?  {q['id']} open, blast {q['blast']}: {q['question'][:70]}")
    if rep["demand"]["flag"]:
        lines.append(f"  !! {rep['demand']['flag']}")
    return "\n".join(lines)


def compact(path) -> dict:
    """Enforce V9: if the rendered file exceeds MAX_LINES, drop the OLDEST
    SS D rows first (never touch SS C, never split the file), and note the
    event as a SS B bugs row. No-op (compacted=False) if already under budget.
    """
    doc = parse(path)
    n_lines = len(render(doc).splitlines())
    if n_lines <= MAX_LINES:
        return {"compacted": False, "lines": n_lines, "dropped": 0}

    # the SS B note itself adds one line, so drop one extra row to net under budget.
    excess = n_lines - MAX_LINES + 1
    dropped = min(excess, len(doc["diffs"]))
    doc["diffs"] = doc["diffs"][dropped:]

    next_b = 1
    for b in doc["bugs"]:
        m = re.match(r"B(\d+)$", b.get("id", ""))
        if m:
            next_b = max(next_b, int(m.group(1)) + 1)
    doc["bugs"].append({
        "id": f"B{next_b}",
        "date": _today(),
        "cause": f"file {n_lines} ln > {MAX_LINES}",
        "fix": f"compacted §D oldest-first: dropped {dropped} row(s) -> V9",
    })

    _write(path, doc)
    after_lines = len(render(doc).splitlines())
    return {
        "compacted": True,
        "lines_before": n_lines,
        "lines_after": after_lines,
        "dropped": dropped,
        "still_over": after_lines > MAX_LINES,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli_new(args) -> int:
    text = new(args.slug, args.title)
    if args.out:
        out = Path(args.out)
        _atomic_write(out, text)
        print(f"OK: wrote {out}")
    else:
        print(text, end="")
    return 0


def _cli_show(args) -> int:
    doc = parse(args.path)
    v = doc["verdict"]
    print(f"{doc.get('title') or '(untitled)'}  [{doc.get('slug') or '-'}]")
    print(f"verdict: {v['verdict']} (conf {_fmt_num(v['conf'])}) - "
          f"as-of run {v['run']} - {v['date']}")
    print(f"one-line: {v['one_line']}")
    by_st = {}
    for c in doc["claims"]:
        by_st[c["st"]] = by_st.get(c["st"], 0) + 1
    lb = sum(1 for c in doc["claims"] if c["load_bearing"])
    print(f"claims: {len(doc['claims'])} total, {lb} load-bearing "
          f"(V={by_st.get('V', 0)} A={by_st.get('A', 0)} "
          f"R={by_st.get('R', 0)} O={by_st.get('O', 0)})")
    by_cls = {}
    for c in doc["claims"]:
        key = c.get("cls", "-") or "-"
        slot = by_cls.setdefault(key, {"n": 0, "V": 0})
        slot["n"] += 1
        if c["st"] == "V":
            slot["V"] += 1
    print("class: " + ", ".join(
        f"{k}={v['n']} ({v['V']} verified)" for k, v in sorted(by_cls.items())))
    ds = demand_status(doc)
    if ds["flag"]:
        print(f"  !! {ds['flag']}")
    if ds["unclassified"]:
        print(f"  note: {ds['unclassified']} claim(s) unclassified -- "
              f"set cls to world/customer/internal")
    print(f"flips: {len(doc['flips'])}  open-qs: {len(doc['opens'])}  "
          f"diff-rows: {len(doc['diffs'])}  bugs: {len(doc['bugs'])}")
    if doc["meter"]:
        print("meter: " + ", ".join(f"{k}={mv}" for k, mv in doc["meter"].items()))
    return 0


def _cli_add_claim(args) -> int:
    cid = add_claim(args.path, args.claim, args.st, args.conf,
                    falsifier=args.falsifier or "-", source=args.source or "-",
                    load_bearing=bool(args.load_bearing), cls=args.cls or "-",
                    seen=args.seen)
    print(f"added {cid}")
    applied = next(c for c in parse(args.path)["claims"]
                   if c["id"] == cid.rstrip("*"))
    if (args.st or "").upper() != applied["st"] or (bool(args.load_bearing)
                                                     and not applied["load_bearing"]):
        print("note: V2 guard applied -- no source, so stored as ASSUMED and "
              "not load-bearing")
    return 0


def _cli_set_claim(args) -> int:
    ok = set_claim(args.path, args.cid, st=args.st, conf=args.conf,
                   falsifier=args.falsifier, source=args.source,
                   claim=args.claim, cls=args.cls,
                   load_bearing=args.load_bearing)
    print(f"revised {args.cid}" if ok else f"NOT FOUND: {args.cid}")
    return 0 if ok else 1


def _cli_set_open(args) -> int:
    ok = set_open(args.path, args.qid, st=args.st, question=args.question,
                  blast=args.blast, cites=args.cites, closed_by=args.closed_by)
    print(f"updated {args.qid}" if ok else f"NOT FOUND: {args.qid}")
    return 0 if ok else 1


def _cli_set_flip(args) -> int:
    ok = set_flip(args.path, args.fid, last_checked=args.last_checked,
                  holds=args.holds, condition=args.condition)
    print(f"stamped {args.fid}" if ok else f"NOT FOUND: {args.fid}")
    return 0 if ok else 1


def _cli_set_verdict(args) -> int:
    set_verdict(args.path, args.verdict, args.conf, args.run, args.date,
                args.one_line)
    print("verdict set")
    return 0


def _cli_append_diff(args) -> int:
    append_diff(args.path, args.run, args.date, args.delta, args.verdict,
                args.cost)
    print(f"appended run {args.run}")
    return 0


def _cli_compact(args) -> int:
    print(compact(args.path))
    return 0


def _cli_demo(args) -> int:
    """The 30-second self-demonstration: scaffold a thesis, show the derived
    demand stamp, tamper with it by hand, watch one mutation put it back,
    try to clear it with free text (refused), clear it with typed buyer
    evidence. This is the product's central claim, executed live."""
    own_dir = args.dir is None
    d = Path(tempfile.mkdtemp(prefix="rnd_demo_")) if own_dir else Path(args.dir)
    d.mkdir(parents=True, exist_ok=True)
    p = d / "demo-thesis.md"

    def verdict_line():
        return next(l for l in p.read_text(encoding="utf-8").splitlines()
                    if l.startswith("verdict:"))

    try:
        print("1. scaffold a thesis, add a desk-verified claim and a customer claim:")
        _atomic_write(p, new("demo", "Demo: a paid changelog tool"))
        add_claim(p, "rivals bundle the feature free", "V", 0.8,
                  falsifier="a paying user cites no free rival",
                  source="example.com/pricing", load_bearing=True, cls="world")
        add_claim(p, "small dev teams will pay us for it", "A", 0.3,
                  falsifier="0 of 5 warm intros convert", cls="customer")
        print(f"   {verdict_line()}")

        print("\n2. tamper: hand-delete the stamp from the file on disk...")
        stripped = "\n".join(
            (l.split(" \u00b7 \u26a0 ")[0] if l.startswith("verdict:") else l)
            for l in p.read_text(encoding="utf-8").splitlines())
        _atomic_write(p, stripped + "\n")
        print(f"   {verdict_line()}")

        print("\n3. any mutation re-derives it -- the stamp is not stored, so it")
        print("   cannot stay deleted:")
        set_claim(p, "C1", conf=0.85)
        print(f"   {verdict_line()}")

        print("\n4. try to clear it with free text (a press release, a comparable):")
        try:
            set_claim(p, "C2", st="V", source="pricing comparable, analyst note")
            print("   BUG: free text cleared the stamp")
            return 1
        except ValueError:
            print("   REFUSED (V10): only a typed buyer interaction can verify a")
            print("   customer claim -- buyer:reply|call|signature|payment")

        print("\n5. clear it with typed buyer evidence:")
        set_claim(p, "C2", st="V", source="buyer:call 2 teams booked a pilot")
        print(f"   {verdict_line()}")

        print("\nWhat this enforces: the buyer-contact question is ASKED, in a")
        print("checkable form, on every write. The truth of the evidence is the")
        print("operator's -- the tool is tamper-evident, not a lie detector.")
        if not own_dir:
            print(f"\nthesis left at: {p}")
        return 0
    finally:
        if own_dir:
            shutil.rmtree(d, ignore_errors=True)


def _cli_retro(args) -> int:
    """Score the thesis's own track record (V16)."""
    paths = ([p for p in sorted(Path(args.dir).glob("*.md")) if p.name != "_index.md"]
             if args.dir else [Path(args.path)])
    if not paths:
        print("give a thesis path or --dir <folder>", file=sys.stderr)
        return 2
    for p in paths:
        r = retro_report(parse(p), today=args.today)
        if r["slug"] == "-":
            r["slug"] = p.stem
        print(render_retro(r))
        print()
    return 0


def _cli_stale(args) -> int:
    """Exit 1 when anything needs attention, so a scheduled brief can gate on it."""
    if args.dir:
        paths = sorted(p for p in Path(args.dir).glob("*.md")
                       if p.name != "_index.md")
    elif args.path:
        paths = [Path(args.path)]
    else:
        print("give a thesis path or --dir <folder>", file=sys.stderr)
        return 2

    hits = 0
    for p in paths:
        try:
            rep = stale_report(parse(p), days=args.days, today=args.today)
        except Exception as e:
            print(f"{p.name}: could not parse ({e})")
            hits += 1
            continue
        rep["slug"] = rep["slug"] if rep["slug"] != "-" else p.stem
        print(render_stale(rep))
        hits += 1 if rep["any"] else 0
    return 1 if hits else 0


def _selftest() -> None:
    """new -> add 3 claims (1 load-bearing, 1 refuted) -> set verdict ->
    append 2 diff rows -> re-parse -> assert round-trip. Also exercises the
    V2 no-source guard, pipe-cell escaping, and the compact() one-file rule.
    """
    tmp_dir = Path(tempfile.mkdtemp(prefix="ledger_selftest_"))
    try:
        path = tmp_dir / "test-thesis.md"

        # encoding canary: the section sign must be the single codepoint
        # U+00A7. If source ever gets mojibake'd (e.g. a cp1252/utf-8 round
        # trip doubling it to 'A-circumflex + section'), REAL files stop
        # parsing while a corrupted selftest would stay self-consistently
        # green - this line is what breaks instead.
        assert SECTION_HEADING["T"] == "## \u00a7T THESIS", SECTION_HEADING["T"]
        assert _SECTION_RE.pattern.count("\u00a7") == 1

        text = new("test-thesis", "Self Test Thesis")
        assert "§T THESIS" in text
        assert "§C CLAIMS" in text
        _atomic_write(path, text)

        cid1 = add_claim(path, "rivals bundle the feature free | inline note", st="V",
                          conf=0.85, falsifier="a paying user cites no free rival",
                          source="example.com/pricing-faq", load_bearing=True)
        cid2 = add_claim(path, "target users are reachable via warm intros", st="A",
                          conf=0.3, source="-")
        cid3 = add_claim(path, "the $500 pilot design is fine as-is", st="R", conf=None,
                          falsifier="pulls the pilot inside a regulated perimeter",
                          source="example.gov/reg-101")
        assert cid1 == "C1*", cid1
        assert cid2 == "C2", cid2
        assert cid3 == "C3", cid3

        # V2 guard: no source -> forced st=A, load_bearing stripped even
        # though V + load_bearing=True were explicitly requested.
        cid4 = add_claim(path, "unsourced optimistic claim", st="V", conf=0.9,
                          source="-", load_bearing=True)
        assert cid4 == "C4", cid4

        set_verdict(path, verdict="reshape", conf=0.7, run=1,
                    date="2026-07-23", one_line="the conclusive argument")

        append_diff(path, run=1, date="2026-07-23",
                    delta="+4 claims, full sweep", verdict="reshape",
                    cost="165k tok / $2.10")
        append_diff(path, run=2, date="2026-07-24",
                    delta="C1 re-held, +0 new", verdict="reshape",
                    cost="22k tok / $0.28")

        doc = parse(path)
        assert len(doc["claims"]) == 4, doc["claims"]
        ids = [c["id"] for c in doc["claims"]]
        assert ids == ["C1", "C2", "C3", "C4"], ids  # monotonic C1..C4
        assert doc["claims"][0]["load_bearing"] is True
        assert doc["claims"][1]["load_bearing"] is False
        assert doc["claims"][2]["st"] == "R"
        assert doc["claims"][0]["claim"] == "rivals bundle the feature free | inline note"
        assert doc["claims"][3]["st"] == "A"
        assert doc["claims"][3]["load_bearing"] is False  # V2 guard held

        v = doc["verdict"]
        assert v["verdict"] == "reshape"
        assert v["conf"] is not None and abs(v["conf"] - 0.7) < 1e-9
        assert v["run"] == 1
        assert v["one_line"] == "the conclusive argument"

        assert len(doc["diffs"]) == 2
        assert doc["diffs"][0]["run"] == 1
        assert doc["diffs"][1]["run"] == 2
        assert doc["diffs"][1]["cost"] == "22k tok / $0.28"

        # --- legacy files (written before cls/closed_by existed) -----------
        # The failure mode this guards: parsing a 7-column §C row with the
        # 8-column schema would shift every cell left, putting claim text in
        # `cls` and the falsifier in `source`. Silent, and it would corrupt
        # the file on the next write.
        legacy = tmp_dir / "legacy.md"
        _atomic_write(legacy,
            "# THESIS: Legacy\nslug: legacy\ncreated: 2026-07-21\n\n"
            "## §T THESIS\nverdict: reshape (conf 0.7) · as-of run 1 · 2026-07-21\n"
            "one-line: old format\n\n"
            "## §C CLAIMS\n"
            "id | st | claim | conf | falsifier | source | seen\n"
            "C1* | V | rivals bundle the feature free | 0.85 | a paying user cites none | example.com | 2026-07-21\n\n"
            "## §F FLIPS\nid | if this becomes true -> verdict flips to | last-checked | holds?\n\n"
            "## §Q OPEN\nid | st | question | blast | cites\n"
            "Q1 | . | is the rival real? | high | C1\n\n"
            "## §D DIFF\nrun | date | delta | verdict | cost\n\n"
            "## §M METER\nfixed: -\n\n"
            "## §B BUGS\nid | date | cause | fix->invariant\n")
        old = parse(legacy)
        oc = old["claims"][0]
        assert oc["id"] == "C1" and oc["load_bearing"] is True, oc
        assert oc["claim"] == "rivals bundle the feature free", oc          # NOT shifted
        assert oc["source"] == "example.com", oc
        assert oc["seen"] == "2026-07-21", oc
        assert oc["cls"] == "-", oc                                # absent -> unclassified
        assert old["opens"][0]["question"] == "is the rival real?", old["opens"]
        assert old["opens"][0]["closed_by"] == "-", old["opens"]
        # ...and one mutation upgrades the file to the current schema in place
        set_claim(legacy, "C1", cls="world")
        assert "id | st | cls | claim" in legacy.read_text(encoding="utf-8")
        assert parse(legacy)["claims"][0]["claim"] == "rivals bundle the feature free"

        # --- V10: claim class + the derived demand flag --------------------
        # so far every claim is unclassified -> no customer claim exists yet.
        ds = demand_status(parse(path))
        # 4 claims exist but C3 is refuted, and a refuted claim is not an
        # outstanding classification debt -> 3, not 4.
        assert ds["total"] == 0 and ds["unclassified"] == 3, ds
        assert "demand-UNTESTED" in ds["flag"], ds
        assert "demand-UNTESTED" in path.read_text(encoding="utf-8"), "flag must reach §T"

        set_claim(path, "C1", cls="world")
        set_claim(path, "C2", cls="customer")          # reachable warm: A, unsourced
        cid5 = add_claim(path, "users will pay for the pro tier", st="A",
                          conf=0.3, source="-", cls="customer")
        assert cid5 == "C5", cid5
        ds = demand_status(parse(path))
        assert ds["total"] == 2 and ds["verified"] == 0 and ds["unvalidated"] is True, ds
        assert "demand-UNVALIDATED" in ds["flag"] and "C2,C5" in ds["flag"], ds
        # the flag is DERIVED: hand-deleting it from §T must not survive a write.
        stripped = path.read_text(encoding="utf-8").replace(f" · ⚠ {ds['flag']}", "")
        _atomic_write(path, stripped)
        assert "demand-UNVALIDATED" not in path.read_text(encoding="utf-8")
        set_claim(path, "C5", conf=0.31)               # any mutation re-derives it
        assert "demand-UNVALIDATED" in path.read_text(encoding="utf-8"), \
            "V10 flag must be recomputed on write, not stored"

        # V10 typed evidence: free text can NOT verify a customer claim...
        try:
            set_claim(path, "C5", st="V", source="3 booked walkthroughs 2026-07-30")
            raise AssertionError("V10: free-text source must not verify a customer claim")
        except ValueError:
            pass
        try:
            add_claim(path, "another buyer claim", st="V", conf=0.6,
                      source="press release", cls="customer")
            raise AssertionError("V10 must guard add_claim too")
        except ValueError:
            pass
        # ...a TYPED buyer interaction does
        set_claim(path, "C5", st="V",
                  source="buyer:call 3 booked walkthroughs 2026-07-30")

        # V15 ladder: confidence is CAPPED by the evidence tier
        set_claim(path, "C5", conf=0.9)   # call tier caps at 0.65
        assert abs(parse(path)["claims"][4]["conf"] - 0.65) < 1e-9, \
            parse(path)["claims"][4]
        cid6 = add_claim(path, "waitlist demand is real", "V", 0.8,
                         source="buyer:signup 214 waitlist joins, CPL $1.40",
                         cls="customer")
        c6 = next(c for c in parse(path)["claims"] if c["id"] == cid6.rstrip("*"))
        assert abs(c6["conf"] - 0.40) < 1e-9, c6   # signup tier caps at 0.40
        set_claim(path, cid6, st="A", source="-", cls="world")  # neutral reset
        # (world, so downstream customer-count asserts stay undisturbed)
        ds = demand_status(parse(path))
        assert ds["verified"] == 1 and ds["unvalidated"] is False and ds["flag"] is None, ds
        set_claim(path, "C5", st="A", source="-")      # put it back for later asserts

        # refuted customer claims are neither support nor an open assumption
        set_claim(path, "C5", st="R", source="a killed claim")
        assert demand_status(parse(path))["total"] == 1
        set_claim(path, "C5", st="A", source="-")

        try:
            add_claim(path, "bad class", st="A", conf=0.1, cls="market")
            raise AssertionError("cls must reject an unknown class")
        except ValueError:
            pass

        # §Q closed_by: the link that separates evidence from a guess
        doc_q = parse(path)
        doc_q["opens"] = [{"id": "Q1", "st": ".", "question": "unit economics?",
                            "blast": "med", "cites": "-", "closed_by": "-"}]
        _write(path, doc_q)
        assert set_open(path, "Q1", st="x", closed_by="C4") is True
        assert parse(path)["opens"][0]["closed_by"] == "C4"

        # --- V16 retro: the thesis scores its own record --------------------
        rdoc = parse(path)
        rr = retro_report(rdoc, today="2026-07-24")
        assert rr["claims"] == len(rdoc["claims"]) and rr["runs"] == 2, rr
        assert rr["refuted"] >= 1 and rr["verified"] >= 1, rr
        assert rr["refutation_rate"] is not None and rr["calibration_gap"] is not None, rr
        assert rr["days_since_buyer_evidence"] is None, "no buyer evidence yet"
        txt = render_retro(rr)
        assert "RETRO" in txt and "verdict history" in txt, txt
        assert "only ever been desk-checked" in txt, txt

        # --- staleness: an untested flip must be LOUD, not merely recorded --
        sdoc = parse(path)
        sdoc["flips"] = [
            {"id": "F1", "condition": "a rival ships the same artifact -> no-go",
             "last_checked": "2026-07-23", "holds": "n"},
            {"id": "F2", "condition": "8+ warm intros book a demo -> go",
             "last_checked": "2026-07-21", "holds": "untested"},
            {"id": "F3", "condition": "an enforcement action lands -> stronger go",
             "last_checked": "2026-07-01", "holds": "n"},
        ]
        sdoc["opens"] = [
            {"id": "Q1", "st": ".", "question": "raw practitioner voice?",
             "blast": "high", "cites": "-", "closed_by": "-"},
            {"id": "Q2", "st": "x", "question": "answered already",
             "blast": "high", "cites": "-", "closed_by": "C1"},
        ]
        _write(path, sdoc)
        rep = stale_report(parse(path), days=7, today="2026-07-24")
        # F2 has never been tested -> its own bucket, regardless of age
        assert [f["id"] for f in rep["never_checked"]] == ["F2"], rep["never_checked"]
        assert rep["never_checked"][0]["age"] == 3, rep["never_checked"]
        # F3 checked 23d ago is stale; F1 checked yesterday is not
        assert [f["id"] for f in rep["stale_flips"]] == ["F3"], rep["stale_flips"]
        # only OPEN high-blast questions surface; the answered one does not
        assert [q["id"] for q in rep["open_high"]] == ["Q1"], rep["open_high"]
        # load-bearing claims age; non-load-bearing and refuted ones are ignored
        assert all(c["id"] == "C1" for c in rep["stale_claims"]), rep["stale_claims"]
        assert rep["any"] is True
        text = render_stale(rep)
        assert "F2 NEVER TESTED" in text and "8+ warm intros book a demo" in text, text
        assert "F3 last checked 23d ago" in text, text

        # a thesis with everything freshly checked and demand verified is quiet
        qdoc = parse(path)
        qdoc["flips"] = [{"id": "F1", "condition": "c", "last_checked": "2026-07-24",
                           "holds": "n"}]
        qdoc["opens"] = []
        for c in qdoc["claims"]:
            c["seen"] = "2026-07-24"
            if c["cls"] == "customer":
                c["st"], c["source"] = "V", "buyer:call 3 booked walkthroughs"
        _write(path, qdoc)
        quiet = stale_report(parse(path), days=7, today="2026-07-24")
        assert quiet["any"] is False, quiet
        assert "nothing stale" in render_stale(quiet)

        # compact() is a no-op under the line budget.
        report = compact(path)
        assert report["compacted"] is False

        # force compaction: pad SS D past MAX_LINES, confirm oldest-first drop.
        doc2 = parse(path)
        for i in range(3, 520):
            doc2["diffs"].append({"run": i, "date": "2026-07-24",
                                   "delta": "pad", "verdict": "reshape", "cost": "0"})
        _write(path, doc2)
        before = len(parse(path)["diffs"])
        report2 = compact(path)
        assert report2["compacted"] is True
        assert report2["dropped"] > 0
        assert report2["lines_after"] <= MAX_LINES

        after_doc = parse(path)
        assert len(after_doc["diffs"]) == before - report2["dropped"]
        # runs were contiguous 1..519 -> oldest-first drop means the new
        # first row's run number equals exactly how many were dropped + 1.
        assert after_doc["diffs"][0]["run"] == 1 + report2["dropped"]
        assert any(b["cause"].startswith("file") for b in after_doc["bugs"])

        print("PASS: ledger.py self-test "
              "(round-trip, V2 guard, pipe-escape, compact) OK")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="ledger.py",
        description="deterministic bookkeeping for a /rnd thesis file",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="print/write a fresh thesis template")
    p_new.add_argument("slug")
    p_new.add_argument("title")
    p_new.add_argument("--out", help="write to this path instead of stdout")
    p_new.set_defaults(func=_cli_new)

    p_show = sub.add_parser("show", help="parse a thesis file, print a summary")
    p_show.add_argument("path")
    p_show.set_defaults(func=_cli_show)

    p_add = sub.add_parser("add-claim", help="append a claim")
    p_add.add_argument("path")
    p_add.add_argument("claim")
    p_add.add_argument("--st", required=True, help="V/A/R/O")
    p_add.add_argument("--conf", type=float, default=None)
    p_add.add_argument("--falsifier", default=None)
    p_add.add_argument("--source", default=None)
    p_add.add_argument("--cls", default=None, help="world/customer/internal")
    p_add.add_argument("--load-bearing", action="store_true")
    p_add.add_argument("--seen", default=None)
    p_add.set_defaults(func=_cli_add_claim)

    p_setc = sub.add_parser("set-claim", help="revise a claim (only passed fields change)")
    p_setc.add_argument("path")
    p_setc.add_argument("cid")
    p_setc.add_argument("--st", default=None)
    p_setc.add_argument("--conf", type=float, default=None)
    p_setc.add_argument("--falsifier", default=None)
    p_setc.add_argument("--source", default=None)
    p_setc.add_argument("--claim", default=None)
    p_setc.add_argument("--cls", default=None)
    p_setc.add_argument("--load-bearing", action=argparse.BooleanOptionalAction,
                        default=None)
    p_setc.set_defaults(func=_cli_set_claim)

    p_seto = sub.add_parser("set-open", help="update an open question")
    p_seto.add_argument("path")
    p_seto.add_argument("qid")
    p_seto.add_argument("--st", default=None, help="'.'/'~'/'x'")
    p_seto.add_argument("--question", default=None)
    p_seto.add_argument("--blast", default=None)
    p_seto.add_argument("--cites", default=None)
    p_seto.add_argument("--closed-by", default=None,
                        help="claim id that answered it (ALWAYS set when st=x)")
    p_seto.set_defaults(func=_cli_set_open)

    p_setf = sub.add_parser("set-flip", help="stamp a flip re-check")
    p_setf.add_argument("path")
    p_setf.add_argument("fid")
    p_setf.add_argument("--last-checked", default=None)
    p_setf.add_argument("--holds", default=None, help="y/n/untested")
    p_setf.add_argument("--condition", default=None)
    p_setf.set_defaults(func=_cli_set_flip)

    p_setv = sub.add_parser("set-verdict", help="rewrite the verdict")
    p_setv.add_argument("path")
    p_setv.add_argument("verdict", help="go/reshape/no-go")
    p_setv.add_argument("--conf", type=float, required=True)
    p_setv.add_argument("--run", type=int, required=True)
    p_setv.add_argument("--date", required=True)
    p_setv.add_argument("--one-line", required=True)
    p_setv.set_defaults(func=_cli_set_verdict)

    p_diff = sub.add_parser("append-diff", help="append one run row to the diff log")
    p_diff.add_argument("path")
    p_diff.add_argument("--run", type=int, required=True)
    p_diff.add_argument("--date", required=True)
    p_diff.add_argument("--delta", required=True)
    p_diff.add_argument("--verdict", required=True)
    p_diff.add_argument("--cost", required=True)
    p_diff.set_defaults(func=_cli_append_diff)

    p_comp = sub.add_parser("compact", help="enforce the 500-line one-file rule")
    p_comp.add_argument("path")
    p_comp.set_defaults(func=_cli_compact)

    p_demo = sub.add_parser("demo", help="30-second live demo of the demand stamp")
    p_demo.add_argument("--dir", default=None,
                        help="write the demo thesis here instead of a temp dir")
    p_demo.set_defaults(func=_cli_demo)

    p_stale = sub.add_parser(
        "stale", help="what has gone unexamined (untested flips, aged load-bearing "
                      "claims, high-blast open questions, unvalidated demand)")
    p_stale.add_argument("path", nargs="?", help="a thesis file")
    p_stale.add_argument("--dir", default=None,
                          help="scan every .md thesis in this folder instead")
    p_stale.add_argument("--days", type=int, default=7)
    p_stale.add_argument("--today", default=None, help="override today (YYYY-MM-DD)")
    p_stale.set_defaults(func=_cli_stale)

    p_retro = sub.add_parser(
        "retro", help="score the thesis's OWN track record: calibration, "
                      "refutation rate, verdict stability, untested flips, "
                      "and how long since real buyer evidence")
    p_retro.add_argument("path", nargs="?")
    p_retro.add_argument("--dir", default=None)
    p_retro.add_argument("--today", default=None, help="override today (YYYY-MM-DD)")
    p_retro.set_defaults(func=_cli_retro)

    p_test = sub.add_parser("selftest", help="run the built-in self-test")
    p_test.set_defaults(func=lambda a: (_selftest(), 0)[1])

    args = ap.parse_args()
    try:
        return args.func(args)
    except ValueError as e:
        # a guard refusal (V2/V10/cls) is an ANSWER, not a crash: say it plainly
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    fix_console_encoding()
    sys.exit(main())
