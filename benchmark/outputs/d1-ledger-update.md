# THESIS: Veltrix assessment
slug: d1
created: 2026-07-25

## §T THESIS
verdict: go (conf 0.75) · as-of run 2 · 2026-07-26
one-line: The previously retracted performance figure is now independently audited and vendor-adopted at 1.7M req/s, and demand is now backed by 12 signed pilot orders with executed signatures rather than only a self-selected survey, so proceed with build-partnership effort while tracking churn, which remains unknown.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1* | V | world | Veltrix is built on the Corda-2 protocol per the vendor public specification sheet (rev 4), which is documented, versioned, and independently mirrored | 0.75 | - | 01-market.md | 2026-07-25
C2 | V | world | The API-gateway category Veltrix competes in has three visible competitors priced between 19 and 49 dollars per month with no dominant market share | 0.85 | - | 01-market.md | 2026-07-25
C3* | R | world | Veltrix processes 2.4 million requests per second per node | 0.85 | - | 03-technical.md | 2026-07-25
C4 | V | world | TechWire has not amended its original launch article even though the vendor retracted the 2.4 million requests per second figure in correction VX-9, so the uncorrected number continues to circulate in later posts and roundups | 0.8 | - | 03-technical.md | 2026-07-25
C5 | V | world | Meridian Assurance completed an independent audit of the retracted 2.4 million requests per second figure and established a revised, verified figure of 1.7 million requests per second; the vendor adopted this figure in specification sheet rev 5, with Meridian methodology and workpapers published | 0.85 | - | 05-three-weeks-later.md | 2026-07-25
C6 | V | world | Survey Panel-K87 (n=214) was self-selected from the vendor own mailing list, not an independent or random sample, and 87 percent of respondents said they would probably or definitely pay 29 dollars per month | 0.85 | - | 02-demand.md | 2026-07-25
C7 | V | customer | Order batch VX-P12 documents 12 signed pilot orders for Veltrix, each with a purchase commitment and an executed signature page, verified by the Meridian Assurance audit; this reverses the earlier absence of any purchases, pilots, or signed orders | 0.85 | - | buyer:signature order batch VX-P12 per 05-three-weeks-later.md | 2026-07-25
C8* | A | customer | Willingness to pay for Veltrix is proven by Survey Panel-K87 and the Meridian Insights analyst note, as the vendor blog claims | 0.3 | - | 02-demand.md | 2026-07-25
C9 | V | world | Meridian Insights analyst note describes the segment as structurally underserved with strong willingness to pay, based on comparable categories rather than Veltrix-specific buyer data | 0.7 | - | 02-demand.md | 2026-07-25
C10 | V | world | Setup in the reviewed technical demo took under an hour using a webhook, two SDKs, and a CLI | 0.8 | - | 03-technical.md | 2026-07-25
C11 | O | world | Veltrix monthly churn rate is unknown; no churn, retention, or cohort data appears anywhere in this corpus | 0 | - | 01-market.md;02-demand.md;03-technical.md | 2026-07-25
C12 | V | world | The vendor redesigned its pricing page and announced a new logo in the same period; no changes to price points or terms accompanied the redesign, so this is cosmetic only and has no bearing on the demand or pricing thesis | 0.9 | - | 05-three-weeks-later.md | 2026-07-25

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
