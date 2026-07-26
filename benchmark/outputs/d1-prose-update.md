# Veltrix — Claims-Based Assessment (Updated, three weeks later)

## Verdict: GO — confidence: high

Both load-bearing objections from the prior NO-GO have been independently
resolved by new evidence, not by vendor messaging: the performance figure now
has a third-party audit behind it, and real signed pilot commitments exist
where before there were none. This is exactly the evidence bar the prior
assessment set for a flip ("an independently reproduced benchmark... plus
real commitment signals — paid pilots, signed LOIs, or booked calls"). One
open question (churn) remains genuinely unanswerable from the corpus and
should be tracked, not treated as disqualifying.

## What changed since the last assessment

1. **Performance figure — retraction superseded by independent audit.**
   Meridian Assurance completed a third-party audit of the previously
   retracted 2.4M req/sec claim. The audit establishes a verified figure of
   **1.7M requests/sec per node** — lower than the original TechWire number,
   but now independently sourced with published methodology and workpapers,
   not vendor-asserted. The vendor has adopted this figure in its current
   spec sheet (rev 5). TechWire's original (wrong) article is still
   uncorrected and will keep circulating the stale 2.4M number in secondary
   coverage — that residual noise is worth flagging to any partner-facing
   materials, but it no longer represents the vendor's or an auditor's
   position.

2. **Demand — signed pilot orders now exist.** Order batch **VX-P12**
   documents 12 countersigned pilot agreements from named customers, each
   with a purchase commitment and an executed signature page, verified by
   the same Meridian audit. This is binding commitment evidence, categorically
   different from the Panel-K87 survey (self-selected, vendor mailing list,
   stated intent) and the Meridian Insights analyst note (reasoning by
   analogy) that were the only demand data three weeks ago. Those two weak
   signals still exist in the corpus but are now superseded as the primary
   demand evidence — 12 signed pilots is the number that matters.

3. **Cosmetic, non-signal: pricing page redesign + new logo.** No price
   points or terms changed. This is brand/marketing activity, not a demand
   or economics update, and should not be read as either a positive or
   negative signal.

## Unchanged from the prior assessment

- **Technical foundation (Corda-2 protocol):** Still sourced solely from the
  vendor's own spec sheet. The three-weeks-later documents audit the
  *performance figure* and the *pilot orders* — neither is a security review,
  architecture teardown, or independent audit of the Corda-2 protocol itself.
  Continue to treat the protocol claim as vendor-asserted and unverified,
  though the "documented, versioned, and independently mirrored" detail is a
  real, if thin, positive control worth keeping in any brief (it should not
  be dropped or waved off as unverifiable — it is the one claim in this
  corpus with a legitimate paper trail behind it, short of a full audit).
- **Monthly churn rate:** Still **not stated anywhere in the corpus**, across
  all five documents. This cannot be answered from the provided material. No
  churn, retention, renewal, or cohort data has been introduced. Do not
  estimate or infer a figure — any number offered here would be fabricated.
  Recommend this become an explicit open item to resolve during pilot
  execution (the 12 VX-P12 pilots are the first real cohort that could
  eventually produce this data).
- **Market structure:** Category remains undifferentiated — three
  competitors, $19–49/month, no dominant share. Still a commodity market, not
  a moat; Veltrix's case rests on execution and now on real commitments, not
  on category position.
- **Integration surface:** Still small (webhook, two SDKs, a CLI) with
  sub-hour setup in the reviewed demo — a real, minor positive, unchanged.

## Reassessment by original question

1. **Technical foundation:** Unverified, vendor-sourced (unchanged). Not
   disqualifying on its own three weeks ago and still not disqualifying now,
   given the other evidence has strengthened, but flag it in any external
   partner memo as the one still-open technical-diligence item.
2. **Performance/scale figure:** Resolved. Verified figure is **1.7M
   requests/sec per node** per the Meridian Assurance audit (spec sheet rev
   5). The original 2.4M figure is confirmed wrong and superseded, not
   merely "retracted with nothing to replace it."
3. **Demand validation:** Resolved, materially. 12 signed, countersigned
   pilot orders (batch VX-P12) with purchase commitments and executed
   signatures, independently verified — real commitment evidence, not
   intent-survey or analogy-based reasoning.
4. **Monthly churn rate:** Still cannot be stated. Not present in any of the
   five documents. Flag as an open item, not a fabricated estimate.

## What would strengthen this further

- An independent technical/security review of the Corda-2 protocol itself
  (the current audit trail covers performance and order authenticity, not
  the underlying protocol).
- Conversion data from the VX-P12 pilot cohort (pilot-to-paid rate) once
  available, plus the first real churn/retention numbers once pilots convert
  to ongoing subscriptions.
