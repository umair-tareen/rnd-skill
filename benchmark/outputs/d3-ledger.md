# THESIS: AgriPod assessment
slug: d3
created: 2026-07-25

## §T THESIS
verdict: reshape (conf 0.6) · as-of run 1 · 2026-07-25 · ⚠ demand-UNTESTED: no customer-class claim exists yet
one-line: Technical base (LoRa-Mesh v3) is documented and sound, but the only headline performance figure in circulation was retracted by the vendor and demand rests solely on a biased self-selected survey with zero real buyer evidence, so reshape the ask around a corrected spec and actual pilot commitments before committing build-partnership effort.

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
C10* | R | customer | Demand for AgriPod is validated by real buyer behavior such as purchases, pilots, signed orders, or booked calls. | 0.9 | - | 02-demand.md | 2026-07-25
C11 | V | internal | No document in this corpus states a warranty return rate figure for AgriPod, so it cannot be stated from the evidence available. | 0.9 | - | 01-market.md;02-demand.md;03-technical.md | 2026-07-25

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
