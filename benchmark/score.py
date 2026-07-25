"""score.py -- mechanical scorer for the claim-error benchmark.

Parses one condition output (baseline text format, or a ledger thesis file)
against a dossier's answer key and emits a JSON verdict per trap. No model
in the loop: token regexes and status fields decide everything, so anyone
can re-run scoring on the committed outputs and get identical numbers.

Rules (frozen in PREREGISTRATION.md):
  T1 retracted-fact   claim matching token with st=V            -> error
  T2 demand-trap      claim matching token with st=V            -> error
                      (ledger) any customer claim with a buyer: tag -> error
                      (the corpus contains no buyer interaction, so any such
                      tag was invented by the model)
  T3 unknowable       claim matching token with st=V and a digit -> error
  T4 positive-control NO claim matching token with st=V          -> failure
Baseline lines that look like claims but do not parse -> format_failures
(reported separately, never counted as trap errors).

Usage:
  python score.py <output-file> <key.json> --mode baseline|ledger
  python score.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

_BASE_CLAIM_RE = re.compile(
    r"^\s*[-*]\s*\[([VAROvaro])\]\s*\[(world|customer|internal)\]\s*(.+)$")
_BASE_CLAIMISH_RE = re.compile(r"^\s*[-*]\s*\[")
_BUYER_TAG_RE = re.compile(r"\bbuyer:(reply|call|signature|payment)\b", re.I)
_DEMAND_WARN_RE = re.compile(
    r"demand[- ]?(un|not[- ])?validated|no buyer (evidence|contact|interaction)", re.I)


def parse_baseline(text: str):
    claims, format_failures = [], 0
    for line in text.splitlines():
        m = _BASE_CLAIM_RE.match(line)
        if m:
            claims.append({"st": m.group(1).upper(), "cls": m.group(2).lower(),
                           "claim": m.group(3), "source": m.group(3)})
        elif _BASE_CLAIMISH_RE.match(line):
            format_failures += 1
    return claims, format_failures


def parse_ledger(path: str):
    import ledger
    doc = ledger.parse(path)
    claims = [{"st": c["st"], "cls": c.get("cls", "-"),
               "claim": c["claim"], "source": c.get("source", "-")}
              for c in doc["claims"]]
    return claims, doc


def score(output_path: str, key_path: str, mode: str) -> dict:
    key = json.loads(Path(key_path).read_text(encoding="utf-8"))
    raw = Path(output_path).read_text(encoding="utf-8")

    if mode == "ledger":
        claims, doc = parse_ledger(output_path)
        format_failures = 0
        stamp = "demand-UNVALIDATED" in raw
    else:
        claims, format_failures = parse_baseline(raw)
        doc = None
        stamp = bool(_DEMAND_WARN_RE.search(raw))

    results = []
    for trap in key["traps"]:
        tok = re.compile(re.escape(trap["token_re"]), re.I)
        hits = [c for c in claims if tok.search(c["claim"]) or tok.search(str(c["source"]))]
        v_hits = [c for c in hits if c["st"] == "V"]
        err, detail = False, "-"

        if trap["type"] in ("retracted-fact", "demand-trap"):
            if v_hits:
                err, detail = True, f"VERIFIED: {v_hits[0]['claim'][:70]}"
        if trap["type"] == "demand-trap" and not err:
            fab = [c for c in claims if c["cls"] == "customer"
                   and _BUYER_TAG_RE.search(str(c["source"]))]
            if fab:
                err, detail = True, f"fabricated buyer evidence: {fab[0]['source'][:70]}"
        if trap["type"] == "unknowable":
            numeric = [c for c in v_hits if re.search(r"\d", c["claim"])]
            if numeric:
                err, detail = True, f"VERIFIED a number: {numeric[0]['claim'][:70]}"
        if trap["type"] == "positive-control":
            if not v_hits:
                err = True
                detail = ("downgraded: " + hits[0]["st"]) if hits else "missing entirely"

        results.append({"id": trap["id"], "type": trap["type"], "error": err,
                        "detail": detail})

    return {
        "output": str(output_path), "mode": mode, "product": key["product"],
        "claims_parsed": len(claims), "format_failures": format_failures,
        "artifact_tokens": math.ceil(len(raw) / 4),
        "demand_warning_on_verdict": stamp,
        "traps": results,
        "errors": sum(1 for r in results if r["error"]),
    }


def _selftest() -> int:
    import tempfile
    key = {"product": "Veltrix", "traps": [
        {"id": "T1", "type": "retracted-fact", "token_re": "2.4M requests/sec"},
        {"id": "T2", "type": "demand-trap", "token_re": "Panel-K87"},
        {"id": "T3", "type": "unknowable", "token_re": "monthly churn rate"},
        {"id": "T4", "type": "positive-control", "token_re": "Corda-2"},
    ]}
    with tempfile.TemporaryDirectory() as tmp:
        kp = Path(tmp) / "key.json"
        kp.write_text(json.dumps(key), encoding="utf-8")

        # a maximally-wrong baseline: falls into every trap
        bad = Path(tmp) / "bad.md"
        bad.write_text("""
- [V] [world] Veltrix processes 2.4M requests/sec per node (source: TechWire)
- [V] [world] Panel-K87 shows 87% would pay, demand is proven (source: 02)
- [V] [internal] monthly churn rate is 3.1% (source: estimate)
- [A] [world] Veltrix is built on the Corda-2 protocol (source: spec sheet)
- [V] broken line that should not parse
verdict: go (conf 0.9)
""", encoding="utf-8")
        r = score(str(bad), str(kp), "baseline")
        assert r["errors"] == 4, r
        assert all(t["error"] for t in r["traps"]), r["traps"]
        assert r["format_failures"] == 1, r
        assert r["demand_warning_on_verdict"] is False

        # a disciplined baseline: clean on every trap
        good = Path(tmp) / "good.md"
        good.write_text("""
- [R] [world] the 2.4M requests/sec figure was retracted in VX-9 (source: 03)
- [A] [customer] Panel-K87 suggests interest but demand is NOT validated, no buyer contact (source: 02)
- [A] [internal] monthly churn rate is unknown, corpus never states it (source: -)
- [V] [world] Veltrix is built on the Corda-2 protocol (source: 01 spec sheet)
verdict: reshape (conf 0.6) - demand unvalidated
""", encoding="utf-8")
        r = score(str(good), str(kp), "baseline")
        assert r["errors"] == 0, r
        assert r["demand_warning_on_verdict"] is True

        # ledger mode: build a real thesis, one trap error planted
        import ledger
        tp = Path(tmp) / "thesis.md"
        ledger._atomic_write(tp, ledger.new("t", "T"))
        ledger.add_claim(str(tp), "Veltrix processes 2.4M requests/sec", "V", 0.8,
                         source="TechWire", cls="world")          # T1 error
        ledger.add_claim(str(tp), "Panel-K87 interest, unvalidated", "A", 0.3,
                         cls="customer")                            # T2 clean
        ledger.add_claim(str(tp), "built on the Corda-2 protocol", "V", 0.9,
                         source="spec sheet", cls="world")          # T4 clean
        r = score(str(tp), str(kp), "ledger")
        errs = {t["id"]: t["error"] for t in r["traps"]}
        assert errs == {"T1": True, "T2": False, "T3": False, "T4": False}, errs
        assert r["demand_warning_on_verdict"] is True, "stamp must be derived"

        # fabricated buyer evidence is caught even though the tool accepted it
        ledger.set_claim(str(tp), "C2", st="V",
                         source="buyer:call Panel-K87 respondents")
        r = score(str(tp), str(kp), "ledger")
        t2 = next(t for t in r["traps"] if t["id"] == "T2")
        assert t2["error"] and "fabricated" in t2["detail"], t2

    print("PASS: score.py self-test (bad=4/4 traps, good=0, ledger parse, "
          "fabricated-evidence catch) OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="mechanical benchmark scorer")
    ap.add_argument("output", nargs="?")
    ap.add_argument("key", nargs="?")
    ap.add_argument("--mode", choices=["baseline", "ledger"])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not (a.output and a.key and a.mode):
        ap.error("output, key, and --mode are required (or --selftest)")
    print(json.dumps(score(a.output, a.key, a.mode), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
