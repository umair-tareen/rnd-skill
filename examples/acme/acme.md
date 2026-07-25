# THESIS: Acme - paid changelog tool for small dev teams
slug: acme
created: 2026-07-25

## §T THESIS
verdict: reshape (conf 0.6) · as-of run 2 · 2026-07-25 · ⚠ demand-UNVALIDATED: 2 customer claim(s), 0 verified by buyer contact (C4,C5)
one-line: Re-held: template rival dismissed (C8), free-bundling and price band re-verified; the support reframe is still untested with any buyer - that is the whole next move.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1* | V | world | RivalCo bundles changelog generation free inside its base tier | 0.85 | a paying team cites a need the free version fails | example.com/pricing | 2026-07-24
C2 | V | world | platform webhooks make ingestion free on every plan | 0.9 | a platform paywalls release webhooks | example.org/docs/webhooks | 2026-07-24
C3* | V | world | $10/seat/mo sits inside the adjacent dev-tool price band | 0.7 | 3 target teams call $10/seat high in a walkthrough | example.net/pricing-scan | 2026-07-24
C4 | A | customer | support teams are the daily READER of 'what changed' and hold budget | 0.4 | 5 support leads shrug in discovery calls | - | 2026-07-24
C5 | A | customer | maintainers will pay to stop writing release notes | 0.3 | every enthusiastic thread keeps doing it free with a script | - | 2026-07-24
C6 | O | internal | draft quality clears the 'shippable without hand-editing' bar | - | two postmortems blame near-miss drafts for churn | blog postmortems (weak) | 2026-07-24
C7 | A | internal | an install takes under half a day of founder time | 0.5 | first real install exceeds a day | - | 2026-07-24
C8 | V | world | AcmeDev's 'AI release-notes' is a template feature, not generation - not a rival | 0.75 | AcmeDev ships actual generation | acme.example/docs/templates | 2026-07-25

## §F FLIPS
id | if this becomes true -> verdict flips to | last-checked | holds?
F1 | 3+ support leads say they'd pay -> go | 2026-07-25 | untested
F2 | RivalCo ships a support-facing changelog -> no-go | 2026-07-25 | n

## §Q OPEN
id | st | question | blast | cites | closed_by
Q1 | x | is AcmeDev's 'AI release-notes' real? | high | C1 | C8
Q2 | . | do support teams hold a budget line for this? | high | C4 | -
Q3 | . | what does churn look like past month 2? | med | C6 | -

## §D DIFF
run | date | delta | verdict | cost
1 | 2026-07-24 | +7 claims, 2 flips, 3 open Qs; full sweep | reshape | 9,846 tok written-artifact / <$0.15 est.
2 | 2026-07-25 | recheck/diff: Q1 closed on evidence (C8), F1/F2 stamped, C1/C3 re-held; Q2 needs buyers not searches | reshape | 952 tok written-artifact (10% of run 1)

## §M METER
unit: written-artifact tokens (chars/4) - a size proxy, NOT API spend
fixed: 631 tok (thesis re-read)
marginal: 321 tok (run-2 recheck brief)
total: 952 tok = 10% of run 1's 9,846
trim: landscape stable; next run recheck-only. Q2 is a call, not a search.

## §B BUGS
id | date | cause | fix->invariant
