# THESIS: AgriPod assessment
slug: d3
created: 2026-07-25

## §T THESIS
verdict: go (conf 0.75) · as-of run 2 · 2026-07-26
one-line: Both prior reshape conditions are now met: an independent Meridian Assurance audit corrected the battery figure to a verified 44 months adopted in vendor spec rev 5, and 15 signed pilot orders in batch AP-P15 give real buyer evidence of demand, so the recommendation moves to go, with warranty return rate still unknown and pilot-stage (not full commercial) orders as the residual watch items.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1 | V | world | AgriPod uses the LoRa-Mesh v3 radio per the vendor public specification sheet, rev 4, current, documented, versioned, and independently mirrored. | 0.85 | - | 01-market.md | 2026-07-25
C2 | V | world | TechWire launch coverage reported that the AgriPod field battery lasts 61 months. | 0.85 | - | 01-market.md | 2026-07-25
C3* | V | world | The vendor formally retracted the 61 month battery figure in correction AP-7, dated three weeks after the TechWire coverage, following an internal audit that found the original methodology double counted. | 0.9 | - | 03-technical.md | 2026-07-25
C4 | V | world | TechWire has not amended its original article despite the vendor retraction, so the 61 month figure remains uncorrected in wider circulation. | 0.85 | - | 03-technical.md | 2026-07-25
C5* | R | world | The AgriPod field battery lasts 61 months. | 0.85 | - | 03-technical.md | 2026-07-25
C6 | V | world | FieldPoll-9 sampled 214 self selected respondents recruited from the vendor mailing list. | 0.9 | - | 02-demand.md | 2026-07-25
C7 | V | world | 87 percent of FieldPoll-9 respondents said they would probably or definitely pay 29 dollars per month for AgriPod. | 0.85 | - | 02-demand.md | 2026-07-25
C8 | V | world | The vendor blog describes the FieldPoll-9 results as proof that demand is proven. | 0.85 | - | 02-demand.md | 2026-07-25
C9 | V | world | Meridian Insights projects strong willingness to pay for the AgriPod segment based on comparable categories rather than AgriPod specific buyer data. | 0.8 | - | 02-demand.md | 2026-07-25
C10* | V | customer | Demand for AgriPod is validated by real buyer behavior: order batch AP-P15 documents 15 signed pilot orders, each with a purchase commitment and an executed signature page, verified by independent audit. | 0.85 | any order in batch AP-P15 is found unsigned, non-binding, or fabricated | buyer:signature order batch AP-P15 per 05-three-weeks-later.md | 2026-07-25
C11 | V | internal | No document in this corpus states a warranty return rate figure for AgriPod, so it cannot be stated from the evidence available. | 0.9 | - | 01-market.md;02-demand.md;03-technical.md | 2026-07-25
C12* | V | world | An independent third-party audit by Meridian Assurance established a revised, verified battery figure of 44 months, superseding the earlier retraction that had left no replacement figure; the vendor has adopted this audited figure in its current specification sheet, rev 5, and the audit methodology and workpapers are published. | 0.85 | Meridian Assurance audit methodology or workpapers are found non-independent, unpublished, or the vendor has not actually adopted the figure in rev 5 | 05-three-weeks-later.md | 2026-07-25
C13 | V | world | The vendor redesigned its pricing page and announced a new logo three weeks after the original coverage; no changes to price points or contract terms accompanied the redesign, so the 29 dollars per month reference price from FieldPoll-9 is unaffected. | 0.75 | - | 05-three-weeks-later.md | 2026-07-25

## §F FLIPS
id | if this becomes true -> verdict flips to | last-checked | holds?

## §Q OPEN
id | st | question | blast | cites | closed_by

## §D DIFF
run | date | delta | verdict | cost
2 | 2026-07-26 | C10 demand claim R to V on buyer:signature evidence (order batch AP-P15, 15 signed pilots); +C12 load-bearing: independent audit verifies 44-month battery, supersedes retraction; +C13 pricing/logo redesign confirmed immaterial (no price/terms change); verdict reshape(0.6) to go(0.75) | go | -

## §M METER
fixed: -
marginal: -
total: -
trim: -

## §B BUGS
id | date | cause | fix->invariant
