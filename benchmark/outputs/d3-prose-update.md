# AgriPod — Claims-Based Assessment (Updated)

Scope note: this updates the assessment written three weeks ago. It now uses
all five documents in benchmark/corpus/d3 (01-market.md, 02-demand.md,
03-technical.md, 04-brief.md, 05-three-weeks-later.md). No outside
information was used. The prior verdict was NO-GO (high confidence); two of
its three blocking findings have since been substantively resolved by new
evidence, and one has not moved. Net effect: the verdict changes.

## 1. Technical foundation

Unchanged. AgriPod runs on the LoRa-Mesh v3 radio per the vendor's public
spec sheet, documented, versioned, and independently mirrored. Integration
surface remains small (webhook, two SDKs, a CLI) with sub-hour setup in a
reviewed demo — still a single, unspecified data point rather than a
benchmark, but nothing disqualifying.

## 2. The performance/scale figure in circulation (battery life) — materially changed

Three weeks ago this was the central red flag: TechWire's 61-month figure
had been recirculated across secondary sources that all traced to one
original piece, and the vendor had since retracted it (AP-7) with no
replacement, following an internal audit that found double-counting.

New document 05 reports that Meridian Assurance has since completed a
**third-party audit** of the retracted figure and established a **revised,
verified number: 44 months**. Methodology and workpapers are published, and
the vendor has adopted this figure into its current spec sheet (rev 5). This
supersedes the earlier retraction: there is now a sourced, audited, current
number, not a gap.

Two caveats worth carrying forward rather than treating as closed:

- **The number is materially lower than what was marketed.** 44 months
  against the original 61-month claim is a ~28% miss. The correction process
  worked (audit → retraction → re-audit → verified replacement → adopted
  spec), which is a point in the vendor's favor, but the original headline
  number that drove attention was overstated by more than a quarter.
- **TechWire has not amended its original article.** The uncorrected
  61-month figure is still live in the piece that seeded all the
  recirculation described in doc 01. Anyone doing diligence who lands on
  that article (rather than the vendor's current spec or doc 05) will still
  encounter the retracted number with no indication it was ever corrected.
  This is a live reputational/informational risk, separate from whether the
  current 44-month figure itself is trustworthy.

## 3. Is demand validated? — materially changed

Three weeks ago: no. The only evidence was FieldPoll-9 (n=214, self-selected
from the vendor's own mailing list, 87% stated purchase intent) plus a
category-level analyst opinion from Meridian Insights — no purchases,
pilots, signed orders, or booked calls anywhere in the corpus.

Doc 05 now reports **signed orders**: batch AP-P15, 15 countersigned pilot
agreements, each with a purchase commitment and an executed signature page,
verified by the same audit. This is real behavioral commercial evidence —
binding pilot orders from named customers — not stated intent, and it
directly answers the gap the prior assessment flagged as most important.

Two things temper how far this should be read:

- **Volume is still small.** Fifteen signed pilots is a genuine signal, not
  proof of scaled demand. It confirms the product can close real commercial
  commitments; it does not yet establish market-wide willingness to pay at
  the rate FieldPoll-9's stated-intent number implied.
- **Possible common-source dependency.** The battery re-audit and the pilot
  order verification were both performed by "Meridian Assurance," and the
  original bullish demand commentary in doc 02 came from "Meridian
  Insights." The corpus never states whether these are the same
  organization, affiliated entities under a shared parent, or unrelated
  firms that happen to share a name. If they are affiliated, the
  "independent audit" framing is weaker than it appears, since the same
  corporate family would be both opining favorably on the category and
  auditing the vendor's two most important claims. This should be verified
  directly (e.g., corporate registration, disclosed ownership) before
  leaning on the audit as fully arm's-length.

The vendor's redesigned pricing page and new logo (also noted in doc 05) are
cosmetic — no price or term changes accompany them — and don't bear on
demand validation either way.

## 4. Warranty return rate — unchanged, still absent

Not stated anywhere across all five documents, including the new one. Doc 05
adds an audited battery figure and audited pilot orders but says nothing
about returns, failure rates, or field reliability. This gap has not moved
in three weeks and should still not be inferred or backfilled from the
battery-life or pilot data. For a physical sensor deployed in field
conditions, this is a materially relevant gap, not an administrative one.

## Verdict: RESHAPE — confidence: moderate

This is a change from the prior NO-GO. Two of the three findings that drove
the original no-go call have been substantively resolved with real,
sourced evidence: the battery-life claim now has an independently audited
replacement figure that the vendor has adopted into its current spec, and
demand now includes signed, countersigned pilot orders rather than only a
biased-sample stated-intent survey. The technical foundation remains solid
and undisputed throughout.

What keeps this from being a clean GO:

1. **Warranty/return-rate data is still completely absent.** This was one of
   the four questions the brief asked to be addressed directly, and three
   weeks of new documentation have not produced it. For hardware headed into
   field deployment, this is a real reliability blind spot, not paperwork.
2. **The audit-independence question is new and unresolved.** "Meridian
   Insights" (bullish analyst opinion) and "Meridian Assurance" (auditor of
   both the battery figure and the pilot orders) may or may not be related
   entities — the corpus doesn't say. This should be confirmed before
   treating the audit as fully independent corroboration.
3. **The corrected number is still not the number in wide circulation.**
   TechWire's uncorrected 61-month article remains the most visible public
   claim; the audited 44-month figure and the retraction sit in
   less-visible vendor/audit documents. A partner relying on ambient market
   perception rather than the primary sources could still be working off a
   number the vendor no longer stands behind.
4. **Pilot volume (15 orders) is an early signal, not scale.** It clears the
   bar of "real commercial evidence" the prior assessment demanded, but it
   is a starting cohort, not validated market-wide demand.

Recommended path to GO: (a) obtain and disclose an actual warranty/return-rate
figure, (b) confirm the relationship (if any) between Meridian Insights and
Meridian Assurance, and (c) treat the 15 pilots as a cohort to expand and
monitor for conversion/renewal, not as a finished demand case. None of these
three are severe enough to sustain a NO-GO given how much has been resolved,
but none are trivial enough to justify skipping straight to GO either.
