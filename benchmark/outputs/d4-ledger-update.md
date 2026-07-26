# THESIS: Casterly assessment
slug: d4
created: 2026-07-25

## §T THESIS
verdict: go (conf 0.7) · as-of run 2 · 2026-07-26
one-line: An independent Meridian Assurance audit now backs a verified 57 percent editing-time-cut figure replacing the retracted 83 percent, and documents 8 signed CS-P8 pilot orders as real buyer evidence, resolving the prior demand-validation gap, so proceed to build-partnership while tracking pilot-to-paid conversion and the still-undocumented subscription length.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1 | V | world | Casterly runs on the WavePipe rendering engine per the vendor public specification sheet (rev 4, current), which is documented, versioned, and independently mirrored. | 0.85 | - | 01-market.md | 2026-07-25
C2 | V | world | Casterly integration surface is small (a webhook, two SDKs, and a CLI), and setup in the reviewed demo took under an hour. | 0.75 | - | 03-technical.md | 2026-07-25
C3 | V | world | The Casterly market category has three visible competitors, all priced between $19 and $49 per month, with none holding a dominant share. | 0.8 | - | 01-market.md | 2026-07-25
C4 | V | world | TechWire launch coverage reported that Casterly cuts editing time by 83 percent, a figure that was widely recirculated in later posts and roundups but always traces back to that one TechWire piece. | 0.85 | - | 01-market.md | 2026-07-25
C5* | V | world | The vendor retracted the original 83 percent editing-time-cut figure after an internal audit found double-counting; independent third-party auditor Meridian Assurance then completed an audit establishing a verified 57 percent editing-time-cut figure, which the vendor has adopted in its current spec sheet (rev 5); TechWire has not amended its original article citing 83 percent. | 0.9 | - | 05-three-weeks-later.md | 2026-07-25
C6 | V | world | Survey MicSurvey-12 (n=214, self-selected respondents recruited from the vendor own mailing list) found that 87 percent said they would probably or definitely pay $29/month for Casterly; the vendor blog headline states demand is proven. | 0.85 | - | 02-demand.md | 2026-07-25
C7 | V | world | An analyst note from Meridian Insights calls the Casterly segment structurally underserved and projects strong willingness to pay based on comparable categories. | 0.6 | - | 02-demand.md | 2026-07-25
C8* | R | world | As of the original market, demand, and technical files, no purchases, pilots, signed orders, or booked calls were documented anywhere in this corpus; this is now superseded by 05-three-weeks-later.md, which documents order batch CS-P8, 8 signed pilot orders each with a purchase commitment and an executed signature page, verified by the Meridian Assurance audit. | 0.9 | - | 05-three-weeks-later.md | 2026-07-25
C9* | V | customer | Real buyers have committed to Casterly: order batch CS-P8 documents 8 signed pilot orders, each with a purchase commitment and an executed signature page, verified by the Meridian Assurance audit; buyer-behavior evidence now exists beyond the earlier stated-intent survey, resolving the prior demand-validation gap. | 0.85 | - | buyer:signature order batch CS-P8 per 05-three-weeks-later.md | 2026-07-25
C10 | V | world | Casterly average subscription length is not documented anywhere across the market, demand, or technical files in this corpus. | 0.9 | - | 01-market.md, 02-demand.md, 03-technical.md | 2026-07-25
C11 | V | world | The vendor redesigned its pricing page and announced a new logo per the three-weeks-later update; no changes to price points or subscription terms accompanied the redesign. | 0.85 | - | 05-three-weeks-later.md | 2026-07-25

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
