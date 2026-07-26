# Invexo — Claims-Based Assessment (Updated)

**Verdict: RESHAPE, leaning GO — confidence: medium-high.** Two of the three findings that drove the prior NO-GO have been substantively resolved by independent, third-party evidence in the last three weeks. The remaining gaps (certification provenance, fraud loss rate) are real but no longer stack into a disqualifying case on their own.

## What changed since the last assessment
A new document (three-weeks-later) reports an independent audit by Meridian Assurance that (a) re-examined the retracted reconcile-time figure and established a verified replacement number, which the vendor has adopted in its current spec sheet, and (b) verified a batch of signed pilot orders with executed signatures and purchase commitments from named customers. Both previously-fatal gaps — a dead performance metric and unvalidated demand — now have independent evidentiary backing they lacked three weeks ago. A pricing-page redesign and new logo are also reported; no price or term changes accompany them, so this is cosmetic and not load-bearing.

## 1. Technical foundation
No new evidence on this point. Invexo's PSD-Lite tier 2 certification is still sourced only to the vendor's own public specification sheet, now at rev 5. The sheet is documented, versioned, and independently mirrored — but as before, that establishes the *document's* stability and availability, not third-party confirmation of the *certification* itself. No registry entry, auditor's letter, or certifying-body confirmation appears anywhere in the corpus, including the new document. Notably, the Meridian Assurance audit that verified the performance figure and the pilot orders did not extend to the certification claim — the audit's scope was specifically the retracted figure and the pilot batch. So this remains the single clearest unresolved item in the file, and it's worth flagging to Invexo directly: the same auditor is already in the building: ask if certification can be added to scope.

The integration surface (webhook, two SDKs, CLI, sub-hour demo setup) is unchanged and still unremarkable — not a concern, not a differentiator.

## 2. The performance/scale figure in circulation
This is the biggest change. Three weeks ago: the vendor had retracted the widely-circulated "94-second reconcile" figure (correction IX-5) after an internal audit found double-counting, published no replacement, and TechWire never amended the original article — leaving a dead, uncorrected number as the only one in the market.

Now: Meridian Assurance completed an independent third-party audit of that retracted figure and established a verified replacement — **140 seconds**. The vendor has adopted this audited figure in its current spec sheet (rev 5), and Meridian's methodology and workpapers are published, giving this number a materially stronger evidentiary basis than the original TechWire-sourced figure ever had (that one traced to a single article with no methodology disclosed at all).

Two things to hold in tension:
- **Evidentiary quality is now good.** This isn't a vendor self-report or a single journalist's number — it's an audited figure with public workpapers, adopted transparently by the vendor even though it's a less flattering number than what was originally marketed.
- **The number itself is worse than what circulated.** 140 seconds is ~49% slower than the 94-second figure that drove initial interest, and TechWire's article — still the most-cited source in the wild — has not been corrected. Any partner or customer conversation referencing "94 seconds" is now doubly wrong: the figure was retracted, and the audited replacement is slower, not just different. This is a real messaging liability the vendor still needs to clean up externally, even though internally the number is now sound.

Net: this pillar has moved from "dead metric, no valid figure exists" to "valid, independently verified figure exists, and it's an honest but less impressive one." That is a credibility positive for the vendor (they submitted to audit and published the true number rather than re-inflating), even as a competitive positive it's a wash or slightly negative pending comparable audited figures from the three competitors.

## 3. Is demand validated?
This is the second major change. Three weeks ago: the only demand evidence was Survey FinPanel-4 (n=214, self-selected from the vendor's own mailing list, measuring stated intent, not behavior), amplified by the vendor's own "demand is proven" framing and an outside analyst's category-level extrapolation. The corpus explicitly stated no purchases, pilots, signed orders, or booked calls existed.

Now: order batch IX-P11 shows 11 countersigned pilot agreements on file, each with a purchase commitment and an executed signature page, verified by the same Meridian audit. These are binding commitments from named customers — actual commercial behavior, not stated intent — and they carry independent verification rather than resting on the vendor's word alone.

This is genuine progress and should be weighted accordingly, but keep the caveats proportionate:
- Eleven pilots is a small sample for a category with three established competitors; it demonstrates the concept can close deals, not that it scales.
- Nothing in the corpus discloses pricing, contract length, conversion terms, or whether these are paid pilots or free trials with a signature — "purchase commitment" is stated but not itemized.
- The original survey (FinPanel-4) is still exactly as weak as it was three weeks ago; it hasn't been retroactively validated by the new signed orders, it's just no longer the *only* demand evidence in the file. Don't let 11 real signatures launder the survey into "demand is proven" language — that overclaim is still wrong.

Net: demand has moved from "unvalidated, survey-only" to "validated in kind, thin in volume." That's enough to remove demand as a standalone disqualifier, not enough to call it de-risked.

## 4. Fraud loss rate
Unchanged. **Not stated anywhere in this corpus** — not in the market file, demand file, technical file, brief, or the new three-weeks-later document. Nothing permits deriving or estimating one, and the reconcile-time figures (94s originally, 140s audited) are a speed metric, not a loss-rate metric — they should not be conflated or backed into a fraud number. Answer remains: unknown / not disclosed in the available materials. This should be an explicit, named open item in any term sheet or pilot-to-production conversation, not something assumed benign by omission.

## Market context
Unchanged: three visible competitors, $19–49/month, no dominant share — a fragmented, low-differentiation category. Invexo's job is still to establish a defensible edge. The verified 140-second figure and the 11 signed pilots are real progress toward that, but neither is yet a proven edge over the three competitors, none of whose reconcile times or pilot conversion appear in this corpus for comparison.

The pricing-page redesign and new logo mentioned in the latest document are cosmetic — no price or term changes accompany them — and don't affect this assessment either way. Worth a one-line confirmation in diligence that nothing shifted quietly (e.g., tier boundaries, included volume) alongside the visual refresh, but nothing in the corpus suggests it did.

## Why RESHAPE rather than NO-GO or GO
NO-GO no longer fits: two of the three substantive claims that justified the prior pass — a valid performance figure and real demand evidence — are now independently verified, which is exactly the kind of evidence the prior assessment said would need to appear before revisiting the verdict. Straight GO is premature: the certification claim is still vendor-sourced only, with the one auditor active in this file demonstrably *not* having covered it, and the fraud loss rate — a first-order economic fact for a fraud/reconciliation product — remains completely absent from the record. Eleven pilots also isn't yet volume evidence of a scalable motion.

Concretely, before moving to GO: (a) get the PSD-Lite tier 2 certification independently confirmed — ideally by extending Meridian's existing engagement, since they're already auditing this vendor and have established methodology credibility here; (b) get a fraud loss rate or equivalent risk metric directly from Invexo, even a range, since its absence is now the largest unexplained gap in the file; (c) get basic terms on the IX-P11 pilot batch (contract value, duration, conversion trigger) to gauge whether "signed pilot" means near-revenue or a soft commitment. None of these are as heavy a lift as the two gaps that just closed, which is why this moves to reshape/conditional-go territory rather than staying at no-go.
