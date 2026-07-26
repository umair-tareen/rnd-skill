# Casterly — Partnership Assessment (Updated)

**Verdict: GO, staged/conditional — confidence ~65%.**
Upgraded from the prior NO-GO (hold, ~75% confidence). The two findings that drove the original hold — a retracted, unreplaced performance figure and zero real commercial evidence — have both been superseded by new, independently verified documents. One material gap from the original assessment remains completely unaddressed. Proceed to a bounded pilot-scale partnership; gate any deeper commitment on the still-missing economics data.

Scope note: this update adds `05-three-weeks-later.md` to the original four documents (01-market, 02-demand, 03-technical, 04-brief) per the brief's instruction to use only the provided corpus. Where the corpus doesn't answer a question, that is stated explicitly rather than inferred or estimated. Changes from the prior assessment are called out inline.

---

## What changed since the last assessment

1. **The performance figure has been re-verified, not just retracted.** Meridian Assurance — a named third party — completed an independent audit of the figure the vendor had pulled. The audit produced a revised, verified number (57% editing-time cut, down from the original 83% claim), and Meridian's methodology and workpapers are published, not merely asserted. The vendor has adopted this audited figure in its current spec sheet (rev 5). This is a materially different evidentiary posture than three weeks ago: there is now a current, sourced, third-party-checked figure in evidence — not an admitted-wrong number with nothing to replace it.
2. **Real commercial evidence now exists.** Order batch CS-P8: eight countersigned pilot agreements, each with a purchase commitment and an executed signature page, verified by the same Meridian audit. This is exactly the category of evidence the prior assessment flagged as absent ("no purchases, pilots, signed orders, or booked calls are documented anywhere in this corpus") and named as the cheapest test to run before proceeding. It has now been supplied, independently checked, and it clears the bar: these are binding commitments from named customers, not survey-stated intent.
3. **Cosmetic, non-decision-relevant change:** the vendor redesigned its pricing page and announced a new logo, with no changes to price points or terms. Noted for completeness; it has no bearing on the verdict and should not be treated as a signal either way.

## 1. Technical foundation

Unchanged from the prior assessment. Casterly runs the "WavePipe rendering engine" per the vendor's spec sheet, now at rev 5. It remains documented, versioned, and independently mirrored — third-party corroboration that the engine exists and is what it claims to be, versioned — but every functional/quality claim about WavePipe itself is still vendor-sourced; no independent benchmark of the engine specifically appears anywhere in this corpus, old or new.

The integration surface (webhook, two SDKs, CLI) with sub-hour reviewed setup remains a genuine, independently observed positive and is untouched by the new document.

**Net:** same as before — plausible, low-friction technical foundation; the engine's own differentiation claims are still unverified beyond "it exists and is versioned." Nothing new here changes this line item.

## 2. The performance/scale figure in circulation

This is the item that moved the most. Sequence, in full, across both assessment rounds:

- TechWire's launch article reported an 83% editing-time cut. Every later citation traced back to that single piece (citation laundering).
- Three weeks after the TechWire piece, the vendor formally retracted the 83% figure following an internal audit that found the original methodology double-counted. No replacement figure was published at that time. TechWire never amended its article. (This was the single most important fact in the prior assessment.)
- **New:** an independent auditor, Meridian Assurance, has now completed a third-party audit and published a verified figure of **57%**, along with its methodology and workpapers. The vendor has adopted this figure in spec sheet rev 5.

Two things follow from this. First, the retraction is superseded — there is now a current, defensible number, and it carries better provenance (independent audit, published workpapers) than the original TechWire figure ever did (single-source press citation). Second, the corrected number is substantially lower than what drove market perception (57% vs. the 83% still circulating in TechWire citations and roundups) — a ~26-point gap. Any partnership conversation should cite 57% (Meridian-verified, spec rev 5) and should anticipate that counterparties who only know the TechWire number will need correcting; the uncorrected TechWire article is still live and still the more widely recirculated figure.

**Net:** resolved, but not for free. There is now a usable, credible number. It is meaningfully less impressive than the marketing claim that built the category's current perception of Casterly, which is itself useful information about how inflated the original pitch was.

## 3. Is demand validated, and by what evidence?

Materially better than three weeks ago, though still not exhaustively proven at scale.

- **MicSurvey-12** (n=214, self-selected from the vendor's own mailing list) is unchanged and still weak evidence for the reasons already given: biased sample, stated intent rather than observed behavior. The vendor's "demand is proven" framing was not supported then and still is not supported by this instrument alone.
- **Meridian Insights**' "structurally underserved" / "strong willingness to pay" note is unchanged — analogical reasoning from comparable categories, not primary evidence about Casterly. (Note: this is a distinct entity from Meridian Assurance, the auditor in the new document — do not conflate an analyst opinion piece with an audited evidentiary finding.)
- **New:** order batch CS-P8 — eight signed pilot agreements, each with a purchase commitment and an executed signature page, independently verified by the Meridian Assurance audit. This is real, behavioral, binding commercial evidence: named customers who committed money/signature, checked by a third party. It is categorically different from, and stronger than, everything in the prior demand file.

Caveat worth stating plainly: eight pilot orders is a real signal, not a market-validated conclusion. It confirms that specific, identifiable buyers will commit to a paid pilot — which is exactly what the prior assessment asked for — but it is a small n and says nothing yet about conversion-to-renewal, expansion, or churn. Treat it as validated early demand, not validated demand at scale.

**Net:** the prior "zero real commercial evidence" finding is now false — real, verified, signed commercial evidence exists. Demand is no longer intent-only. It remains early-stage.

## 4. Average subscription length

**Still not stated anywhere in the corpus, including the new document.** `05-three-weeks-later.md` discusses the audit, the pilot orders, and the pricing-page/logo redesign — it does not touch retention, churn, or subscription length in any form. This gap is completely unaddressed by the new evidence and should still be treated as absent data, not estimated or inferred. Given that CS-P8 are pilots rather than renewals, subscription-length data may not even exist yet in a meaningful form — but the corpus doesn't say that either, so this is flagged as unknown, full stop.

This is now the single largest remaining gap. Partnership economics (LTV, payback period, whether an 8-pilot cohort is worth building around) still cannot be sized from anything in this dossier.

---

## Why GO (staged) rather than a clean GO or continued NO-GO

**Why not continued NO-GO:** both objections that justified the prior hold have been resolved by evidence that meets the bar the prior assessment itself set — an independently audited replacement figure with published methodology, and real signed pilot orders in place of survey intent. Holding further with this evidence in hand would be over-weighting the original vendor overclaim rather than responding to what's now in the record.

**Why not a clean, unconditional GO:** the retained gap — no subscription-length/retention/cohort data anywhere in the corpus — is exactly the input needed to size a partnership commitment, and it is exactly as absent now as it was three weeks ago. Eight pilots is genuine but small; nothing indicates whether these pilots renew, expand, or churn. Committing at full scale on the current evidence would mean sizing effort against unknowable unit economics, which is a different (and larger) risk than "is there real interest."

## What would flip this further, or reverse it

- **Would strengthen to a clean GO:** retention/cohort data on the CS-P8 pilots (or any prior cohort) once available — even preliminary 30/60/90-day figures.
- **Would revert toward NO-GO:** if the CS-P8 pilots fail to convert to paid renewals when they come up, or if a further independent look at the 57% figure or the audit itself surfaces problems (nothing in this corpus suggests that, but the corpus is also thin — one audit, one batch of orders).
- **Worth tracking but decision-irrelevant:** the pricing-page/logo redesign is cosmetic per the document itself (no price or term changes) and should not be read as either a positive or negative signal.

**Cheapest next test:** ask Casterly for (a) the CS-P8 pilots' renewal/expansion status once their pilot terms lapse, and (b) any subscription-length or cohort-retention data that exists for their broader (non-pilot) customer base, even informally. Structure any partnership commitment now as staged/bounded — matched to the pilot scale actually in evidence — rather than sized against assumed retention.
