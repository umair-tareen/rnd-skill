# Contributing

The highest-value contribution to this repo is a **refutation**. The whole
premise is that being corrected early is the win, so use the "Refute a claim"
issue template if you can break anything we assert: a novelty claim, a
benchmark result, an invariant, a number. Refuted claims go into the ledger
with your issue as the source; they are never silently deleted (invariant V4).

## Ground rules (the same ones the tool enforces)

- **No URL, no claim.** Assertions in PRs and issues carry sources.
- **No rules in prose.** If your change adds a rule, it ships with the code
  or test that enforces it. This repo's most repeated defect - four times -
  was a rule that lived only in documentation (SPEC §B: B1, B4, B6).
- **The suite must stay green**, including `tools/test_fixture.py`, which
  parses a committed artifact your change did not create. If you change the
  schema, the fixture test failing is the system working - update the fixture
  in the same PR and say why.
- **Benchmarks are pre-registered.** If you improve a scorer, the old one
  stays in the repo and your results are labelled post-hoc against any runs
  that predate your rule (see score2.py vs score3.py for the pattern).
- **A broken invariant gets a §B row.** Cause, fix, and the invariant it
  earned. The bug log is the product; do not be shy about adding to it.

## Cheap ways in

- Run the cold-operator path (README quickstart, no help) and file exactly
  where it broke.
- Add a benchmark dossier with harder traps - the current corpus is too easy
  for modern models, and both published nulls say so.
- Port `SKILL.md` to another agent runtime; the tools are runtime-agnostic.

## Self-tests

```
python tools/ledger.py selftest
python tools/squeeze.py --selftest
python tools/trim.py --self-test
python tools/state.py --self-test
python tools/test_fixture.py
python tools/test_server.py   # needs: pip install mcp
```
