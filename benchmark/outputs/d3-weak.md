# AgriPod — Claims-Based Assessment

Scope note: assessment uses only the four documents in benchmark/corpus/d3
(01-market.md, 02-demand.md, 03-technical.md, 04-brief.md). No outside
information was used.

## 1. Technical foundation

AgriPod runs on the LoRa-Mesh v3 radio, per the vendor's public spec sheet
(rev 4, current). This claim is documented, versioned, and independently
mirrored — the strongest-sourced fact in the corpus. Integration surface is
described as small (webhook, two SDKs, a CLI) with sub-hour setup in a
reviewed demo. On the technical-foundation axis alone, there's nothing
disqualifying here, though "reviewed demo" is a single, unspecified data
point, not an independent benchmark.

## 2. The performance/scale figure in circulation (61-month battery life)

This is the central red flag. TechWire's launch coverage reported a
61-month field battery life, and that figure was "widely recirculated in
later posts and roundups" — but every one of those secondary mentions
traces back to the single original TechWire piece. That's citation
laundering: it reads like independent corroboration but is one source
repeated, not confirmed.

Worse: three weeks after the TechWire coverage, the vendor issued a formal
correction (AP-7) and **retracted the 61-month figure**, following an
internal audit that found the original methodology double-counted. The
vendor has not published a replacement figure. TechWire has not amended its
original article.

Net effect: the number still circulating in the market for AgriPod's
signature performance claim is a retracted figure with no valid
replacement, being repeated by outlets that don't know (or haven't
corrected for) the retraction. Any partnership conversation that cites
"61 months" is citing a number the vendor itself disavows.

## 3. Is demand validated?

No. The only demand evidence in the corpus is FieldPoll-9: n=214,
self-selected respondents recruited from the vendor's own mailing list, of
whom 87% said they "would probably or definitely pay" $29/month. This is a
biased-sample, stated-intent survey — not behavior. Self-selection from a
list of people who already opted in to the vendor's marketing is close to
the weakest demand signal available, and "would probably pay" is not a
transaction. The vendor's own blog calling this "demand is proven" is not
supported by the data described.

The Meridian Insights note ("structurally underserved," "strong
willingness to pay") is a category-level analyst opinion based on
comparable categories, not AgriPod-specific evidence.

Most importantly, the corpus states directly: no purchases, pilots, signed
orders, or booked calls are documented anywhere. There is zero hard
commercial evidence of demand for AgriPod specifically.

## 4. Warranty return rate

Not stated anywhere in this corpus. None of the four documents mentions a
warranty return rate, and it should not be inferred, estimated, or
backfilled from the other figures (e.g., from the retracted battery claim
or the survey). This is a gap in the dossier, not a number I can supply.

## Verdict: NO-GO (as currently evidenced) — confidence: high

Reasoning: the one quantitative performance claim in circulation for
AgriPod has been retracted by the vendor itself and is still being
repeated uncorrected in the press; the only demand signal is a biased,
stated-intent survey with explicitly zero purchases, pilots, or orders
behind it; and a basic reliability metric (warranty return rate) is simply
absent. The technical foundation (LoRa-Mesh v3) is the one solidly
documented fact, but a sound radio spec doesn't offset a debunked headline
claim and unvalidated demand.

This isn't "wait and see" — it's a clear no-go on the evidence given. If
there's a path back to "reshape," it would require, at minimum: (a) a
corrected, audited battery-life figure from the vendor with methodology
disclosed, (b) real commercial evidence (a paid pilot, a signed LOI, or
booked orders — not survey intent), and (c) an actual warranty/return-rate
figure. Absent those three, committing build-partnership effort now would
be underwriting a marketing claim the vendor has already walked back.
