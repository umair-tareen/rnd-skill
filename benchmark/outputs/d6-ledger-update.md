# THESIS: Printhaven assessment
slug: d6
created: 2026-07-25

## §T THESIS
verdict: go (conf 0.68) · as-of run 2 · 2026-07-26
one-line: A third-party audit verified a lower but credible 7900-seller base and 14 signed, countersigned pilot orders supply the real buyer-commitment evidence that was missing, clearing the prior demand-validation gap enough to justify go despite still-unknown seller LTV.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1 | V | world | Printhaven runs on the MeshGrid-2 job queue per the vendors current public spec sheet rev 4, which is documented, versioned, and independently mirrored | 0.8 | - | 01-market.md | 2026-07-25
C2 | V | world | TechWires launch coverage reported Printhaven had 11400 active sellers, a figure that was widely recirculated in later posts and roundups all tracing back to that single TechWire piece | 0.8 | - | 01-market.md | 2026-07-25
C3* | V | world | The vendor formally retracted the 11400 active sellers figure via correction PH-11, issued three weeks after the TechWire coverage, after an internal audit found the original methodology double-counted sellers | 0.9 | - | 03-technical.md | 2026-07-25
C4 | V | world | Meridian Assurance completed a third-party audit with published methodology and workpapers, establishing a revised verified figure of 7900 active sellers; the vendor adopted this figure in spec sheet rev 5, superseding the earlier retraction. TechWire has not amended its original 11400 article, so 11400 remains an unreliable historical figure while 7900 is the current verified scale metric. | 0.9 | - | 05-three-weeks-later.md | 2026-07-25
C5 | V | world | Survey MakerPoll-6 of 214 self-selected respondents recruited from the vendors own mailing list found 87 percent said they would probably or definitely pay 29 dollars per month for Printhaven | 0.75 | - | 02-demand.md | 2026-07-25
C6 | V | world | The MakerPoll-6 sample is self-selected from the vendors own mailing list, which is a biased sample, so the vendors blog claim that demand is proven is not supported by the surveys methodology | 0.8 | - | 02-demand.md | 2026-07-25
C7 | V | world | Meridian Insights analyst note calls the segment structurally underserved and projects strong willingness to pay based on comparable categories rather than on any Printhaven-specific buyer data | 0.7 | - | 02-demand.md | 2026-07-25
C8* | V | world | Printhaven now has 14 signed, countersigned pilot orders on file (batch PH-P14), each with a purchase commitment and an executed signature page, verified by the Meridian Assurance audit; this supersedes the prior absence of purchases, pilots, signed orders, or booked calls documented in the corpus. | 0.9 | - | 05-three-weeks-later.md | 2026-07-25
C9* | V | customer | Demand for Printhaven is now supported by real buyer commitments: 14 signed, countersigned pilot orders (batch PH-P14) with purchase commitments and executed signatures, independently verified by the Meridian Assurance audit, rather than survey sentiment alone. | 0.85 | - | buyer:signature order batch PH-P14 per 05-three-weeks-later.md | 2026-07-25
C10 | O | world | No seller lifetime value figure, or any inputs needed to derive one such as churn, retention, or revenue per seller over time, are documented anywhere in this corpus | 0.5 | - | 04-brief.md | 2026-07-25
C11 | V | world | Vendor redesigned its pricing page and announced a new logo three weeks after launch coverage; no changes to price points or terms accompanied the redesign, so this is a cosmetic change with no bearing on the thesis. | 0.7 | - | 05-three-weeks-later.md | 2026-07-25

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
