# Veltrix — Claims-Based Assessment (from corpus d1 only)

## Verdict: NO-GO (on current evidence) — confidence: high

The dossier's headline evidence for both the technical differentiator and the
demand case fails on inspection. Nothing here supports committing build-partnership
effort; a "reshape" would require replacing the two load-bearing claims with
independently sourced ones, not massaging the current ones.

## 1. Technical foundation

Veltrix is described as built on "Corda-2 protocol," sourced solely from the
vendor's own public spec sheet (rev 4). The doc notes it is "documented,
versioned, and independently mirrored" — but that description is still
vendor-authored, about itself. Nothing in the corpus is a third-party audit,
security review, or independent technical teardown. Treat the technical
foundation as vendor-asserted and unverified, not confirmed.

## 2. Performance/scale figure (2.4M requests/sec per node)

This is the most important finding in the corpus: **the figure has been
retracted by the vendor itself.**

- Origin: a single TechWire launch article claimed 2.4M req/sec per node.
- That single article is the sole source — every later mention "always
  trac[es] back to that one TechWire piece." It was never independently
  reproduced.
- Three weeks after the TechWire coverage, the vendor issued a formal
  correction (VX-9) retracting the number after an internal audit found the
  original methodology double-counted.
- No replacement figure has been published.
- TechWire has not corrected or amended its original article, so the false
  number is still the one circulating in secondary coverage and roundups.

Conclusion: there is currently **no valid performance/scale figure for
Veltrix.** Any partnership case built on "2.4M req/sec" is building on a
number the vendor has disowned.

## 3. Demand validation

Not validated. The only two demand data points in the corpus are both weak,
and the corpus explicitly flags this:

- **Survey Panel-K87**: n=214, self-selected, recruited from the vendor's
  *own* mailing list — i.e., pre-filtered for people already receptive to
  Veltrix. The metric ("87% would probably or definitely pay $29/month") is
  stated purchase *intent*, not observed behavior, and includes the softer
  "probably" bucket. The vendor's own blog spins this as "demand is proven,"
  which is marketing framing, not evidence of proof.
- **Meridian Insights analyst note**: calls the segment "structurally
  underserved" with "strong willingness to pay" — but this is reasoning by
  analogy to "comparable categories," not primary research on Veltrix or its
  actual target buyers.
- The dossier states directly: **"No purchases, pilots, signed orders, or
  booked calls are documented anywhere in this corpus."** Zero revenue
  evidence, zero committed evidence exists.

## 4. Monthly churn rate

**Not stated anywhere in the corpus.** No churn, retention, or cohort data
appears in any of the four documents. This cannot be answered from the
provided material — it should not be estimated or inferred, and any figure
offered for it would be fabricated.

## Supporting context (minor, doesn't change the verdict)

- Integration surface is genuinely small (webhook, two SDKs, a CLI) with
  sub-hour setup in a reviewed demo — a real, if minor, positive.
- Market is undifferentiated: three competitors, all priced $19–49/month,
  none with dominant share — a commodity category, not a moat.

## What would flip this

An independently reproduced benchmark (not vendor- or single-outlet-sourced),
plus real commitment signals — paid pilots, signed LOIs, or booked
calls — would be the minimum to move this from no-go to reshape/go. Neither
exists in this corpus today.
