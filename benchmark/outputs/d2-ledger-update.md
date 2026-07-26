# THESIS: Orvana assessment
slug: d2
created: 2026-07-25

## §T THESIS
verdict: reshape (conf 0.7) · as-of run 2 · 2026-07-26
one-line: Technical integration and category context still hold, DAU is now independently audited at 289k which supersedes the retracted 417k figure, and demand now has genuine binding evidence via 9 signed pilot orders in batch OR-P9, but customer acquisition cost remains completely undisclosed, so reshape around securing CAC data and expanding pilot-to-paid conversion before further investment.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1 | V | world | Category context: the home strength-training app category has three visible competitors, all priced between 19 and 49 dollars per month, none with a dominant share. | 0.85 | - | 01-market.md | 2026-07-25
C2 | V | world | Per the vendor public specification sheet (rev 4, current), Orvana integrates the HL-Sync wearable standard, which is documented, versioned, and independently mirrored. | 0.8 | - | 01-market.md | 2026-07-25
C3 | V | world | Orvana integration surface is small (one webhook, two SDKs, one CLI) and setup in the reviewed demo took under an hour. | 0.75 | - | 03-technical.md | 2026-07-25
C4 | V | world | TechWire launch coverage reported that Orvana reached 417k daily active users, a figure later recirculated widely, with every recirculation tracing back to that single TechWire piece. | 0.8 | - | 01-market.md | 2026-07-25
C5 | R | world | Orvana has 417k daily active users, the scale figure TechWire originally reported at launch. | 0.85 | Vendor correction OR-22 retracted this figure after an internal audit found the original methodology double-counted. | 03-technical.md | 2026-07-25
C6* | V | world | Vendor formally retracted the 417k daily active figure via correction OR-22, three weeks after TechWire coverage, after an internal audit found double-counting; TechWire has not amended its original article. This retraction is now superseded: independent auditor Meridian Assurance published a verified current figure of 289k daily active with public methodology and workpapers, and the vendor adopted this figure in spec sheet rev 5. | 0.85 | - | 03-technical.md; 05-three-weeks-later.md | 2026-07-25
C7 | V | world | Survey Pulse-D3 of 214 self-selected respondents recruited from Orvana own mailing list found 87 percent said they would probably or definitely pay 29 dollars per month; the vendor blog calls this demand is proven. | 0.8 | - | 02-demand.md | 2026-07-25
C8 | V | world | Analyst firm Meridian Insights calls the segment structurally underserved and projects strong willingness to pay based on comparable categories, without citing any Orvana-specific buyer data. | 0.75 | - | 02-demand.md | 2026-07-25
C9* | R | world | As of run 1, no purchases, pilots, signed orders, or booked calls were documented anywhere in the corpus. This is now superseded: order batch OR-P9 documents 9 signed pilot orders, verified by the Meridian Assurance audit, per 05-three-weeks-later.md. | 0.85 | - | 05-three-weeks-later.md | 2026-07-25
C10 | A | internal | Orvana customer acquisition cost is not stated anywhere in this corpus; no spend, funnel, or per-customer cost figures appear in any of the four documents. | 0.9 | A vendor-disclosed CAC figure, or blended spend and paying-customer counts sufficient to compute one, would resolve this. | - | 2026-07-25
C11* | V | world | Independent audit by Meridian Assurance established a verified current figure of 289k daily active users, lower than the original 417k TechWire figure; the audit methodology and workpapers are published, and the vendor adopted this figure in the current spec sheet (rev 5), superseding the earlier retraction. | 0.85 | - | 05-three-weeks-later.md | 2026-07-26
C12* | V | customer | Orvana has documented signed pilot orders: order batch OR-P9 contains 9 signed pilot orders from named customers, each with a purchase commitment and an executed signature page, independently verified by the Meridian Assurance audit. | 0.85 | - | buyer:signature order batch OR-P9 per 05-three-weeks-later.md | 2026-07-26
C13 | V | world | Vendor redesigned its pricing page and announced a new logo; no changes to price points or terms accompanied the redesign. | 0.75 | - | 05-three-weeks-later.md | 2026-07-26

## §F FLIPS
id | if this becomes true -> verdict flips to | last-checked | holds?

## §Q OPEN
id | st | question | blast | cites | closed_by

## §D DIFF
run | date | delta | verdict | cost
2 | 2026-07-26 | New doc 05 read: independent audit (Meridian Assurance) verifies DAU at 289k, superseding the OR-22 retraction (C6 revised, +C11 load-bearing); 9 signed pilot orders OR-P9 verified via typed buyer evidence (+C12, customer, load-bearing); C9 no-purchases claim refuted; +1 minor claim on pricing-page redesign (C13); demand-UNTESTED flag cleared. | reshape | small recheck: 1 new source, 6 claim ops, no live token metering available

## §M METER
fixed: -
marginal: -
total: -
trim: -

## §B BUGS
id | date | cause | fix->invariant
