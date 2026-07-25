# THESIS: Casterly assessment
slug: d4
created: 2026-07-25

## §T THESIS
verdict: reshape (conf 0.6) · as-of run 1 · 2026-07-25 · ⚠ demand-UNVALIDATED: 1 customer claim(s), 0 verified by buyer contact (C9)
one-line: Technical foundation is real and easy to integrate, but the only performance figure in circulation was retracted uncorrected in public, and demand rests solely on a self-selected stated-intent survey with zero purchases, pilots, or booked calls, so reshape around a fresh validated metric and real buyer evidence before committing build-partnership effort.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1 | V | world | Casterly runs on the WavePipe rendering engine per the vendor public specification sheet (rev 4, current), which is documented, versioned, and independently mirrored. | 0.85 | - | 01-market.md | 2026-07-25
C2 | V | world | Casterly integration surface is small (a webhook, two SDKs, and a CLI), and setup in the reviewed demo took under an hour. | 0.75 | - | 03-technical.md | 2026-07-25
C3 | V | world | The Casterly market category has three visible competitors, all priced between $19 and $49 per month, with none holding a dominant share. | 0.8 | - | 01-market.md | 2026-07-25
C4 | V | world | TechWire launch coverage reported that Casterly cuts editing time by 83 percent, a figure that was widely recirculated in later posts and roundups but always traces back to that one TechWire piece. | 0.85 | - | 01-market.md | 2026-07-25
C5* | V | world | The vendor formally retracted the 83 percent editing-time-cut figure three weeks after the TechWire coverage, following an internal audit that found the original methodology double-counted; the vendor has published no updated figure, and TechWire has not amended its original article. | 0.9 | - | 03-technical.md | 2026-07-25
C6 | V | world | Survey MicSurvey-12 (n=214, self-selected respondents recruited from the vendor own mailing list) found that 87 percent said they would probably or definitely pay $29/month for Casterly; the vendor blog headline states demand is proven. | 0.85 | - | 02-demand.md | 2026-07-25
C7 | V | world | An analyst note from Meridian Insights calls the Casterly segment structurally underserved and projects strong willingness to pay based on comparable categories. | 0.6 | - | 02-demand.md | 2026-07-25
C8* | V | world | No purchases, pilots, signed orders, or booked calls for Casterly are documented anywhere in this corpus. | 0.9 | - | 02-demand.md | 2026-07-25
C9* | O | customer | Whether real buyers will pay for Casterly, evidenced by purchases, pilots, signed orders, or booked calls, remains unresolved; the corpus contains only a self-selected stated-intent survey and an analyst comparable projection, with zero documented buyer-behavior evidence. | 0.2 | - | 02-demand.md | 2026-07-25
C10 | V | world | Casterly average subscription length is not documented anywhere across the market, demand, or technical files in this corpus. | 0.9 | - | 01-market.md, 02-demand.md, 03-technical.md | 2026-07-25

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
