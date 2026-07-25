# THESIS: Veltrix assessment
slug: d1
created: 2026-07-25

## §T THESIS
verdict: reshape (conf 0.6) · as-of run 1 · 2026-07-25 · ⚠ demand-UNVALIDATED: 1 customer claim(s), 0 verified by buyer contact (C8)
one-line: Technical foundation looks legitimate and integration is easy, but the headline performance figure is retracted and uncorrected in press, and demand rests only on a self-selected vendor survey with zero verified buyer interactions, so reshape before committing build-partnership effort.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1* | V | world | Veltrix is built on the Corda-2 protocol per the vendor public specification sheet (rev 4), which is documented, versioned, and independently mirrored | 0.75 | - | 01-market.md | 2026-07-25
C2 | V | world | The API-gateway category Veltrix competes in has three visible competitors priced between 19 and 49 dollars per month with no dominant market share | 0.85 | - | 01-market.md | 2026-07-25
C3* | R | world | Veltrix processes 2.4 million requests per second per node | 0.85 | - | 03-technical.md | 2026-07-25
C4 | V | world | TechWire has not amended its original launch article even though the vendor retracted the 2.4 million requests per second figure in correction VX-9, so the uncorrected number continues to circulate in later posts and roundups | 0.8 | - | 03-technical.md | 2026-07-25
C5 | V | world | The vendor has published no updated performance figure since retracting the 2.4 million requests per second claim following an internal audit that found the methodology double-counted | 0.8 | - | 03-technical.md | 2026-07-25
C6 | V | world | Survey Panel-K87 (n=214) was self-selected from the vendor own mailing list, not an independent or random sample, and 87 percent of respondents said they would probably or definitely pay 29 dollars per month | 0.85 | - | 02-demand.md | 2026-07-25
C7 | V | world | No purchases, pilots, signed orders, or booked calls for Veltrix are documented anywhere in this corpus | 0.9 | - | 02-demand.md | 2026-07-25
C8* | A | customer | Willingness to pay for Veltrix is proven by Survey Panel-K87 and the Meridian Insights analyst note, as the vendor blog claims | 0.3 | - | 02-demand.md | 2026-07-25
C9 | V | world | Meridian Insights analyst note describes the segment as structurally underserved with strong willingness to pay, based on comparable categories rather than Veltrix-specific buyer data | 0.7 | - | 02-demand.md | 2026-07-25
C10 | V | world | Setup in the reviewed technical demo took under an hour using a webhook, two SDKs, and a CLI | 0.8 | - | 03-technical.md | 2026-07-25
C11 | O | world | Veltrix monthly churn rate is unknown; no churn, retention, or cohort data appears anywhere in this corpus | 0 | - | 01-market.md;02-demand.md;03-technical.md | 2026-07-25

## §F FLIPS
id | if this becomes true -> verdict flips to | last-checked | holds?

## §Q OPEN
id | st | question | blast | cites | closed_by

## §D DIFF
run | date | delta | verdict | cost

## §M METER
fixed: -
marginal: -
total: -
trim: -

## §B BUGS
id | date | cause | fix->invariant
