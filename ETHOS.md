# Ethos

What this repo believes. Structure borrowed from
[gstack](https://github.com/garrytan/gstack) - principles belong in one
canonical place, not scattered where they drift. Content deliberately
inverted: gstack's ethos asserts compression multipliers and "the
engineering barrier is gone." Those may be true; we have no evidence for
them, and a verification tool shipping unverified claims about verification
is self-refuting.

So this file follows its own rule 5: **no belief here is only a belief.**
Each one names the code or test that enforces it. A principle with an empty
right-hand column would be prose, and prose is what this repo keeps getting
burned by.

| # | The belief | What enforces it |
|---|---|---|
| 1 | **The model is already smart; durability is the problem.** Three pre-registered benchmarks failed to show our enforcement makes a model more honest in the moment. What it cannot do alone is stay current: prose re-narrates history, a ledger re-checks the delta. | `benchmark/RESULTS*.md` (three published nulls) · measured 0.54x update cost, 0 format failures vs 213 |
| 2 | **A claim without a source is an assumption.** Not a style note - a write-time refusal. | V2 · `ledger.add_claim` / `set_claim` guards · selftest |
| 3 | **Desk research can never validate demand.** Claims are classed by what could settle them; customer claims verify only on typed buyer evidence, confidence capped by rung. A hot waitlist is real signal and is not revenue. | V10, V15 · `BUYER_EVIDENCE_CAPS` · `_clamp_customer_conf` · selftest (0.9 clamps to 0.65) |
| 4 | **Tamper-evident, not a lie detector.** The stamp enforces that the buyer question is ASKED in a checkable form, never that the answer is true. | `demand_status` derived on every write · selftest strips it and asserts it returns |
| 5 | **No rule may live only in prose.** This repo's most repeated defect, five times over. | V14 · `tools/test_fixture.py` in CI · CONTRIBUTING |
| 6 | **A self-test that round-trips through its own writer is blind.** Verify against at least one artifact this process did not create. | SPEC §B B6 · `test_fixture.py` parses committed `examples/acme` |
| 7 | **Pre-register the bar; publish the null.** When a metric turns out wrong, ship the corrected scorer BESIDE the original and label the new numbers post-hoc. Never re-headline. | 3 × `PREREGISTRATION*.md` · `score2.py` + `score3.py` kept side by side · `FUNNEL-PREREGISTRATION.md` |
| 8 | **Degrade, don't die.** Limits and failures are the environment. An interrupted move is REDONE, never skipped; a degraded run is labelled. | V12 · `state.py` (WIP/FAILED are not settled) · selftest kills mid-move and resumes cold |
| 9 | **Score yourself, not just the world.** A ledger that re-checks the world every run and never re-checks its own record has a hole where its thesis lives. | V16 · `ledger.py retro` (calibration, verdict stability, days since real buyer evidence) |
| 10 | **The verdict is advice; the last inch is human.** This tool drafts, investigates, records. It never posts, charges, deploys, or publishes. | V7 · advice-only walls in `SKILL.md` · every distribution channel we hit gated on a human, by design |

If you find a row whose right-hand column is weaker than its left, that is a
bug - open a [refutation](.github/ISSUE_TEMPLATE/refute-a-claim.yml).
