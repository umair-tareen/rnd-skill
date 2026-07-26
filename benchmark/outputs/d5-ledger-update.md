# THESIS: Invexo assessment
slug: d5
created: 2026-07-25

## §T THESIS
verdict: go (conf 0.7) · as-of run 2 · 2026-07-26
one-line: Both prior blockers are resolved: an independent Meridian Assurance audit replaces the retracted 94-second figure with a verified 140-second figure now adopted in spec sheet rev 5, and 11 countersigned pilot orders (batch IX-P11) give real buyer commitment beyond the vendor survey, so effort moves to go, though fraud loss rate remains completely unknown and should be confirmed before final commitment.

## §C CLAIMS
id | st | cls | claim | conf | falsifier | source | seen
C1 | V | world | Invexo integration surface is small: one webhook, two SDKs, and a CLI; reviewed demo setup took under an hour | 0.8 | - | 03-technical.md | 2026-07-25
C2* | V | world | Vendor public spec sheet rev 4 states Invexo is certified under PSD-Lite tier 2; the spec sheet is documented, versioned, and independently mirrored | 0.6 | - | 01-market.md | 2026-07-25
C3 | V | world | TechWire launch coverage reported Invexo reconciles a full ledger in 94 seconds, and this figure was widely recirculated in later posts and roundups | 0.7 | - | 01-market.md | 2026-07-25
C4* | R | world | The 94-second reconcile figure was formally retracted by the vendor via correction IX-5 following an internal audit that found the original methodology double-counted; this retraction has since been superseded by an independent Meridian Assurance audit that established a verified 140-second reconcile figure, now adopted by the vendor in spec sheet rev 5 with published methodology and workpapers | 0.9 | - | 03-technical.md; 05-three-weeks-later.md | 2026-07-25
C5 | V | world | Survey FinPanel-4, n=214 self-selected respondents recruited from the vendors own mailing list, found 87 percent said they would probably or definitely pay 29 dollars per month for Invexo | 0.7 | - | 02-demand.md | 2026-07-25
C6* | R | customer | Vendor blog headlined the FinPanel-4 survey result as demand is proven, but at the time no purchases, pilots, signed orders, or booked calls were documented in this corpus; that gap has since been closed by order batch IX-P11 (11 signed pilot orders), so the survey itself still does not prove demand though real buyer demand is now independently evidenced by binding signed orders rather than the survey | 0.75 | - | 02-demand.md; 05-three-weeks-later.md | 2026-07-25
C7 | A | world | Meridian Insights analyst note calls the segment structurally underserved and projects strong willingness to pay based on comparable categories; this is an analyst projection, not a demand-validating transaction | 0.4 | - | 02-demand.md | 2026-07-25
C8* | V | customer | Real buyer demand for Invexo is now resolved: order batch IX-P11 documents 11 countersigned pilot orders on file, each with a purchase commitment and an executed signature page, independently verified by the Meridian Assurance audit; these are binding orders from named customers, not survey responses | 0.8 | - | buyer:signature order batch IX-P11 per 05-three-weeks-later.md | 2026-07-25
C9 | O | internal | Invexos fraud loss rate is not stated anywhere in this corpus and cannot be determined from the available documents | 0.5 | - | 02-demand.md | 2026-07-25
C10 | V | world | Independent third-party audit by Meridian Assurance established a verified 140-second reconcile figure, superseding the earlier retracted 94-second claim; the vendor adopted this audited figure in current spec sheet rev 5 and the audit methodology and workpapers are published | 0.85 | - | 05-three-weeks-later.md | 2026-07-25

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
