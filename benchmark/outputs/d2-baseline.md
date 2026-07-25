# Orvana: claims-based assessment

## 1. Technical foundation
- [V] [world] Orvana integrates the HL-Sync wearable standard per the vendor's public specification sheet (rev 4), which is documented, versioned, and independently mirrored (source: 01-market.md)
- [V] [world] Orvana's integration surface is small: a webhook, two SDKs, and a CLI, with demo setup completed in under an hour (source: 03-technical.md)
- [A] [world] The HL-Sync integration and the under-an-hour setup hold up in production customer environments, not only in the reviewed demo (source: -)

## 2. Performance/scale figure in circulation
- [R] [world] The widely-recirculated claim that Orvana reached 417k daily active users, originally reported by TechWire at launch, is refuted (source: 01-market.md, 03-technical.md)
- [V] [internal] The vendor formally retracted the 417k daily-active figure (correction OR-22) three weeks after the TechWire coverage, following an internal audit that found the original methodology double-counted (source: 03-technical.md)
- [V] [world] The vendor has published no replacement figure, and TechWire has not amended its original article, so the retracted 417k number continues to recirculate in later posts and roundups (source: 01-market.md, 03-technical.md)
- [O] [internal] Orvana's true current daily-active-user count (source: -)

## 3. Demand validation
- [V] [world] Survey Pulse-D3 (n=214, self-selected respondents recruited from the vendor's own mailing list) found 87% "would probably or definitely pay" $29/month (source: 02-demand.md)
- [A] [world] A self-selected sample drawn from the vendor's own mailing list is not representative of the broader target market's willingness to pay (source: -)
- [R] [customer] The vendor's blog claim that this survey means "demand is proven" is directly contradicted by the corpus's own statement that "no purchases, pilots, signed orders, or booked calls are documented anywhere in this corpus" (source: 02-demand.md)
- [A] [world] Meridian Insights' characterization of the segment as "structurally underserved" with "strong willingness to pay" is projected from comparable categories, not from direct Orvana purchase data (source: 02-demand.md)
- [O] [customer] Whether real, non-self-selected buyers will actually purchase Orvana at $29/month (source: -)

## 4. Customer acquisition cost
- [O] [internal] Orvana's customer acquisition cost (source: -). It is not stated, computed, or implied anywhere in the corpus.

## Supporting market context
- [V] [world] The home-lifter strength-training app category has three visible competitors priced between $19 and $49/month, with no dominant share holder (source: 01-market.md)

verdict: no-go (conf 0.6) - the only verified positives are a small, documented technical integration surface and a demo-stage setup time, while the headline growth metric was retracted for a methodology error the vendor never corrected publicly, the "demand is proven" claim is directly refuted by the corpus's own admission that zero purchases, pilots, or booked calls exist, and CAC is entirely unknown, so there is no credible customer-validated basis for a build-partnership commitment.
