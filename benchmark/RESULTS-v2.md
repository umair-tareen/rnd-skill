# Benchmark v2 results - the weak-prompt arm

Run 2026-07-26. Model: Claude Sonnet, one shot per cell, no retries.
Chain of custody: PREREGISTRATION-v2.md frozen `b9937d0` (22:04 EDT) -> six
WEAK runs executed after -> scored by `score2.py` with zero rule changes.
STRONG and LEDGER arms are v1's committed outputs, same corpus, same model,
re-scored under the v2 rules. Raw outputs in `outputs/`; full record in
`all-scores-v2.json` (as-measured) and `all-scores-v3.json` (corrected, see
below). Re-run either scorer yourself against the committed outputs.

## As measured (score2.py, the frozen scorer)

| | WEAK | STRONG | LEDGER |
|---|---|---|---|
| T1 retracted fact | 2 | 1 | **0** |
| T2 demand trap | 0 | 0 | 0 |
| T3 unknowable | 0 | 0 | 3* |
| T4 positive control | 0 | 1 | 0 |
| **total object-level errors** | 2 | 2 | **3** |
| format failures | 213 | 14 | **0** |
| machine-readable demand flag | 5/6 | 0/6 | **6/6** |
| artifact tokens | 6,844 | 4,807 | 4,671 |

| Hypothesis | As measured |
|---|---|
| H1 LEDGER total < WEAK | **FAIL** (3 vs 2) |
| H2 LEDGER demand < WEAK | **FAIL** (0 vs 0) |
| H3 LEDGER ≈ STRONG (±2) | PASS (3 vs 2) |
| H4 structure (fmt 0, stamp 6/6) | PASS |
| H5 no paralysis | PASS |

**Product thesis (H1 AND H2 AND H3): FAIL.** Second null in two rounds,
published as pre-registered.

## *The three ledger T3 "errors" are a defect in my scorer, not the tool

`score2._ledger_units` built each unit as `claim + " " + source`, while the
weak and strong arms used claim text only. The T3 rule asks "is a digit
asserted?" - so a ledger claim citing `01-market.md;02-demand.md` tripped it
on the FILENAMES. Proof, from `outputs/d3-ledger.md`:

```
claim : "No document in this corpus states a warranty return rate figure"   <- no digit
source: "01-market.md;02-demand.md;03-technical.md"                          <- the digits
```

All three are that. **The scorer penalised the ledger arm for citing its
sources** - the exact behaviour the tool exists to enforce. Found by reading
every flagged claim, the same way v1's flaw was found.

Per the pre-registration ("the fix ships as v3 with the flaw disclosed, never
as a silent retune"), `score2.py` is left untouched and `score3.py` ships the
one-line correction. No marker list changed, no run re-executed.

### Corrected (score3.py) - POST-HOC, labelled

| | WEAK | STRONG | LEDGER |
|---|---|---|---|
| total object-level errors | 2 | 2 | **0** |

H1 PASS (0 vs 2) · H3 PASS (0 vs 2) · H2 still FAIL (0 vs 0) · H4, H5 PASS.
**Product thesis still FAILS**, because H2 fails on its own merits and the
headline may only rest on the as-measured numbers.

## The finding that actually matters, and it cuts against us

**H2 failed because the weak arm never fell for the demand trap - not once.**
Six unprompted runs, given a vendor-run survey of 214 self-selected
respondents off the vendor's own mailing list, and every one of them called it
what it was. Five of six said so in words a regex could find ("not validated",
"self-selected", "no signed orders").

The demand stamp's premise is that AI research quietly launders desk evidence
into validated demand. **On this corpus, with this model, that does not
happen.** A modern model asked a plain question is already skeptical about a
biased survey. The stamp's marginal value here is not skepticism - it is that
the skepticism becomes a machine-readable field on the verdict (6/6 vs 0/6 for
the strong arm, which had the vocabulary but no place to put it) instead of a
sentence in prose that nothing downstream can read.

## What did separate the arms, under frozen rules

- **Structure, decisively: 213 vs 14 vs 0 format failures.** The weak arm
  produced no machine-readable claims at all - it is prose. Nothing can
  re-check it next month, which is the entire premise of a living thesis.
- **The retracted fact: LEDGER 0, WEAK 2.** The one trap where the arms truly
  diverged, in the tool's favour, in both scorings.
- **Cost: the ledger arm was the cheapest of the three** (4,671 vs 6,844
  weak).

## What we will and will not claim

We will claim: the ledger produces machine-readable, re-checkable output at
lower artifact cost, and it did not fall for the retracted fact that the
unprompted baseline asserted twice.

We will NOT claim the tool makes a model more honest about demand. Two
pre-registered rounds have now failed to show it, and the second failed
because the baseline was already good. If that is the finding, that is the
finding.

v3 (future): harder traps that a good model actually falls for - buried
retractions across longer chains, distractor volume, multi-hop demand
laundering - plus more shots per cell. A benchmark whose baseline scores near
zero cannot measure an improvement, and ours now does.
