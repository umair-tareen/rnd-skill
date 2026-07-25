# THESIS: Orvana assessment
slug: d2
created: 2026-07-25

## §T THESIS
verdict: reshape (conf 0.6) · as-of run 1 · 2026-07-25 · ⚠ demand-UNTESTED: no customer-class claim exists yet
one-line: Technical integration checks out, but the headline 417k DAU figure is retracted, demand rests only on a self-selected vendor-list survey with zero purchases, pilots, or booked calls, and CAC is unknown, so reshape around real buyer validation before further investment.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1 | V | world | Category context: the home strength-training app category has three visible competitors, all priced between 19 and 49 dollars per month, none with a dominant share. | 0.85 | - | 01-market.md | 2026-07-25
C2 | V | world | Per the vendor public specification sheet (rev 4, current), Orvana integrates the HL-Sync wearable standard, which is documented, versioned, and independently mirrored. | 0.8 | - | 01-market.md | 2026-07-25
C3 | V | world | Orvana integration surface is small (one webhook, two SDKs, one CLI) and setup in the reviewed demo took under an hour. | 0.75 | - | 03-technical.md | 2026-07-25
C4 | V | world | TechWire launch coverage reported that Orvana reached 417k daily active users, a figure later recirculated widely, with every recirculation tracing back to that single TechWire piece. | 0.8 | - | 01-market.md | 2026-07-25
C5 | R | world | Orvana has 417k daily active users, the scale figure TechWire originally reported at launch. | 0.85 | Vendor correction OR-22 retracted this figure after an internal audit found the original methodology double-counted. | 03-technical.md | 2026-07-25
C6* | V | world | The vendor formally retracted the 417k daily active figure via correction OR-22, three weeks after the TechWire coverage, after an internal audit found the original methodology double-counted; no updated figure has been published, and TechWire has not amended its original article. | 0.85 | - | 03-technical.md | 2026-07-25
C7 | V | world | Survey Pulse-D3 of 214 self-selected respondents recruited from Orvana own mailing list found 87 percent said they would probably or definitely pay 29 dollars per month; the vendor blog calls this demand is proven. | 0.8 | - | 02-demand.md | 2026-07-25
C8 | V | world | Analyst firm Meridian Insights calls the segment structurally underserved and projects strong willingness to pay based on comparable categories, without citing any Orvana-specific buyer data. | 0.75 | - | 02-demand.md | 2026-07-25
C9* | V | world | No purchases, pilots, signed orders, or booked calls for Orvana are documented anywhere in this corpus. | 0.9 | - | 02-demand.md | 2026-07-25
C10 | A | internal | Orvana customer acquisition cost is not stated anywhere in this corpus; no spend, funnel, or per-customer cost figures appear in any of the four documents. | 0.9 | A vendor-disclosed CAC figure, or blended spend and paying-customer counts sufficient to compute one, would resolve this. | - | 2026-07-25

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
