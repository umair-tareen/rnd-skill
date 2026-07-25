# Benchmark results - published as pre-registered, including the part that failed

Run: 2026-07-25. Model: Claude Sonnet, one shot per cell, no retries.
Chain of custody: pre-registration frozen `1ba25ae` (13:25 EDT) -> corpus
committed `339ce91` (13:27) -> scorer committed `23f7af5` (13:28) -> all 12
runs executed after -> scored by `score.py` with zero rule changes.
Raw outputs are committed under `outputs/`; `all-scores.json` is the full
mechanical scoring record. Re-run scoring yourself:
`python benchmark/score.py outputs/d1-ledger.md corpus/d1/key.json --mode ledger`

## The pre-registered bar, applied verbatim

| Hypothesis | Result | Numbers |
|---|---|---|
| H1: ledger demand-trap errors = 0 AND baseline's > 0 | **FAIL** | B.T2=6, A.T2=5 |
| H2: ledger total errors <= baseline | PASS | 7 vs 8 |
| H3: no discipline-by-paralysis (positive control) | PASS | B.T4=0, A.T4=1 |
| H4: overhead <= 2x | PASS | **0.97x** (4,671 vs 4,807 artifact tokens) |

**Overall (H1 AND H2 AND H3): FAIL.** The headline claim - that enforcement
reduces claim errors versus the same discipline merely requested - is NOT
supported on this corpus. We wrote in the pre-registration that a null gets
published as exactly that, so here it is.

## What the "errors" actually were (and why the null is informative)

Reading the 15 flagged claims (all committed in `outputs/`): **not one of
them, in either condition, asserts a planted falsehood.** Every T2 flag has
the shape "Survey Panel-K87 was a self-selected sample from the vendor's own
mailing list" marked VERIFIED - a TRUE, sourced, skeptical claim ABOUT the
evidence, matched by the trap token. Both T1 flags on "TechWire reported X"
are the same: accurate meta-claims about the reporting, not endorsements of
the retracted figure. The frozen scoring rule ("V + token = error") cannot
distinguish object-level claims (X is true) from meta-claims (source S says
X, and S is biased) - a limitation we disclose rather than patch after the
fact, and one that hit both conditions symmetrically, so the comparison
stayed fair.

The honest reading: **a well-prompted Sonnet with this vocabulary is already
skeptically disciplined on a 4-document corpus.** Neither condition verified
the retracted figure, invented the unknowable number, or called demand
proven. The traps were not hard enough to separate enforcement from request
at the object level - that is a fact about the corpus difficulty as much as
about the tool, and v2 needs harder traps (longer evidence chains, buried
retractions, distractor volume) plus an object/meta claim distinction in
scoring.

## What DID separate the conditions (frozen rules, no reinterpretation)

| Measure | baseline | ledger |
|---|---|---|
| Format failures (claim lines that failed to parse) | **14** | **0** |
| Machine-readable demand warning on the verdict | **0/6** | 3/6 as-scored* |
| Positive control dropped (real fact missing/downgraded) | 1 | 0 |
| Fabricated `buyer:` evidence to defeat the refusal | n/a | **0** |
| Artifact tokens | 4,807 | 4,671 |

*Post-hoc note (not pre-registered, labeled as such): the frozen scorer
grepped only `demand-UNVALIDATED`. The other 3 ledger runs carry the sibling
derived flag ("no customer-class claim exists yet" / refuted-demand states) -
a machine-derived demand statement is present on **6/6** ledger verdicts and
**0/6** baseline verdicts. We report the as-scored 3/6 in the table and this
correction beside it rather than silently rescoring.

Also observed in run logs: the d2 ledger agent hit the V2 no-source guard
(an unsourced claim silently requested as load-bearing), was downgraded to
ASSUMED by the tool, and recorded it honestly instead of inventing a source -
the enforcement behaving exactly as designed, at a moment no scorer was
watching.

## Conclusion we will actually stand behind

On this corpus, the ledger's measured value is **structure, not error-rate**:
outputs that always parse (14 vs 0 format failures), a demand flag that is
machine-derived on every verdict rather than left to prose, refusals that get
obeyed rather than gamed, and all of it at slightly LESS artifact cost than
freeform output (0.97x). The error-rate claim - the one skeptics most want -
remains **unproven**, and this repo will not cite this benchmark as if it
proved it. What "the skill is the prompt" is worth remains real but
unmeasured here: the baseline received the full discipline vocabulary
hand-delivered, which is precisely what nobody types by hand in real use.

v2, if run: harder traps, object/meta scoring distinction, a weak-prompt arm
(no discipline vocabulary - the realistic baseline), more shots per cell.
