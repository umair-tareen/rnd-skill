# Benchmark v3 pre-registration - the drift benchmark

Registered 2026-07-26, BEFORE any v3 run. Frozen as of the commit adding this
file and the `corpus/d*/05-three-weeks-later.md` deltas. Results publish in
`RESULTS-v3-drift.md` regardless of outcome.

## Why v3 measures a different axis

v1 and v2 both returned nulls, and both tested the same thing: single-run
claim discipline. The honest reading of two nulls is that a modern model is
already skeptical in the moment. But this repo's differentiator - verified
against the published landscape - was never in-the-moment discipline. It is
TEMPORAL: a thesis whose falsifiers are re-checked across runs, whose verdict
cannot silently rot, and whose update costs a fraction of a rewrite. Neither
prior round touched that axis. v3 does: **the world changes between run 1 and
run 2; does the assessment change with it, and at what cost?**

This is also the demand stamp's first TRUE-POSITIVE test. v1/v2 only ever
tested that the stamp resists false validation. In v3, real buyer evidence
finally arrives in the corpus - the correct behaviour is for the stamp to
CLEAR.

## The world-change (per dossier, uniform, disclosed)

Each dossier gains ONE new document, `05-three-weeks-later.md`, containing:

- **CH1 - the retraction is superseded.** An independent audit publishes a
  REVISED, verified figure (a new unique token per dossier). Run-1's correct
  conclusion ("the figure was retracted") is now itself stale. Parroting the
  retraction is the drift failure this measures.
- **CH2 - buyer evidence arrives.** Signed pilot orders are documented
  (unique token per dossier). Demand moves from unvalidated to validated by
  real buyer commitment. Not noticing is a drift failure; for the ledger arm,
  the derived demand stamp should clear via a legitimate `buyer:signature`
  source.
- **CH3 - a distractor** (cosmetic vendor news) to prevent "everything
  changed" heuristics. Not scored; present for realism.

## Arms (both start from COMMITTED run-1 artifacts in `outputs/`)

- **PROSE-UPDATE (6 runs):** the agent gets its arm's prior assessment
  (`dN-weak.md`) plus the dossier including doc 05: "Three weeks later there
  are new documents. Update your assessment." Output: updated prose.
- **LEDGER-RECHECK (6 runs):** the agent gets the prior thesis
  (`dN-ledger.md`) plus the dossier including doc 05, and runs the recheck
  loop through `ledger.py` CLI (set-claim / add-claim / set-verdict). Output:
  the updated thesis file.

Same model tier (Claude Sonnet), one shot per cell, no retries.

## Scoring (mechanical; object/meta classifier from score3 reused verbatim)

Per dossier, two update checks:
- **U1 figure-currency:** the final output asserts the NEW audited figure
  (token match, OBJECT-level) - and does not assert the old retracted state
  as current. Miss = parroting the stale retraction with no mention of the
  revision.
- **U2 demand-currency:** the final output reflects validated demand (OBJECT-
  level assertion of the signed orders token). Ledger arm additionally: the
  `buyer:` tag present is now LEGITIMATE (doc 05 documents signatures) and
  the derived stamp must be GONE from the verdict line.

Plus, per arm: update artifact tokens (chars/4 proxy, unit disclosed as
always), machine-parseability of the updated output, and for the ledger arm
the stamp state.

## Pre-registered bar

- **H1 (drift):** LEDGER U1+U2 catches >= PROSE U1+U2 (out of 12 each).
- **H2 (cost of staying current):** LEDGER update artifact tokens < PROSE
  update artifact tokens, summed over 6 dossiers.
- **H3 (the stamp's true-positive):** stamp cleared on >= 5/6 ledger updates
  WITHOUT any fabricated evidence (the buyer: source must reference the doc-05
  orders, which now exist).
- **H4 (structure holds under update):** updated ledger files all parse
  (`ledger.parse`, 0 failures); updated prose remains structurally unparseable
  (expected, reported not judged).

PASS for the temporal thesis = H1 AND H2 AND H3. Any FAIL publishes as
measured. If PROSE matches LEDGER on drift at similar cost, the honest
headline is "re-prompting is enough on this corpus" and that is what ships.

## Disclosed limits

Same author-written corpus; uniform change-shape across dossiers (varied
tokens only); one model tier; one shot per cell; artifact-token proxy for
cost. The prior artifacts are committed and public (`outputs/`), so the run-1
starting points are auditable and were produced BEFORE this pre-registration
existed - they cannot have been tuned for v3.
