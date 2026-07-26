"""score_drift.py -- v3 scorer: did the assessment change when the world did?

Implements PREREGISTRATION-v3.md. Reuses score3's unit extraction and
object/meta classifier verbatim (ledger units = claim text only; prose units
= sentences). Checks per dossier:

  U1 figure-currency: some unit asserts the NEW audited figure (token match,
     OBJECT-level).
  U2 demand-currency: some unit asserts the signed orders (token match,
     OBJECT-level). Ledger arm additionally reports:
       - stamp_present: the derived demand warning still on the verdict line
         (correct answer after doc 05: ABSENT)
       - buyer_tag_legit: every customer claim carrying a buyer: tag cites
         the orders token that actually exists in the corpus

Usage:
  python score_drift.py <output> <key.json> --arm prose|ledger
  python score_drift.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import score3  # noqa: E402  (brings the corrected ledger units + classifier)
import score2  # noqa: E402

_BUYER_TAG_RE = score2._BUYER_TAG_RE
_DEMAND_WARN_RE = score2._DEMAND_WARN_RE


def _units(path, arm):
    raw = Path(path).read_text(encoding="utf-8")
    if arm == "ledger":
        units, doc = score2._ledger_units(path)  # patched by score3 import
        return raw, units, doc
    text = re.sub(r"\s+", " ", raw)
    return raw, [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", text) if s.strip()], None


def score(output_path, key_path, arm) -> dict:
    key = json.loads(Path(key_path).read_text(encoding="utf-8"))
    drift = key["drift"]
    raw, units, doc = _units(output_path, arm)

    # TWO PRE-SCORING REFINEMENTS, both caught by this scorer's own selftest
    # failing on its gold case BEFORE any real v3 output was scored (the
    # discipline v2 taught: a metric that cannot recognise its own ideal
    # answer must not run):
    # 1. Ledger presence checks search claim+source - the citation channel is
    #    the source field by design (buyer:signature order batch ...). A
    #    presence check widened this way cannot create a false error; it is
    #    the inverse of v2's digit-in-filename defect.
    # 2. The object/meta classifier runs on the CLAIM TEXT alone for the
    #    ledger arm: source strings are citations by definition, and the v2
    #    marker list ("per ", "vendor") would tag every well-cited claim META
    #    and block its pass. Prose has no separate citation channel, so its
    #    sentences classify as-is - a disclosed asymmetry that, if it biases
    #    anything, biases AGAINST the prose arm's opponent being flattered:
    #    every prose U-failure is read and reported individually.
    if arm == "ledger" and doc:
        pairs = [(c["claim"], f"{c['claim']} {c.get('source', '')}")
                 for c in doc["claims"]]
    else:
        pairs = [(u, u) for u in units]

    def object_hit(token):
        tok = re.compile(re.escape(token), re.I)
        hits = [cls_text for cls_text, search_text in pairs
                if tok.search(search_text)]
        objs = [t for t in hits if score2.classify(t, "drift") == "OBJECT"]
        return hits, objs

    u1_hits, u1_obj = object_hit(drift["U1_new_figure"])
    u2_hits, u2_obj = object_hit(drift["U2_orders"])

    out = {
        "output": str(output_path), "arm": arm, "product": key["product"],
        "U1_pass": bool(u1_obj), "U1_mentions": len(u1_hits),
        "U2_pass": bool(u2_obj), "U2_mentions": len(u2_hits),
        "artifact_tokens": math.ceil(len(raw) / 4),
        "parseable": None, "stamp_present": None, "buyer_tag_legit": None,
    }

    if arm == "ledger":
        out["parseable"] = doc is not None and len(doc["claims"]) > 0
        out["stamp_present"] = bool(
            _DEMAND_WARN_RE.search(
                next((l for l in raw.splitlines() if l.startswith("verdict:")), "")))
        tagged = [c for c in (doc["claims"] if doc else [])
                  if c.get("cls") == "customer"
                  and _BUYER_TAG_RE.search(str(c.get("source", "")))]
        orders_tok = re.compile(re.escape(drift["U2_orders"]), re.I)
        out["buyer_tag_legit"] = (bool(tagged) and all(
            orders_tok.search(str(c.get("source", "")) + " " + c.get("claim", ""))
            for c in tagged))
    return out


def _selftest() -> int:
    import tempfile
    key = {"product": "Veltrix",
           "drift": {"U1_new_figure": "1.7M requests/sec",
                     "U1_old_figure": "2.4M requests/sec",
                     "U2_orders": "order batch VX-P12"}}
    with tempfile.TemporaryDirectory() as tmp:
        kp = Path(tmp) / "k.json"
        kp.write_text(json.dumps(key), encoding="utf-8")

        good = Path(tmp) / "good.md"
        good.write_text(
            "The audited figure is 1.7M requests/sec, adopted in spec rev 5. "
            "Demand is now backed by order batch VX-P12 with executed signatures.",
            encoding="utf-8")
        r = score(good, kp, "prose")
        assert r["U1_pass"] and r["U2_pass"], r

        stale = Path(tmp) / "stale.md"
        stale.write_text(
            "The 2.4M figure was retracted and no updated figure exists. "
            "Demand remains unvalidated; the survey was self-selected.",
            encoding="utf-8")
        r = score(stale, kp, "prose")
        assert not r["U1_pass"] and not r["U2_pass"], r

        # ledger: stamp cleared by a legit tag citing the real orders token
        import ledger
        tp = Path(tmp) / "t.md"
        ledger._atomic_write(tp, ledger.new("t", "T"))
        ledger.add_claim(str(tp), "audited figure is 1.7M requests/sec", "V", 0.8,
                         source="05-three-weeks-later.md", cls="world")
        ledger.add_claim(str(tp), "demand validated by signed pilots", "V", 0.8,
                         source="buyer:signature order batch VX-P12 per 05",
                         cls="customer")
        r = score(str(tp), str(kp), "ledger")
        assert r["U1_pass"] and r["U2_pass"] and r["parseable"], r
        assert r["stamp_present"] is False, r
        assert r["buyer_tag_legit"] is True, r

        # a fabricated tag (does not cite the orders) is flagged illegitimate
        ledger.add_claim(str(tp), "more buyers exist", "V", 0.6,
                         source="buyer:call two mystery teams", cls="customer")
        r = score(str(tp), str(kp), "ledger")
        assert r["buyer_tag_legit"] is False, r

        print("PASS: score_drift self-test (currency both ways, stamp clear, "
              "legit-vs-fabricated tag)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("output", nargs="?")
    ap.add_argument("key", nargs="?")
    ap.add_argument("--arm", choices=["prose", "ledger"])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not (a.output and a.key and a.arm):
        ap.error("output, key, --arm required (or --selftest)")
    print(json.dumps(score(a.output, a.key, a.arm), indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
