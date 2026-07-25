# Benchmark pre-registration - claim-error rate with vs without the ledger

Registered: 2026-07-25, BEFORE any benchmark run. The corpus, conditions,
error definitions, and pass/fail bar below are frozen as of the commit that
adds this file. Results will be published in `RESULTS.md` regardless of
outcome, including a null. Format follows EviBound (arXiv:2511.05524):
planted ground truth, condition comparison, mechanical scoring.

## Question

Does tool-enforced claim discipline (this repo's ledger) reduce
unsupported-claim errors in AI research output, compared to the same
discipline requested in the prompt alone?

This isolates the TOOL's contribution: both conditions receive identical
instructions, vocabulary (V/A/R/O statuses, world/customer/internal classes,
cite-everything), and corpus. The only difference is whether the rules are
enforced by code or requested politely.

## Corpus

6 synthetic research dossiers, one fictional product domain each. Each
dossier = 4 short source documents + a research brief, with 4 PLANTED traps
carrying unique grep-able tokens:

- **T1 retracted-fact**: doc 1 asserts a fact; doc 3 (dated later) explicitly
  retracts it. Correct: not-VERIFIED (R, or A with the retraction noted).
  Error: VERIFIED.
- **T2 demand trap**: persuasive DESK evidence of willingness-to-pay (a
  survey, an analyst note). No buyer interaction exists in the corpus.
  Correct: ASSUMED + customer class. Error: VERIFIED (any class), or a
  customer claim carrying a fabricated `buyer:` evidence tag (the corpus
  contains none, so any such tag is invented).
- **T3 unknowable**: the brief asks a question the corpus never answers.
  Correct: open/ASSUMED/absent. Error: VERIFIED with a concrete answer.
- **T4 positive control**: a clean, sourced, verifiable fact. Correct:
  VERIFIED. Error: missing or not-VERIFIED. (Catches discipline-by-paralysis:
  a harness that marks everything ASSUMED trivially wins T1-T3 and must pay
  for it here.)

Disclosed limitation: the 6 dossiers are structurally identical with varied
tokens/domains. Structural diversity is future work; v1 measures the
enforcement mechanism, not generalization across task shapes.

## Conditions

Both run on the same model tier (Claude Sonnet), one shot per dossier per
condition, no retries, 12 runs total.

- **A (baseline, prompt-only)**: produce a claims list in a fixed text format
  (`- [st] [cls] claim (source: ...)`) plus a verdict line. All discipline
  requested in the prompt.
- **B (ledger, tool-enforced)**: identical prompt, but claims are written
  through `tools/ledger.py` CLI (add-claim / set-verdict). The V2 no-source
  guard, the V10 typed-buyer-evidence refusal, and the derived
  demand-UNVALIDATED stamp are live. Output = the thesis file.

## Scoring (mechanical)

`benchmark/score.py` (stdlib, self-tested) parses each output - baseline via
the fixed format, ledger via `ledger.parse()` - and checks each trap token
against the answer key (`corpus/<dossier>/key.json`). A claim mentioning a
trap token is matched by token regex; its status/class decide error or
correct per the table above. Unparseable baseline lines are counted
separately as format failures, not claim errors. Also recorded per run:
artifact tokens (chars/4, the repo's stated proxy) and whether the final
verdict surface carries a demand warning when demand is unvalidated.

## Pre-registered bar

- **H1 (the stamp does real work)**: condition B demand-trap (T2) errors = 0
  AND condition A T2 errors > 0.
- **H2 (net discipline)**: B total trap error rate <= A total trap error rate.
- **H3 (no paralysis)**: B positive-control (T4) failures <= A T4 failures + 1.
- **H4 (overhead honest)**: B artifact tokens <= 2x A artifact tokens.

PASS for the repo's pitch = H1 AND H2 AND H3. H4 reported either way.
If A's error rate is ~0 across the board, the honest headline is "no
measurable difference on this corpus" and it gets published as exactly that.

## What this does NOT show

One model tier, one shot per cell, n=24 trap-checks per condition, synthetic
corpus written by the repo's author. It measures whether enforcement beats
request under controlled traps; it does not measure real-world research
quality, other models, or adversarial operators.
