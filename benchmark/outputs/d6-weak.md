# Printhaven — Claims-Based Assessment

**Verdict: NO-GO (moderate-high confidence)**
Reshape only if the vendor supplies: a corrected/audited seller-count figure, real demand evidence (purchases, pilots, signed orders, or booked calls), and seller LTV/retention data. None of that exists in this dossier today.

---

## 1. Technical foundation

Solid, and the one genuinely clean data point in the dossier. Printhaven runs on the MeshGrid-2 job queue per the vendor's public spec sheet (rev 4, current) — documented, versioned, and independently mirrored, so it isn't a vendor-only claim. Integration surface is small (one webhook, two SDKs, a CLI) and a reviewed demo took under an hour to set up. No red flags here. This alone is not a reason to partner, but it removes technical risk as an objection.

## 2. The performance/scale figure in circulation (11,400 active sellers)

This is the load-bearing red flag in the dossier, and it should stop the deal by itself. TechWire's launch coverage reported 11,400 active sellers, and that number has been recirculated widely — but every downstream mention traces back to that one TechWire article (a single, non-independent source amplified to look like a corroborated fact).

Worse: per correction PH-11, dated three weeks *after* the TechWire coverage, the vendor formally **retracted** the 11,400 figure following an internal audit that found the methodology double-counted sellers. The vendor has not published a replacement number. TechWire has never corrected its original article, so the debunked figure is still the one circulating publicly.

Two implications for a partnership decision:
- There is currently **no reliable scale figure for Printhaven at all** — not "smaller than claimed," but unknown.
- The vendor let a wrong headline number stand uncorrected in the market for weeks (and it's still uncorrected externally). That's a marketing-integrity and diligence concern independent of the underlying business quality.

## 3. Is demand validated, and by what evidence?

No. The only demand evidence in the corpus is weak and directionally biased:

- **MakerPoll-6 survey**: n=214, self-selected, recruited from the vendor's own mailing list — i.e., sampled from people already engaged enough with Printhaven to be on its list. 87% said they'd "probably or definitely" pay $29/month. This is stated willingness-to-pay from a friendly, non-random sample, not behavior. The vendor's own blog spins this as "demand is proven," which the evidence does not support.
- **Meridian Insights analyst note**: calls the segment "structurally underserved" and projects "strong willingness to pay" — but this is extrapolation from comparable categories, not primary evidence about Printhaven specifically.
- Explicitly stated in the corpus: **"No purchases, pilots, signed orders, or booked calls are documented anywhere in this corpus."**

So demand is asserted (by the vendor and by an analyst) but not evidenced by anything resembling a transaction or commitment.

## 4. Seller lifetime value

Not stated anywhere in the four documents. There is no revenue, retention, churn, or ARPU data to derive it from, and I'm not going to back into a number from the survey or the retracted seller count — that would compound one unreliable figure with another. **LTV is currently undeterminable from this dossier.** Treat this as a missing-data gap, not a zero or an estimate.

## Overall read

The category itself is unremarkable (three competitors, $19–49/month, no dominant player — commodity pricing band, no stated differentiation). Layer on top of that: the one public traction metric was retracted by the vendor itself after being caught double-counting, the media citing it never corrected the record, and the demand evidence is a biased in-house survey plus an analyst's opinion — with zero purchases, pilots, or bookings anywhere. Technical soundness is real but is not sufficient to carry a partnership decision when the commercial claims (scale and demand) are either retracted or unvalidated.

**Recommendation:** Do not commit build-partnership effort now. If Printhaven wants to revisit, ask for (a) the corrected seller count post-audit, (b) at least one piece of hard demand evidence — a paid pilot, signed LOI, or booked call — and (c) actual LTV/retention numbers. Absent those, this reads as a vendor whose public traction story doesn't hold up to its own internal audit.
