# Adoption funnel pre-registration

Frozen 2026-07-26, BEFORE any distribution submission below went out. This
is the repo's own medicine applied to its own adoption claim: the thesis
"someone other than the author will use this" sits at ASSUMED (see
`research/landscape.md`), and per our evidence ladder it can only move on
typed, capped evidence. Stars and clones are signup-tier signal (conf cap
0.40); an external issue, PR, or refutation is reply-tier (cap 0.50); a
maintained external integration would be signature-tier. No amount of
traffic reaches "adoption validated" - the ladder forbids it, on purpose.

## The channels (durable first, lottery never before evidence)

Submitted/opened as of this freeze, in order:
1. gstack integration issue (garrytan/gstack) - on-topic, per their
   contributing culture; proposes the office-hours -> evidence-layer handoff
   documented in docs/USING_WITH_GSTACK.md.
2. awesome-list PRs (Claude Code / MCP server lists).
3. MCP registry listing(s) for the `rnd` server.
4. Anthropic plugin directory submission (manifest already passes
   `claude plugin validate --strict`).
No Show HN, no Reddit launch, no paid promotion inside this window - those
are lottery channels and stay gated on this test's outcome.

## The pre-registered bar (14 days from the first listing going live)

- B1: >= 30 GitHub stars
- B2: >= 50 unique cloners (GitHub traffic API)
- B3: >= 1 external issue, PR, or refutation from a non-author account

HIT (all three): adoption claim upgrades on signup/reply-tier evidence
(conf <= 0.40-0.50), and the lottery channels + creator pitches unlock.
MISS (any fails): the repo is an excellent personal tool, the flagship
investment stops, and that verdict gets published here - the same way all
three benchmark nulls were.

Numbers chosen before data existed; the GitHub traffic snapshot at freeze
is effectively zero (repo is ~30h old, unindexed at last check). Results
will be appended to this file with the raw traffic JSON committed.
