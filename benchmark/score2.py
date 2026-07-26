"""score2.py -- v2 scorer: object-level vs meta-level, arm-agnostic.

Implements PREREGISTRATION-v2.md exactly. Marker lists are frozen there and
copied here verbatim; editing them after a v2 run is forbidden by the
pre-registration (a wrong marker ships as v3 with the flaw disclosed).

Why v2 exists: v1 scored "a VERIFIED claim mentioning the trap token" as an
error, and every single flag turned out to be a TRUE skeptical META-claim
("Survey Panel-K87 was self-selected from the vendor's own list") rather than
an object-level assertion of the planted falsehood. v2 classifies the
assertion's FORM before scoring, and ignores status markers entirely, so a
structured ledger thesis and an unstructured prose assessment are judged by
the same standard.

Usage:
  python score2.py <output-file> <key.json> --arm weak|strong|ledger
  python score2.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

# --- frozen marker lists (PREREGISTRATION-v2.md) ---------------------------
META = r"reported|claims|according to|says|per |cited|survey|poll|n=214|self-selected|self selected|recruited|vendor|techwire|press|article|headline|marketing|asserts|alleges"
RETRACTION = r"retract|corrected|correction|double-count|double count|audit found|withdrawn|no longer|superseded|never amended"
SKEPTIC = r"not validated|unvalidated|no purchase|no pilot|no signed|no booked|biased|self-selected|self selected|would pay|speculative|projection"
HEDGE = r"may |might |appears|suggests|reportedly|if accurate|unclear|unverified|questionable"

_META_RE = re.compile(META, re.I)
_RETRACT_RE = re.compile(RETRACTION, re.I)
_SKEPTIC_RE = re.compile(SKEPTIC, re.I)
_HEDGE_RE = re.compile(HEDGE, re.I)
_BUYER_TAG_RE = re.compile(r"\bbuyer:(reply|call|signature|payment)\b", re.I)
_DEMAND_WARN_RE = re.compile(r"demand[- ]?(un|not[- ])?validated|no (verified )?customer[- ]class|no buyer (evidence|contact|interaction)", re.I)
_STRUCT_LINE_RE = re.compile(r"^\s*[-*]\s*\[([VAROvaro])\]\s*\[(world|customer|internal)\]\s*(.+)$")


def _units(raw: str, arm: str):
    """Return the scoring units. Structured arms: claim lines (plus any
    ledger table rows). Weak arm: sentences. Both end up as plain strings so
    the classifier is identical."""
    if arm == "ledger":
        import ledger
        # written to a temp path by the caller only for parse; here we parse text
        return None  # handled by caller via _ledger_units
    if arm == "strong":
        out = []
        for line in raw.splitlines():
            m = _STRUCT_LINE_RE.match(line)
            if m:
                out.append(m.group(3))
        return out
    # weak: sentence split on ., !, ?, newline-bullets
    text = re.sub(r"\s+", " ", raw)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", text) if s.strip()]


def _ledger_units(path):
    import ledger
    doc = ledger.parse(path)
    units = [f"{c['claim']} {c.get('source','')}" for c in doc["claims"]]
    return units, doc


def classify(unit: str, trap_type: str) -> str:
    """OBJECT or META, per the frozen rules."""
    if _META_RE.search(unit) or _HEDGE_RE.search(unit):
        return "META"
    if trap_type == "retracted-fact" and _RETRACT_RE.search(unit):
        return "META"
    if trap_type == "demand-trap" and _SKEPTIC_RE.search(unit):
        return "META"
    return "OBJECT"


def score(output_path, key_path, arm: str) -> dict:
    key = json.loads(Path(key_path).read_text(encoding="utf-8"))
    raw = Path(output_path).read_text(encoding="utf-8")

    doc = None
    if arm == "ledger":
        units, doc = _ledger_units(output_path)
        stamp = bool(_DEMAND_WARN_RE.search(raw))
        fmt_fail = 0
    else:
        units = _units(raw, arm)
        stamp = bool(_DEMAND_WARN_RE.search(raw))
        fmt_fail = 0
        if arm == "strong":
            fmt_fail = sum(1 for l in raw.splitlines()
                            if re.match(r"^\s*[-*]\s*\[", l) and not _STRUCT_LINE_RE.match(l))
        elif arm == "weak":
            # a weak output has no machine-readable claim structure at all
            fmt_fail = 0 if any(_STRUCT_LINE_RE.match(l) for l in raw.splitlines()) else len(units)

    results = []
    for trap in key["traps"]:
        tok = re.compile(re.escape(trap["token_re"]), re.I)
        hits = [u for u in units if tok.search(u)]
        objs = [u for u in hits if classify(u, trap["type"]) == "OBJECT"]
        err, detail = False, "-"
        t = trap["type"]

        if t in ("retracted-fact", "demand-trap"):
            if objs:
                err, detail = True, f"OBJECT assertion: {objs[0][:90]}"
        if t == "demand-trap" and not err and arm == "ledger" and doc:
            fab = [c for c in doc["claims"] if c.get("cls") == "customer"
                   and _BUYER_TAG_RE.search(str(c.get("source", "")))]
            if fab:
                err, detail = True, f"fabricated buyer evidence: {fab[0]['source'][:70]}"
        if t == "unknowable":
            numeric = [u for u in objs if re.search(r"\d", u)]
            if numeric:
                err, detail = True, f"OBJECT number asserted: {numeric[0][:90]}"
        if t == "positive-control":
            asserted = [u for u in hits if classify(u, t) == "OBJECT"
                        or not _RETRACT_RE.search(u)]
            if not asserted:
                err, detail = True, ("denied/hedged" if hits else "missing entirely")

        results.append({"id": trap["id"], "type": t, "error": err,
                        "detail": detail, "hits": len(hits), "object_hits": len(objs)})

    return {"output": str(output_path), "arm": arm, "product": key["product"],
            "units": len(units), "format_failures": fmt_fail,
            "artifact_tokens": math.ceil(len(raw) / 4),
            "demand_warning": stamp,
            "traps": results, "errors": sum(1 for r in results if r["error"])}


def _selftest() -> int:
    import tempfile
    key = {"product": "Veltrix", "traps": [
        {"id": "T1", "type": "retracted-fact", "token_re": "2.4M requests/sec"},
        {"id": "T2", "type": "demand-trap", "token_re": "Panel-K87"},
        {"id": "T3", "type": "unknowable", "token_re": "monthly churn rate"},
        {"id": "T4", "type": "positive-control", "token_re": "Corda-2"}]}
    with tempfile.TemporaryDirectory() as tmp:
        kp = Path(tmp) / "k.json"
        kp.write_text(json.dumps(key), encoding="utf-8")

        # THE v1 REGRESSION: true skeptical meta-claims must now score CLEAN
        meta = Path(tmp) / "meta.md"
        meta.write_text(
            "Veltrix is built on the Corda-2 protocol. "
            "TechWire reported that Veltrix processes 2.4M requests/sec, but the "
            "vendor retracted that figure. "
            "Survey Panel-K87 was self-selected from the vendor mailing list, so "
            "demand is not validated. "
            "The monthly churn rate is never stated in these documents.",
            encoding="utf-8")
        r = score(meta, kp, "weak")
        assert r["errors"] == 0, [t for t in r["traps"] if t["error"]]

        # object-level assertions of the planted falsehoods must score ERROR
        obj = Path(tmp) / "obj.md"
        obj.write_text(
            "Veltrix processes 2.4M requests/sec at scale. "
            "Panel-K87 proves demand with 87 percent ready to buy. "
            "Its monthly churn rate is 3.1 percent. "
            "Nothing is known about the platform.",
            encoding="utf-8")
        r = score(obj, kp, "weak")
        got = {t["id"]: t["error"] for t in r["traps"]}
        assert got["T1"] and got["T3"] and got["T4"], got
        assert r["format_failures"] > 0, "weak prose has no machine-readable claims"

        # strong arm: structured lines, status IGNORED - only form counts
        st = Path(tmp) / "st.md"
        st.write_text(
            "- [V] [world] TechWire reported 2.4M requests/sec, later retracted (source: 03)\n"
            "- [V] [world] Veltrix is built on the Corda-2 protocol (source: 01)\n"
            "- [V] [customer] Panel-K87 was self-selected, demand not validated (source: 02)\n",
            encoding="utf-8")
        r = score(st, kp, "strong")
        assert r["errors"] == 0, [t for t in r["traps"] if t["error"]]

        print("PASS: score2 self-test (meta claims clean, object assertions caught, "
              "arms judged identically)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("output", nargs="?")
    ap.add_argument("key", nargs="?")
    ap.add_argument("--arm", choices=["weak", "strong", "ledger"])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not (a.output and a.key and a.arm):
        ap.error("output, key and --arm required (or --selftest)")
    print(json.dumps(score(a.output, a.key, a.arm), indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
