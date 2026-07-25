"""trim.py -- /rnd run cost meter (ported from ai-trim, github.com/skibidiskib/ai-trim).

Why: the thesis-ledger's whole pitch (SPEC sec G) is that run N costs a
FRACTION of run 1. This is the meter that PROVES it. Ported 1:1 from
ai-trim's token/pricing model (chars-per-token estimator + per-model
$/token), re-pointed at a /rnd run's own file split instead of a coding
agent's tooling tax:
  - MARGINAL ("on-demand"): the run folder's .md files -- new research
    done THIS run.
  - FIXED ("always-loaded"): the thesis file (if given) -- the ledger
    that gets re-read whole every run (SPEC sec I.2 step 1).
Emits the SPEC's "sec M METER" block, and if the thesis's sec D DIFF log
already has a run 1 row, prints the run1-vs-runN delta + a trim
recommendation string.

Usage:
    python trim.py <run_folder> [--thesis <thesis.md>] [--model opus]
    python trim.py runs/acme-2026-07-21 --thesis theses/acme.md

Self-test: python trim.py --self-test
    Builds a temp run folder + fake thesis, measures it, asserts the
    numbers and the rendered block make sense. Prints PASS/raises on FAIL.
"""
import argparse
import datetime
import math
import re
import sys
import tempfile
from pathlib import Path

# --- ai-trim constants (ported EXACTLY from src/ai-trim.ts) -----------------
CHARS_PER_TOKEN = 4
PRICING = {
    "opus": 0.000015,
    "sonnet": 0.000003,
    "haiku": 0.0000008,
}

# dirs a walk never descends into (ai-trim's skipDirs, plus repo norms)
SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".venv"}


def estimate_tokens(text: str) -> int:
    """ai-trim's estimator, ported exactly: ceil(chars / CHARS_PER_TOKEN)."""
    if not text:
        return 0
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def estimate_file_tokens(path: Path) -> int:
    """Read a file and estimate its tokens. Unreadable/missing -> 0 tokens,
    matching ai-trim's fail-open behavior (a try/catch returning 0)."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="cp1252", errors="replace")
        except OSError:
            return 0
    except OSError:
        return 0
    return estimate_tokens(text)


def cost_usd(tokens: int, model: str) -> float:
    """tokens * $/token for `model`; unknown model falls back to opus,
    matching ai-trim's `PRICING[model] || PRICING.opus`."""
    rate = PRICING.get(model, PRICING["opus"])
    return tokens * rate


def format_cost(tokens: int, model: str) -> str:
    """Estimate string. Deliberately imprecise: the underlying number is a
    chars/4 proxy times a blended input rate, so four decimal places would be
    false precision wearing a currency sign."""
    cost = cost_usd(tokens, model)
    if cost < 0.01:
        return "<$0.01 est."
    return f"~${cost:.2f} est."


def format_tokens(n: int) -> str:
    return f"{n:,}"


def _walk_md_files(folder: Path):
    """Recursively yield .md files under folder, skipping SKIP_DIRS and any
    hidden (dot-prefixed) subdirectory."""
    folder = Path(folder)
    if not folder.exists():
        return
    for p in sorted(folder.rglob("*.md")):
        if not p.is_file():
            continue
        rel_parts = p.relative_to(folder).parts[:-1]  # dirs only, not the filename
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel_parts):
            continue
        yield p


def _since_epoch(since):
    """'2026-07-23' -> epoch seconds at local midnight. None/garbage -> None."""
    try:
        return datetime.datetime.fromisoformat(str(since).strip()).timestamp()
    except (ValueError, TypeError):
        return None


def _mtime_date(path: Path) -> str:
    """File mtime as YYYY-MM-DD (for the stale-folder warning). '' on error."""
    try:
        return datetime.date.fromtimestamp(Path(path).stat().st_mtime).isoformat()
    except OSError:
        return ""


def measure_run(run_folder, thesis_file=None, model: str = "opus", since=None) -> dict:
    """Measure ONE /rnd run's token + $ cost, split fixed vs marginal.

    UNIT: written-artifact tokens (chars/4) -- what the run WROTE, a size
    proxy. It does not observe API calls, subagent context, fetches, or
    reasoning tokens. Honest as a floor and a trend, wrong as a bill.

    fixed (always-loaded)  = thesis_file, if given -- the ledger re-read
                              that happens EVERY run regardless of what's new.
    marginal (on-demand)   = the .md files under run_folder written by THIS
                              run -- the new research this run produced.

    `since` ('YYYY-MM-DD') filters marginal by mtime, so a recheck run that
    shares an earlier run's folder is not charged for that run's briefs.
    Excluded files are reported under `stale` (never silently dropped: a
    silent drop would understate cost exactly as counting them overstates it).

    Never raises on a missing run_folder/thesis_file (treated as 0 tokens),
    so measuring a first-ever run (no thesis yet) still works cleanly.
    """
    run_folder = Path(run_folder)
    cutoff = _since_epoch(since)
    marginal_files = []
    stale_files = []
    for f in _walk_md_files(run_folder):
        entry = {"path": str(f), "tokens": estimate_file_tokens(f), "mtime": _mtime_date(f)}
        if cutoff is not None:
            try:
                is_stale = f.stat().st_mtime < cutoff
            except OSError:
                is_stale = False
            if is_stale:
                stale_files.append(entry)
                continue
        marginal_files.append(entry)
    marginal_tokens = sum(f["tokens"] for f in marginal_files)

    fixed_tokens = 0
    fixed_path = None
    if thesis_file:
        fixed_path = Path(thesis_file)
        fixed_tokens = estimate_file_tokens(fixed_path)

    total_tokens = fixed_tokens + marginal_tokens

    return {
        "run_folder": str(run_folder),
        "thesis_file": str(fixed_path) if fixed_path else None,
        "model": model,
        "since": since,
        "fixed": {
            "tokens": fixed_tokens,
            "usd": cost_usd(fixed_tokens, model),
            "file": str(fixed_path) if fixed_path else None,
        },
        "marginal": {
            "tokens": marginal_tokens,
            "usd": cost_usd(marginal_tokens, model),
            "files": marginal_files,
        },
        "stale": {
            "tokens": sum(f["tokens"] for f in stale_files),
            "files": stale_files,
        },
        "total": {
            "tokens": total_tokens,
            "usd": cost_usd(total_tokens, model),
        },
    }


def stale_folder_warning(measurement: dict, diff_rows=None):
    """Catch the operator trap this meter exists to avoid: pointing run N at
    run 1's folder, so run 1's briefs get re-charged as run N's marginal and
    the meter reports ~100% of run1 instead of the real fraction.

    Fires only when no --since was given AND every marginal file predates the
    latest sec D run date. Returns a warning string, or None when clean.
    """
    if measurement.get("since"):
        return None
    files = measurement["marginal"]["files"]
    rows = [r for r in (diff_rows or []) if r.get("date")]
    if not files or not rows:
        return None
    last = max(rows, key=lambda r: r["run"])
    last_date = re.search(r"(\d{4}-\d{2}-\d{2})", last["date"])
    if not last_date:
        return None
    last_date = last_date.group(1)
    newest = max((f.get("mtime") or "") for f in files)
    if newest and newest < last_date:
        return (f"warning: newest file here is {newest}, older than run {last['run']} "
                f"({last_date}). This looks like an EARLIER run's folder, so its briefs "
                f"are being charged as this run's marginal cost. Give run N its own "
                f"folder, or pass --since {last_date}.")
    return None


# --- sec D DIFF log parsing (for the run1-vs-runN delta) --------------------
# Row shape per SPEC sec I.1: `run | date | delta | verdict | cost`
_ROW_RE = re.compile(r"^\s*(\d+)\s*\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|\s*(.+?)\s*$")
_COST_TOK_RE = re.compile(r"([\d,]+\.?\d*)\s*([kKmM]?)\s*tok", re.IGNORECASE)
_COST_USD_RE = re.compile(r"\$([\d,]+\.?\d*)")


def _parse_cost_cell(cell: str):
    """'165k tok / $2.10' -> (165000, 2.10). '22000 tok / $0.33' also works.
    Missing pieces come back as None rather than raising."""
    tok = None
    usd = None
    m = _COST_TOK_RE.search(cell)
    if m:
        num = float(m.group(1).replace(",", ""))
        mult = {"k": 1_000, "m": 1_000_000, "": 1}[m.group(2).lower()]
        tok = int(num * mult)
    m = _COST_USD_RE.search(cell)
    if m:
        usd = float(m.group(1).replace(",", ""))
    return tok, usd


def parse_diff_log(thesis_text: str):
    """Pull sec D DIFF rows out of a thesis file's markdown.
    Returns a list of dicts oldest-first; [] if there's no sec D section
    yet (i.e. this really is run 1 -- nothing to compare against)."""
    if not thesis_text:
        return []
    m = re.search(r"\xa7D[^\n]*", thesis_text)  # \xa7 == '§'
    if not m:
        return []
    section = thesis_text[m.end():]
    nxt = re.search(r"\n\s*\xa7[A-Z]", section)  # stop at next § heading
    if nxt:
        section = section[:nxt.start()]

    rows = []
    for line in section.splitlines():
        rm = _ROW_RE.match(line)
        if not rm:
            continue
        run_no = rm.group(1)
        if not run_no.isdigit():
            continue
        cost_tok, cost_usd_val = _parse_cost_cell(rm.group(5))
        rows.append({
            "run": int(run_no),
            "date": rm.group(2).strip(),
            "delta": rm.group(3).strip(),
            "verdict": rm.group(4).strip(),
            "cost_tokens": cost_tok,
            "cost_usd": cost_usd_val,
        })
    return rows


def trim_recommendation(fixed_tokens: int, run1_tokens, current_tokens: int) -> str:
    """SPEC's trim rec: is the landscape stable enough to go recheck-only
    next time, or does it still need fresh research spend?"""
    if not run1_tokens:
        return "no prior run in \xa7D yet -- this IS run 1 (nothing to trim against)."
    ratio = current_tokens / run1_tokens if run1_tokens else 1.0
    if ratio <= 0.5:
        projected_k = max(1, round(fixed_tokens / 1000))
        return f"landscape stable -> next run recheck-only ~{projected_k}k tokens"
    return (f"landscape still moving ({ratio * 100:.0f}% of run1 cost) -> "
            f"keep researching open \xa7Q before trusting recheck-only")


# --- YIELD: what the run BOUGHT (the counterweight to cost) -----------------
# Why this exists: a cost meter alone rewards spending less, and the cheapest
# possible run answers nothing. Reported next to sec M, "5.3% of run 1" stops
# being a boast and becomes a ratio you can audit: 5% of the cost for WHAT?
try:  # sibling import, resilient to being run from any cwd
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ledger as _ledger
    from ledger import fix_console_encoding as _fix_console_encoding
except Exception:  # pragma: no cover - yield degrades, cost meter still works
    _ledger = None

    def _fix_console_encoding():
        pass

_ISO_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _iso(s):
    m = _ISO_RE.search(str(s or ""))
    return m.group(1) if m else None


def measure_yield(thesis_file, run=None) -> dict:
    """What did run N actually ADD to the thesis?

    Attributes claims to a run by `seen` date falling in that run's window
    [run_N.date, run_N+1.date), open-ended for the latest run, so a run that
    spans two days is still counted correctly.

    Reports claims added by state and class, mean confidence, load-bearing
    count, and -- the metric that matters -- how many open questions were
    closed on EVIDENCE (a verified claim) versus closed on an ASSUMPTION.
    Once a question's status flips to 'x' those look identical; only the
    closed_by link tells them apart.
    """
    out = {"available": False, "reason": None, "run": run}
    if _ledger is None:
        out["reason"] = "ledger.py not importable"
        return out
    try:
        doc = _ledger.parse(thesis_file)
    except Exception as e:
        out["reason"] = f"could not parse thesis: {e}"
        return out

    diffs = [d for d in doc.get("diffs") or [] if isinstance(d.get("run"), int)]
    if not diffs:
        out["reason"] = "no sec D run rows yet"
        return out
    diffs.sort(key=lambda d: d["run"])
    target = (max(diffs, key=lambda d: d["run"]) if run is None
              else next((d for d in diffs if d["run"] == run), None))
    if target is None:
        out["reason"] = f"run {run} not found in sec D"
        return out

    start = _iso(target["date"])
    if not start:
        out["reason"] = f"run {target['run']} has a non-ISO date ({target['date']!r})"
        return out
    later = [_iso(d["date"]) for d in diffs if d["run"] > target["run"]]
    end = min([d for d in later if d], default=None)

    def in_window(seen):
        s = _iso(seen)
        if not s:
            return False
        return s >= start and (end is None or s < end)

    claims = doc.get("claims") or []
    added = [c for c in claims if in_window(c.get("seen"))]
    by_st, by_cls = {}, {}
    for c in added:
        by_st[c["st"]] = by_st.get(c["st"], 0) + 1
        key = c.get("cls", "-") or "-"
        by_cls[key] = by_cls.get(key, 0) + 1
    confs = [c["conf"] for c in added if c.get("conf") is not None and c["st"] != "R"]
    by_id = {c["id"]: c for c in claims}

    closed = {"evidence": [], "assumption": [], "unlinked": []}
    for q in doc.get("opens") or []:
        if (q.get("st") or "").strip() != "x":
            continue
        cid = (q.get("closed_by") or "-").strip().rstrip("*")
        src = by_id.get(cid)
        if src is None:
            closed["unlinked"].append(q["id"])
        elif not in_window(src.get("seen")):
            continue  # closed by an earlier run; not this run's yield
        elif src["st"] == "V":
            closed["evidence"].append(f"{q['id']}<-{cid}")
        else:
            closed["assumption"].append(f"{q['id']}<-{cid}")

    out.update({
        "available": True,
        "run": target["run"],
        "window": (start, end),
        "claims_added": len(added),
        "by_st": by_st,
        "by_cls": by_cls,
        "load_bearing_added": sum(1 for c in added if c.get("load_bearing")),
        "mean_conf": (sum(confs) / len(confs)) if confs else None,
        "closed": closed,
        "demand": _ledger.demand_status(doc),
    })
    return out


def render_yield(y: dict, total_tokens=None) -> str:
    """Render the sec Y YIELD block that sits under sec M."""
    if not y.get("available"):
        return f"\xa7Y YIELD\n\n(unavailable: {y.get('reason')})"

    lines = [f"\xa7Y YIELD (run {y['run']})", ""]
    st = y["by_st"]
    lines.append(
        f"claims added: {y['claims_added']} "
        f"(V={st.get('V', 0)} A={st.get('A', 0)} R={st.get('R', 0)}), "
        f"{y['load_bearing_added']} load-bearing"
    )
    mc = y["mean_conf"]
    lines.append(f"mean confidence of what it added: {mc:.2f}" if mc is not None
                 else "mean confidence of what it added: n/a")
    if y["by_cls"]:
        lines.append("by class: " + ", ".join(f"{k}={v}" for k, v in sorted(y["by_cls"].items())))

    c = y["closed"]
    parts = [f"{len(c['evidence'])} on EVIDENCE"
             + (f" [{', '.join(c['evidence'])}]" if c["evidence"] else ""),
             f"{len(c['assumption'])} on an ASSUMPTION"
             + (f" [{', '.join(c['assumption'])}]" if c["assumption"] else "")]
    if c["unlinked"]:
        parts.append(f"{len(c['unlinked'])} unlinked [{', '.join(c['unlinked'])}]")
    lines.append("questions closed: " + ", ".join(parts))

    if total_tokens:
        verified = st.get("V", 0)
        lines.append(
            f"cost per verified claim: {format_tokens(round(total_tokens / verified))} tok"
            if verified else
            f"cost per verified claim: n/a (0 verified claims for "
            f"{format_tokens(total_tokens)} tok)"
        )

    warnings = []
    if y["claims_added"] and not y["load_bearing_added"]:
        warnings.append("0 load-bearing claims added: cheap, but it moved nothing "
                        "the verdict rests on")
    if c["assumption"]:
        warnings.append(f"{len(c['assumption'])} question(s) closed on an assumption: "
                        "the cost fell partly by answering with a guess")
    if c["unlinked"]:
        warnings.append(f"{len(c['unlinked'])} answered question(s) have no closed_by "
                        "link: evidence vs guess is unauditable")
    if y["demand"].get("flag"):
        warnings.append(y["demand"]["flag"])
    for w in warnings:
        lines.append(f"  !! {w}")

    return "\n".join(lines)


# --- sec M METER rendering ---------------------------------------------------
def render_meter(measurement: dict, diff_rows=None) -> str:
    """Render the SPEC's 'sec M METER' markdown block from a measure_run() dict."""
    model = measurement["model"]
    fixed = measurement["fixed"]
    marginal = measurement["marginal"]
    total = measurement["total"]

    lines = ["\xa7M METER", ""]
    lines.append("unit: written-artifact tokens (chars/4) -- a size PROXY for "
                 "what the run wrote, NOT API spend")
    lines.append(""),
    lines.append(
        f"fixed (always-loaded, ledger re-read): "
        f"{format_tokens(fixed['tokens'])} tok / {format_cost(fixed['tokens'], model)} ({model})"
    )
    lines.append(
        f"marginal (on-demand, new research this run): "
        f"{format_tokens(marginal['tokens'])} tok / {format_cost(marginal['tokens'], model)} ({model})"
    )
    stale = measurement.get("stale") or {}
    if stale.get("files"):
        lines.append(
            f"excluded (earlier runs, before --since {measurement.get('since')}): "
            f"{format_tokens(stale['tokens'])} tok across {len(stale['files'])} file(s)"
        )
    lines.append(
        f"total: {format_tokens(total['tokens'])} tok / {format_cost(total['tokens'], model)} ({model})"
    )

    diff_rows = diff_rows or []
    warn = stale_folder_warning(measurement, diff_rows)
    if warn:
        lines.append("")
        lines.append(warn)
    run1_tokens = None
    if diff_rows:
        run1 = min(diff_rows, key=lambda r: r["run"])
        run1_tokens = run1["cost_tokens"]
        lines.append("")
        if run1_tokens:
            pct_of_run1 = (total["tokens"] / run1_tokens) * 100
            reduction = 100 - pct_of_run1
            sign = "-" if reduction >= 0 else "+"
            run1_usd = (f" / ~${run1['cost_usd']:.2f} est." if run1["cost_usd"] is not None else "")
            lines.append(f"run1 (baseline): {format_tokens(run1_tokens)} tok{run1_usd}")
            lines.append(
                f"this run:        {format_tokens(total['tokens'])} tok / "
                f"{format_cost(total['tokens'], model)}"
            )
            lines.append(
                f"delta: this run = {pct_of_run1:.1f}% of run1 cost "
                f"({sign}{abs(reduction):.1f}%)"
            )
        else:
            lines.append("run1 row found in \xa7D but its cost cell didn't parse -- no delta.")

    lines.append("")
    lines.append(f"trim: {trim_recommendation(fixed['tokens'], run1_tokens, total['tokens'])}")

    return "\n".join(lines)


# --- CLI ---------------------------------------------------------------------
def main() -> int:
    _fix_console_encoding()

    ap = argparse.ArgumentParser(
        description="Measure a /rnd run's token + $ cost (fixed vs marginal), ported from ai-trim."
    )
    ap.add_argument("run_folder", help="run scratch folder to walk for .md files (marginal/on-demand cost)")
    ap.add_argument("--thesis", default=None, help="thesis ledger .md file (fixed/always-loaded cost)")
    ap.add_argument("--model", default="opus", choices=sorted(PRICING.keys()),
                     help="pricing model for the $ estimate (default: opus)")
    ap.add_argument("--run", type=int, default=None, metavar="N",
                     help="which §D run to report YIELD for (default: the latest)")
    ap.add_argument("--no-yield", action="store_true",
                     help="cost only; skip the yield block")
    ap.add_argument("--since", default=None, metavar="YYYY-MM-DD",
                     help="count only files written on/after this date as THIS run's "
                          "marginal cost (use when a recheck run shares an earlier "
                          "run's folder; earlier files are reported as excluded)")
    args = ap.parse_args()

    if not Path(args.run_folder).exists():
        print(f"ERROR: run folder does not exist: {args.run_folder}", file=sys.stderr)
        print("A missing measurement subject must not produce a confident meter.",
              file=sys.stderr)
        return 2

    measurement = measure_run(args.run_folder, args.thesis, args.model, since=args.since)

    diff_rows = []
    if args.thesis:
        try:
            thesis_text = Path(args.thesis).read_text(encoding="utf-8")
        except OSError as e:
            print(f"warning: could not read --thesis {args.thesis!r}: {e}", file=sys.stderr)
            thesis_text = None
        if thesis_text:
            diff_rows = parse_diff_log(thesis_text)

    print(f"run folder: {measurement['run_folder']}")
    if measurement["thesis_file"]:
        print(f"thesis:     {measurement['thesis_file']}")
    print(f"model:      {measurement['model']}")
    print(f"marginal .md files scanned: {len(measurement['marginal']['files'])}")
    print()
    print(render_meter(measurement, diff_rows))
    if args.thesis and not args.no_yield:
        print()
        print(render_yield(measure_yield(args.thesis, run=args.run),
                            total_tokens=measurement["total"]["tokens"]))
    return 0


def _self_test() -> int:
    """Build a temp run folder + fake thesis, measure it, sanity-check the
    numbers and the rendered §M block. Raises AssertionError on any FAIL."""
    with tempfile.TemporaryDirectory(prefix="trim_selftest_") as tmp:
        tmp = Path(tmp)
        run_dir = tmp / "run_2026-07-23"
        run_dir.mkdir()
        (run_dir / "research1.md").write_text(
            "# Research note one\n" + ("competitive landscape scan. " * 200),
            encoding="utf-8",
        )
        (run_dir / "research2.md").write_text(
            "# Research note two\n" + ("falsifier recheck evidence. " * 150),
            encoding="utf-8",
        )
        # a file trim.py should NOT count (not .md)
        (run_dir / "notes.txt").write_text("ignore me" * 500, encoding="utf-8")

        thesis = tmp / "fake-thesis.md"
        thesis.write_text(
            "\xa7T THESIS\n"
            "verdict: reshape (conf 0.7) . as-of run 2 . 2026-07-22\n\n"
            "\xa7D DIFF\n"
            "run | date  | delta                   | verdict | cost\n"
            "1   | 07-21 | +11 claims, full sweep  | reshape | 165000 tok / $2.4750\n"
            "2   | 07-22 | C1 re-held, +Q1         | reshape | 22000 tok / $0.3300\n"
            "\n\xa7M METER\n(prior run's meter goes here)\n",
            encoding="utf-8",
        )

        measurement = measure_run(run_dir, thesis, model="opus")

        assert measurement["total"]["tokens"] > 0, "total tokens should be > 0"
        assert measurement["total"]["usd"] > 0, "total usd should be > 0"
        assert measurement["marginal"]["tokens"] > 0, "marginal tokens should be > 0 (2 .md files)"
        assert measurement["fixed"]["tokens"] > 0, "fixed tokens should be > 0 (thesis given)"
        assert len(measurement["marginal"]["files"]) == 2, (
            f"should find exactly 2 .md files (notes.txt excluded), got "
            f"{len(measurement['marginal']['files'])}"
        )

        thesis_text = thesis.read_text(encoding="utf-8")
        diff_rows = parse_diff_log(thesis_text)
        assert len(diff_rows) == 2, f"expected 2 \xa7D rows, got {len(diff_rows)}"
        assert diff_rows[0]["run"] == 1 and diff_rows[0]["cost_tokens"] == 165000, diff_rows[0]
        assert diff_rows[1]["run"] == 2 and diff_rows[1]["cost_tokens"] == 22000, diff_rows[1]

        block = render_meter(measurement, diff_rows)
        assert "\xa7M METER" in block
        assert "fixed" in block and "marginal" in block and "total" in block
        assert "trim:" in block

        # --since: an OLD brief in the same folder must not be charged to run N.
        import os as _os
        old = run_dir / "run1-old-brief.md"
        old.write_text("# run 1 brief\n" + ("stale landscape sweep. " * 400), encoding="utf-8")
        old_epoch = _since_epoch("2026-07-01")
        _os.utime(old, (old_epoch, old_epoch))

        unfiltered = measure_run(run_dir, thesis, model="opus")
        filtered = measure_run(run_dir, thesis, model="opus", since="2026-07-23")
        assert len(unfiltered["marginal"]["files"]) == 3, unfiltered["marginal"]["files"]
        assert len(filtered["marginal"]["files"]) == 2, filtered["marginal"]["files"]
        assert len(filtered["stale"]["files"]) == 1, filtered["stale"]["files"]
        assert filtered["stale"]["tokens"] > 0
        assert filtered["marginal"]["tokens"] < unfiltered["marginal"]["tokens"], (
            "--since must lower marginal cost by excluding the earlier run's brief")
        assert "excluded (earlier runs" in render_meter(filtered, diff_rows)

        # stale-folder warning: fires when EVERY marginal file predates the last §D run.
        stale_dir = tmp / "run_old_only"
        stale_dir.mkdir()
        only_old = stale_dir / "old.md"
        only_old.write_text("# only an old brief\n" + ("x" * 400), encoding="utf-8")
        _os.utime(only_old, (old_epoch, old_epoch))
        dated_rows = [{"run": 1, "date": "2026-07-21", "cost_tokens": 165000, "cost_usd": 2.47},
                      {"run": 2, "date": "2026-07-23", "cost_tokens": 22000, "cost_usd": 0.33}]
        stale_m = measure_run(stale_dir, thesis, model="opus")
        warn = stale_folder_warning(stale_m, dated_rows)
        assert warn and "EARLIER run's folder" in warn, warn
        assert "--since 2026-07-23" in warn, warn
        assert warn in render_meter(stale_m, dated_rows)
        # ...and does NOT fire once --since is supplied, or on a fresh folder.
        assert stale_folder_warning(measure_run(stale_dir, thesis, since="2026-07-23"), dated_rows) is None
        assert stale_folder_warning(measure_run(run_dir, thesis), dated_rows) is None

        # trim_recommendation branch logic, isolated
        rec_stable = trim_recommendation(1000, 165000, 5000)      # 5000/165000 ~= 3%
        assert "recheck-only" in rec_stable, rec_stable
        rec_moving = trim_recommendation(1000, 165000, 150000)   # 150000/165000 ~= 91%
        assert "keep researching" in rec_moving, rec_moving
        rec_first = trim_recommendation(1000, None, 5000)
        assert "run 1" in rec_first, rec_first

        # constants, ported EXACTLY per spec
        assert PRICING == {"opus": 0.000015, "sonnet": 0.000003, "haiku": 0.0000008}, PRICING
        assert CHARS_PER_TOKEN == 4
        assert estimate_tokens("abcd") == 1          # 4 chars -> 1 tok
        assert estimate_tokens("abcde") == 2          # ceil(5/4) == 2
        assert estimate_tokens("") == 0
        assert math.isclose(cost_usd(1_000_000, "opus"), 15.0)
        assert math.isclose(cost_usd(1_000_000, "sonnet"), 3.0)
        assert math.isclose(cost_usd(1_000_000, "haiku"), 0.8)

        # --- YIELD ---------------------------------------------------------
        # A thesis where run 2 is cheap for a BAD reason: it added one
        # unsourced claim and closed a question with it. Cost says "great",
        # yield must say "you answered that with a guess".
        y_thesis = tmp / "yield-thesis.md"
        y_thesis.write_text(
            "# THESIS: Yield\nslug: yield\ncreated: 2026-07-21\n\n"
            "## \xa7T THESIS\nverdict: reshape (conf 0.7) \xb7 as-of run 2 \xb7 2026-07-23\n"
            "one-line: t\n\n"
            "## \xa7C CLAIMS\n"
            "id | st | cls | claim | conf | falsifier | source | seen\n"
            "C1* | V | world | competitor map | 0.85 | x | src | 2026-07-21\n"
            "C2 | A | customer | firms will pay | 0.3 | x | - | 2026-07-21\n"
            "C3 | V | world | rival is thin | 0.6 | x | src2 | 2026-07-23\n"
            "C4 | A | internal | our install hours | 0.4 | x | reasoned estimate | 2026-07-24\n\n"
            "## \xa7F FLIPS\nid | if this becomes true -> verdict flips to | last-checked | holds?\n\n"
            "## \xa7Q OPEN\nid | st | question | blast | cites | closed_by\n"
            "Q1 | x | is the rival real? | high | C1 | C3\n"
            "Q2 | x | do the unit economics work? | med | - | C4\n"
            "Q3 | x | legacy answered question | low | - | -\n"
            "Q4 | . | still open | low | - | -\n\n"
            "## \xa7D DIFF\nrun | date | delta | verdict | cost\n"
            "1 | 2026-07-21 | full sweep | reshape | 25431 tok / $0.38\n"
            "2 | 2026-07-23 | recheck | reshape | 1331 tok / $0.02\n\n"
            "## \xa7M METER\nfixed: -\n\n"
            "## \xa7B BUGS\nid | date | cause | fix->invariant\n",
            encoding="utf-8")

        y2 = measure_yield(y_thesis)                      # latest run = 2
        assert y2["available"], y2
        assert y2["run"] == 2 and y2["window"] == ("2026-07-23", None), y2
        # C3 (07-23) and C4 (07-24) belong to run 2; a run spanning 2 days counts both
        assert y2["claims_added"] == 2, y2
        assert y2["load_bearing_added"] == 0, y2
        assert y2["by_cls"] == {"world": 1, "internal": 1}, y2
        assert abs(y2["mean_conf"] - 0.5) < 1e-9, y2
        assert y2["closed"]["evidence"] == ["Q1<-C3"], y2["closed"]
        assert y2["closed"]["assumption"] == ["Q2<-C4"], y2["closed"]
        assert y2["closed"]["unlinked"] == ["Q3"], y2["closed"]
        assert y2["demand"]["unvalidated"] is True, y2["demand"]

        y1 = measure_yield(y_thesis, run=1)               # window [07-21, 07-23)
        assert y1["run"] == 1 and y1["claims_added"] == 2, y1
        assert y1["load_bearing_added"] == 1, y1
        # Q1 was closed by C3, which belongs to run 2 -> not run 1's yield
        assert y1["closed"]["evidence"] == [] and y1["closed"]["assumption"] == [], y1["closed"]

        yblock = render_yield(y2, total_tokens=1331)
        for expect in ("\xa7Y YIELD (run 2)", "0 load-bearing",
                        "1 on EVIDENCE", "1 on an ASSUMPTION", "unlinked",
                        "closed on an assumption", "demand-UNVALIDATED",
                        "moved nothing"):
            assert expect in yblock, (expect, yblock)
        assert "cost per verified claim: 1,331 tok" in yblock, yblock

        assert measure_yield(tmp / "nope.md")["available"] is False
        assert measure_yield(y_thesis, run=99)["available"] is False

        print("PASS: trim.py self-test ok")
        print()
        print(block)
        print()
        print(yblock)
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        _fix_console_encoding()
        sys.exit(_self_test())
    sys.exit(main())
