# Veltrix — claims-based assessment

## 1. Technical foundation
- [V] [world] Veltrix is built on the Corda-2 protocol, per the vendor's public specification sheet (rev 4, current), which is described as documented, versioned, and independently mirrored (source: 01-market.md)
- [V] [world] Veltrix's integration surface is small (one webhook, two SDKs, a CLI), and a reviewed demo completed setup in under an hour (source: 03-technical.md)
- [A] [world] The technical foundation (protocol) claim is unaffected by the separate retraction of the performance figure, since they come from distinct documentation sources with no stated link between them (source: -)

## 2. Performance/scale figure in circulation
- [V] [world] TechWire's launch coverage reported that Veltrix processes 2.4M requests/sec per node (source: 01-market.md)
- [V] [world] The 2.4M requests/sec figure is single-sourced: all later posts and roundups recirculating it trace back to that one TechWire piece (source: 01-market.md)
- [R] [world] The vendor formally retracted the 2.4M requests/sec figure (correction VX-9, issued three weeks after the TechWire coverage) after an internal audit found the original methodology double-counted requests (source: 03-technical.md)
- [V] [world] The vendor has published no replacement or updated performance figure since the retraction (source: 03-technical.md)
- [V] [world] TechWire has not amended its original article to reflect the retraction, so the debunked 2.4M figure remains the number still in public circulation (source: 03-technical.md)

## 3. Whether demand is validated, and by what evidence
- [V] [internal] A vendor-run survey (Panel-K87, n=214, self-selected respondents recruited from the vendor's own mailing list) found 87% said they "would probably or definitely pay" $29/month (source: 02-demand.md)
- [R] [customer] The vendor's blog claim that this survey means "demand is proven" for Veltrix (source: 02-demand.md)
- [V] [world] Meridian Insights' analyst note calls the segment "structurally underserved" and projects "strong willingness to pay," but this projection is based on comparable categories, not primary research on Veltrix or its actual buyers (source: 02-demand.md)
- [V] [customer] No purchases, pilots, signed orders, or booked calls for Veltrix are documented anywhere in the corpus (source: 02-demand.md)
- [R] [customer] Demand for Veltrix has been validated through real buyer interaction (source: 02-demand.md)

## 4. Monthly churn rate
- [O] [internal] Veltrix's monthly churn rate — no figure, proxy, or discussion of churn/retention appears anywhere in the corpus; cannot be stated (source: -)

## Supporting market context
- [V] [world] The API-gateway-for-small-SaaS-teams category has three visible competitors priced $19-$49/month with no dominant share, and Veltrix's tested price point ($29/month) sits within that existing range (source: 01-market.md)

verdict: no-go (conf 0.6) - the one concrete scale claim in circulation was retracted by the vendor itself and never replaced while third-party coverage remains uncorrected, and the vendor's "demand is proven" line rests solely on a self-selected in-house mailing-list survey with zero purchases, pilots, or booked calls anywhere in the corpus, plus churn is entirely unknown, and this combination of an overclaiming pattern with unvalidated demand and unknown retention economics is too risky to commit build-partnership effort to now.
