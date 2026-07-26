# THESIS: Claim-ledger tooling landscape - can rnd-skill earn adoption?
slug: landscape
created: 2026-07-25

## §T THESIS
verdict: reshape (conf 0.65) · as-of run 1 · 2026-07-25 · ⚠ demand-UNVALIDATED: 1 customer claim(s), 0 verified by buyer contact (C9)
one-line: The mechanism whitespace is real - four academic convergences, zero shipped products doing cross-run falsifier recheck - but adoption is blocked by the proof gap (no benchmark) and discovery (0 stars beside an 88k-star context-memory incumbent); path = benchmark (Q2) + cold-operator test (F2) + directory (Q1), promotion last.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1* | V | world | ResearchLoop (arXiv:2605.28282) implements a persistent claim ledger as durable repo-backed state - but its schema has NO pre-registered falsifier field and claims are NOT re-validated across runs; the recheck loop is unclaimed by it | 0.85 | a ResearchLoop release adds falsifier fields + cross-run recheck | arxiv.org/abs/2605.28282 (3-0 adversarial votes, 2026-07-25) | 2026-07-25
C2 | V | world | EviBound (arXiv:2511.05524) gates agent claims behind machine-verifiable typed evidence (queryable run IDs, artifacts) - the same refusal pattern as our buyer: tag, applied to execution artifacts, not demand | 0.8 | EviBound or a fork applies evidence gates to market/demand claims | arxiv.org/abs/2511.05524 (3-0 votes) | 2026-07-25
C3 | V | world | POPPER (snap-stanford, Candes/Leskovec, 280 stars) runs agent-designed falsification experiments with Type-I error control - single-run only: no persistent ledger, no cost meter, no demand concept in its README | 0.8 | POPPER ships persistent cross-run claim state | github.com/snap-stanford/POPPER (fetched 2026-07-25) | 2026-07-25
C4 | V | world | HDSO (arXiv:2606.22330) curates falsifiable hypotheses with validation plans for embodied agent skills (ALFWorld); approved-only repository - initial research claim that it retains rejected hypotheses was WRONG on direct fetch, and no code is released | 0.75 | HDSO code release shows a rejected-hypothesis ledger | arxiv.org/abs/2606.22330 (fetched 2026-07-25; corrects a 0-vote claim) | 2026-07-25
C5 | V | world | Agent-memory incumbents at 20-60k stars (mem0, Letta, Zep/Graphiti) store facts and context, not falsifiable claims: mem0 overwrites facts in place, Zep timestamps fact validity but has no falsifiers or demand concept | 0.7 | any of them ships claim-with-falsifier semantics | particula.tech, mcp.directory, developersdigest.tech comparisons (blog-grade; traction numbers unaudited) | 2026-07-25
C6* | V | world | claude-mem (88,534 stars, gh api 2026-07-25) owns the 'memory across sessions' perception slot in Claude Code - adopters will believe they already have what rnd-skill does unless the claim-vs-context distinction is the headline | 0.8 | cold operators asked to compare articulate the distinction unprompted | gh api repos/thedotmack/claude-mem | 2026-07-25
C7* | V | world | The official Anthropic plugin directory holds 15 external plugins and ZERO in research/memory/claims/evidence (verified by listing external_plugins directly) - a gated but open whitespace channel: solo maintainers can submit via Console; review is the moat | 0.85 | a research/claims plugin lands in the directory before ours | gh api repos/anthropics/claude-plugins-official/contents/external_plugins; claude.com/docs/plugins/submit | 2026-07-25
C8 | V | world | The skeptic bar is quantified: ~84% of developers use AI tools, ~29% trust output; comparable skill launches were attacked on validation credibility, not ignored - the demanded proof artifact is an EviBound-style benchmark (claim-error rate with vs without the ledger), which we do not have | 0.6 | a launch in this category succeeds on narrative alone in 2026 | stackoverflow.blog 2026-02-18; HN threads on comparable launches | 2026-07-25
C9 | A | customer | Someone other than the author will install and use rnd-skill | 0.3 | the pre-registered cold-operator test misses its bar | - | 2026-07-25
C10 | A | internal | A solo maintainer can sustain directory review, benchmark work, and issue support alongside a consultancy | 0.4 | first month of issues exceeds ~2h/week | - | 2026-07-25
C11* | V | world | garrytan/gstack (YC CEO, 124.4k stars, created 2026-03, pushed 2026-07-15) is the dominant adjacent toolkit: 23 skills covering Think-Plan-Build-Ship, and its /office-hours triggers on IS THIS WORTH BUILDING - our core question. Verified from skill bodies: it is a Socratic forcing-questions session saving a design doc; NO claim ledger, NO evidence typing, NO falsifier recheck anywhere in the 23 skills | 0.85 | gstack ships claim/evidence tracking, or a gbrain schema stores typed claims | gh api repos/garrytan/gstack + office-hours/SKILL.md body, fetched 2026-07-26 | 2026-07-25
C12 | V | internal | Our 2026-07-25 landscape sweep MISSED gstack entirely - a 124k-star direct-adjacent repo by the YC CEO. The competitive-set claims from that sweep were built on an incomplete scan; process lesson: star-magnitude sweeps must include the toolkit category, not just research/memory keywords | 0.9 | - | this recheck, 2026-07-26 | 2026-07-25

## §F FLIPS
id | if this becomes true -> verdict flips to | last-checked | holds?
F1 | a SHIPPED product does pre-registered falsifier recheck across runs -> differentiation gone, reposition as UX layer | 2026-07-26 | n
F2 | cold-operator test hits its pre-registered bar -> go: directory submission + benchmark | 2026-07-25 | untested
F3 | a research/claims plugin lands in the official directory first -> whitespace closed, urgency gone | 2026-07-25 | n

## §Q OPEN
id | st | question | blast | cites | closed_by
Q1 | . | directory acceptance reality for a solo skill+MCP repo: latency, bar, rejection reasons | high | C7 | -
Q2 | . | define + run the benchmark skeptics demand: claim-error / unsupported-verdict rate with vs without the ledger, EviBound-style | high | C8 | -
Q3 | . | do users see claim-ledger as distinct from claude-mem-style context memory? | med | C6 | -

## §D DIFF
run | date | delta | verdict | cost
1 | 2026-07-25 | +10 claims, 3 flips, 3 open Qs; deep-research workflow (5 angles, 23 sources, 109 extracted claims, 25 sent to 3-vote verification: 5 confirmed 3-0, 0 refuted; remaining votes killed by a session limit and finished by hand in the main loop - 4 claims re-verified by direct fetch, 1 CORRECTED) | reshape | 1.65M subagent tok (harness-measured; trim.py's artifact proxy does not capture workflow spend, and says so)
2 | 2026-07-26 | gstack recheck (user-prompted): +C11 gstack scope verified from skill bodies (asks the question, no evidence system), +C12 sweep-miss logged; F1 re-checked holds n; positioning: rnd = the evidence layer office-hours hands off to | reshape | ~2k tok, 3 fetches

## §M METER
unit: run 1 measured by the workflow harness (subagent tokens), not trim.py - the artifact proxy does not see workflow spend
run1: 1,650,467 subagent tok across 105 agents (43 done, 62 killed by a session limit; verification finished by hand)
trim: run 2 should be a recheck: 3 flips + C1/C6/C7 falsifiers + open Qs only; expected well under 50k tok

## §B BUGS
id | date | cause | fix->invariant
