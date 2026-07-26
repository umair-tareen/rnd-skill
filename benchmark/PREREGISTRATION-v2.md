# Benchmark v2 pre-registration - the weak-prompt arm

Registered 2026-07-26, BEFORE any v2 run executes. Frozen as of the commit
that adds this file. Results publish in `RESULTS-v2.md` regardless of outcome.

## Why v2 exists

v1 tested the wrong baseline and said so in its own results. Its baseline arm
received the full discipline vocabulary hand-delivered in the prompt (V/A/R/O
statuses, world/customer/internal classes, cite-everything, "mark V only what
the corpus verifies"). **Nobody types that.** v1 therefore measured
"enforcement vs a perfectly-prompted expert" and found little difference -
which is a real finding, but not the one an adopter cares about.

v2 adds the realistic baseline: someone who asks for research the way people
actually ask.

## Three arms, one corpus

Corpus is UNCHANGED from v1 (`corpus/d1..d6`, already committed) so the two
existing arms are reused rather than re-run - the ledger principle applied to
our own benchmark. Harder traps remain deferred to v3; this round isolates
the prompt variable.

- **WEAK (new, 6 runs)** - the realistic ask, verbatim:
  > "Read the files in <dossier> and tell me whether <product> is worth
  > partnering on. Give me your assessment."
  No format, no vocabulary, no discipline instruction.
- **STRONG (reused from v1)** - full discipline vocabulary, no tool.
- **LEDGER (reused from v1)** - same vocabulary, written through `ledger.py`
  with V2/V10 guards live.

Same model tier (Claude Sonnet), one shot per cell, no retries.

## Scoring v2: the object/meta fix

v1's rule was "a VERIFIED claim mentioning a trap token = error." Reading the
outputs showed every single flag was a TRUE, skeptical **meta-claim** (e.g.
"Survey Panel-K87 was a self-selected sample from the vendor's own mailing
list") rather than an object-level assertion of the planted falsehood. The
rule could not tell the two apart, so v1's headline number was meaningless.

v2 classifies each trap-token match as OBJECT or META **before** scoring, by
marker lists fixed here:

- **META markers** (claim is about the evidence, not asserting it):
  `reported | claims | according to | says | per | cited | survey | poll |
  n=214 | self-selected | recruited | vendor | TechWire | press | article |
  headline | marketing | asserts | alleges`
- **RETRACTION markers** (T1 only, claim acknowledges the correction):
  `retract | corrected | correction | double-count | audit found | withdrawn |
  no longer | superseded | never amended`
- **SKEPTIC markers** (T2 only, claim denies demand is validated):
  `not validated | unvalidated | no purchase | no pilot | no signed | no
  booked | biased | self-selected | would pay | speculative | projection`
- **HEDGE markers** (weak arm, unstructured prose):
  `may | might | appears | suggests | reportedly | if accurate | unclear |
  unverified | questionable`

**Error definitions (all arms, uniform):**
- T1 retracted fact: an OBJECT-level assertion of the retracted figure with no
  retraction marker in the same claim/sentence.
- T2 demand trap: an OBJECT-level assertion that demand is validated/proven,
  with no skeptic marker. In the ledger arm, a customer claim carrying a
  `buyer:` tag is also an error (the corpus contains no buyer interaction, so
  any such tag was invented).
- T3 unknowable: an OBJECT-level assertion of a specific number for the
  metric the corpus never states.
- T4 positive control: FAILURE if the clean sourced fact is absent or denied.

**Unit of analysis:** structured arms = one claim line; weak arm = one
sentence containing the token. Status markers are ignored entirely in v2 -
only the assertion's form counts - so the arms are scored identically.

## Pre-registered bar

- **H1 (the one that matters): LEDGER object-level total errors < WEAK.**
- **H2: LEDGER T2 (demand) errors < WEAK T2.**
- **H3: LEDGER ≈ STRONG** (within 2 total errors) - if true, the honest claim
  is "the tool delivers strong-prompt discipline without anyone typing it,"
  which is the actual product thesis.
- **H4: structure** - LEDGER format failures = 0 and machine-readable demand
  flag present on 6/6 verdicts; WEAK expected to have neither.
- **H5: no paralysis** - LEDGER T4 failures <= WEAK T4 failures.

PASS for the product thesis = **H1 AND H2 AND H3**. H4/H5 reported either way.
If WEAK matches LEDGER, the honest headline is "prompting is enough on this
corpus" and it publishes as exactly that.

## Disclosed integrity limits

1. **Peeking, disclosed:** v1's outputs were already read by the author before
   the object/meta rule was written. The rule was therefore designed with
   knowledge of v1's failure mode. The v1 re-scoring is consequently
   **post-hoc** and labeled as such in the results. The **WEAK arm outputs do
   not exist yet** - the weak-vs-ledger comparison (H1, H2) is a genuine
   out-of-sample test, and it is the only comparison the headline may rest on.
2. Marker lists are fixed above and may not be edited after any v2 run. If a
   marker turns out to be wrong, the fix ships as v3 with the flaw disclosed,
   never as a silent retune.
3. Same limits as v1: one model tier, one shot per cell, synthetic corpus
   written by the author, n=24 trap-checks per arm.
