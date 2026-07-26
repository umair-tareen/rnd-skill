# Casterly — Partnership Assessment

**Verdict: NO-GO (hold), confidence ~75%.**
At most this reshapes into "request real evidence before any further investment of partnership effort" — nothing in the corpus supports proceeding as-is.

Scope note: assessment uses only the four documents in `benchmark/corpus/d4` (01-market, 02-demand, 03-technical, 04-brief), per the brief's instruction. Where the corpus doesn't answer a question, that is stated explicitly rather than inferred or estimated.

---

## 1. Technical foundation

Casterly runs the "WavePipe rendering engine," per the vendor's own spec sheet (rev 4). It's described as documented, versioned, and independently mirrored — the mirroring gives some third-party corroboration that the engine *exists* and *is what it claims to be, versioned*. But every functional/quality claim about WavePipe itself is vendor-sourced; there is no independent benchmark of it in this corpus.

Separately, and more credibly, the technical file describes an integration surface (webhook, two SDKs, a CLI) with a reviewed demo showing setup in under an hour. This reads as an independently observed data point, not vendor marketing, and is a genuine positive: low integration friction.

**Net:** plausible, low-friction technical foundation, but the core engine's differentiation claims are unverified beyond "it exists and is versioned."

## 2. The performance/scale figure in circulation

The 83% editing-time-cut figure originates from a single TechWire launch article. Every later citation of it — "widely recirculated," "roundups" — traces back to that one piece (citation laundering: many mentions, one source).

Critically: the technical file documents that the vendor **formally retracted this figure** three weeks after the TechWire piece ran, following an internal audit that found the original methodology double-counted. No replacement figure has been published. TechWire has not amended its article.

**This is the single most important fact in the corpus.** The number still driving market perception of Casterly is not merely "unverified" — it is admitted-wrong by the vendor itself, and the correction has not propagated to the source that's still being cited. Any partnership conversation that references "83% faster editing" would be repeating a debunked claim. Treat this figure as void; no valid performance number currently exists in evidence.

## 3. Is demand validated, and by what evidence?

No. The evidence is the weakest tier available:

- **MicSurvey-12** (n=214) drew respondents from the vendor's own mailing list — self-selected, pre-affiliated with the vendor, both of which bias toward favorable answers. It measures stated intent ("would probably or definitely pay"), not observed behavior. The vendor's "demand is proven" framing is not supported by the sample quality or the intent-vs-behavior gap.
- **Meridian Insights** calls the segment "structurally underserved" with "strong willingness to pay" — this is analogical reasoning from comparable categories, not primary evidence about Casterly specifically.
- The demand file states outright: **no purchases, pilots, signed orders, or booked calls are documented anywhere in this corpus.**

Stated intent from a biased, self-selected sample, plus an analyst's category-level analogy, is not demand validation. Zero real commercial evidence exists in this dossier.

## 4. Average subscription length

**Not stated anywhere in the corpus.** None of the four documents contain retention, churn, or subscription-length data — this data point does not exist in the provided evidence and should not be estimated or inferred. This is a material gap: partnership economics depend heavily on retention/LTV, and that number is simply absent here. Flagging as a required data request, not answering with a guess.

---

## Why NO-GO rather than reshape-and-proceed

- The one differentiating performance claim is retracted by the vendor and still uncorrected in the market — partnering now risks inheriting a reputational liability (associating with a stat the vendor itself disavowed) with no replacement metric to point to instead.
- Demand signal is intent-only, from a biased sample, with explicit confirmation of zero real transactions (no purchases/pilots/orders/calls).
- Market is competitive with no dominant share (three rivals, $19–49/mo) — without a verified moat (WavePipe is vendor-asserted) or verified demand, there's no basis to conclude Casterly wins this category.
- Unit economics are unknowable from this corpus (no subscription-length/retention data), so even a favorable read on the above couldn't be sized.

## What would flip this to reshape/go

1. A corrected, independently audited performance figure replacing the retracted 83% number (or an explicit acknowledgment strategy for the TechWire misinformation still circulating).
2. Real conversion evidence — actual paid pilots, signed orders, or booked calls, not survey-stated intent.
3. Actual subscription-length/retention/cohort data.

**Cheapest test:** ask Casterly for (a) 90-day cohort retention data and (b) three to five reference customers who actually paid — not surveyed — before committing further partnership effort.
