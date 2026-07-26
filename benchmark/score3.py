"""score3.py -- v2 scoring with ONE disclosed correction. Does not replace
score2.py; both stay in the repo so the delta is auditable.

THE DEFECT (found after the v2 run, disclosed rather than silently patched):
score2._ledger_units built each scoring unit as `claim + " " + source`, while
the weak and strong arms used claim text only. The T3 (unknowable) rule asks
"is a digit asserted?" - so a ledger claim citing `01-market.md;02-demand.md`
tripped it on the FILENAMES. All three ledger T3 "errors" in v2 are that: the
scorer penalised the ledger arm for citing its sources, which is the behaviour
the tool exists to enforce. Proof, from d3-ledger:

    claim : "No document in this corpus states a warranty return rate figure"
    source: "01-market.md;02-demand.md;03-technical.md"   <- the digits

The correction: ledger units are claim text ONLY, identical to the other arms.
The source field is still read for the buyer:-tag check, where it belongs.

PREREGISTRATION-v2.md says a wrong rule "ships as v3 with the flaw disclosed,
never as a silent retune." This is that. v2's as-measured numbers remain
published in RESULTS-v2.md; v3's numbers are labelled post-hoc throughout.
No marker list is changed. No run is re-executed - same committed outputs.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import score2  # noqa: E402


def _ledger_units_fixed(path):
    """Claim text only - symmetric with the weak and strong arms."""
    import ledger
    doc = ledger.parse(path)
    return [c["claim"] for c in doc["claims"]], doc


score2._ledger_units = _ledger_units_fixed
score = score2.score


if __name__ == "__main__":
    import argparse
    import json
    ap = argparse.ArgumentParser(description="v2 scoring, unit asymmetry corrected (v3)")
    ap.add_argument("output")
    ap.add_argument("key")
    ap.add_argument("--arm", choices=["weak", "strong", "ledger"], required=True)
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(json.dumps(score(a.output, a.key, a.arm), indent=2))
