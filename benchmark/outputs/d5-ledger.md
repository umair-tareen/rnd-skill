# THESIS: Invexo assessment
slug: d5
created: 2026-07-25

## §T THESIS
verdict: reshape (conf 0.6) · as-of run 1 · 2026-07-25 · ⚠ demand-UNVALIDATED: 1 customer claim(s), 0 verified by buyer contact (C8)
one-line: Technical foundation looks small and workable, but the headline 94-second figure is retracted and demand rests only on a vendor-mailing-list survey and analyst opinion with zero real purchases, pilots, or booked calls, and fraud loss rate is unknown, so effort should reshape around getting a validated benchmark and a real buyer commitment before committing further.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1 | V | world | Invexo integration surface is small: one webhook, two SDKs, and a CLI; reviewed demo setup took under an hour | 0.8 | - | 03-technical.md | 2026-07-25
C2* | V | world | Vendor public spec sheet rev 4 states Invexo is certified under PSD-Lite tier 2; the spec sheet is documented, versioned, and independently mirrored | 0.6 | - | 01-market.md | 2026-07-25
C3 | V | world | TechWire launch coverage reported Invexo reconciles a full ledger in 94 seconds, and this figure was widely recirculated in later posts and roundups | 0.7 | - | 01-market.md | 2026-07-25
C4* | R | world | The 94-second reconcile figure was formally retracted by the vendor via correction IX-5, three weeks after the TechWire coverage, following an internal audit that found the original methodology double-counted; no updated figure has been published and TechWire has not amended its article | 0.85 | - | 03-technical.md | 2026-07-25
C5 | V | world | Survey FinPanel-4, n=214 self-selected respondents recruited from the vendors own mailing list, found 87 percent said they would probably or definitely pay 29 dollars per month for Invexo | 0.7 | - | 02-demand.md | 2026-07-25
C6* | R | customer | Vendor blog headlines the FinPanel-4 survey result as demand is proven, but no purchases, pilots, signed orders, or booked calls are documented anywhere in this corpus, so the proven-demand claim is not supported by real buyer behavior | 0.75 | - | 02-demand.md | 2026-07-25
C7 | A | world | Meridian Insights analyst note calls the segment structurally underserved and projects strong willingness to pay based on comparable categories; this is an analyst projection, not a demand-validating transaction | 0.4 | - | 02-demand.md | 2026-07-25
C8* | O | customer | Whether real buyer demand for Invexo exists (purchases, pilots, signed orders, or booked calls) is unresolved: the corpus documents none | 0.5 | - | 02-demand.md | 2026-07-25
C9 | O | internal | Invexos fraud loss rate is not stated anywhere in this corpus and cannot be determined from the available documents | 0.5 | - | 02-demand.md | 2026-07-25

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
