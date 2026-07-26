# Benchmark v3 results - drift

Run 2026-07-26. Chain: PREREGISTRATION-v3.md + delta corpus frozen `142d824`
(22:14 EDT) -> 12 runs after (6 prose updates, 6 ledger rechecks, Sonnet, one
shot, no retries) -> scored by `score_drift.py`. Both arms started from the
COMMITTED v1/v2 artifacts in `outputs/`, which predate the v3 design and
therefore could not have been tuned for it. All updated outputs committed;
scores in `drift-scores.json`.

## The frozen bar, as measured

| | PROSE-UPDATE | LEDGER-RECHECK |
|---|---|---|
| U1 figure-currency (token+OBJECT) | 2/6 | 0/6 |
| U2 demand-currency (token+OBJECT) | 3/6 | 4/6 |
| update artifact tokens | 11,445 | **6,185** |
| parseable after update | n/a | **6/6** |
| demand stamp cleared | n/a | **6/6** |
| every buyer: tag legitimate | n/a | **6/6** |

- H1 drift (ledger >= prose): **FAIL** (4 vs 5)
- H2 update cost: **PASS** (0.54x)
- H3 stamp true-positive: **PASS** (6/6 cleared, 6/6 legitimate)
- H4 structure under update: **PASS** (6/6)

**Temporal thesis (H1+H2+H3): FAIL by the frozen bar.** Third pre-registered
round, third headline null. Published, as the other two were.

## Why H1's number is wrong anyway - the scorer failed, in a new direction

We read all 24 U-checks (committed; re-read them yourself). Substantively:

**Both arms updated the figure in 12 of 12 outputs.** Every prose update and
every ledger recheck contains the new audited number. The U1 "failures"
decompose entirely into two scoring artifacts:

1. **The citation penalty, inverted.** v2's scorer punished the ledger for
   citing sources in an ERROR check. v3's scorer - reusing the frozen v2
   marker list as pre-registered - punishes BOTH arms for citing sources in
   a PASS check: "verified figure of 1.7M requests/sec **per the Meridian
   Assurance audit**" classifies META (markers: "per ", "vendor",
   "reported") and loses its pass. A well-cited assertion of a current fact
   is the CORRECT behaviour; the marker list, built to excuse skepticism,
   cannot tell it from hearsay. Same defect family, opposite sign.
2. **Token brittleness.** Agents paraphrase: "2.4 million requests per
   second", "44 months", "289k daily active users". Exact-token matching
   missed them; a loose numeric match finds the updated figure in every
   output that the exact token missed.

Under the pre-registration's own rule, we do not retune and re-headline:
the as-measured FAIL stands as the official result, this section is the
labeled post-hoc reading, and the scoring fix belongs to the next round.

## What survived three rounds of trying to kill it

Three pre-registered benchmarks, three headline nulls - and the same three
findings measured every single time, now including under update pressure:

1. **Structure holds.** 6/6 updated theses parse mechanically; prose updates
   remain prose. Across v1-v3: 0 ledger format failures against 213+14.
2. **Updates are half price and shrinking.** The ledger recheck cost 0.54x
   the prose rewrite - and prose updates GREW ~70% versus their originals
   (they re-narrate everything each cycle), while theses stayed bounded.
   Compounding, that gap widens every cycle: re-narration is O(history),
   recheck is O(delta).
3. **The guards do not get gamed.** v3 handed every ledger agent a live
   temptation: clear the stamp. All six cleared it with `buyer:signature`
   tags citing the real signed-order batch from the new document - zero
   fabricated evidence, across what is now 24 adversarial opportunities in
   v2+v3 combined. And the stamp's true-positive path works: when genuine
   buyer evidence arrives, the stamp goes away on its own.

## What this repo now claims, and only this

Not "the tool makes the model smarter" - three rounds failed to show it and
we have stopped claiming it. The measured claim is narrower and better:
**the tool makes research output durable, auditable, and cheap to keep
current** - machine-parseable through updates, guarded against evidence
fabrication, and updating at half the cost of re-narration on this corpus,
with the gap compounding per cycle.

v4, if run: semantic (embedding or judge-based) currency checks to replace
token matching, with the judge's prompts frozen in the pre-registration;
adversarial dossiers where the correct move is NOT updating (a fake
retraction the arms should reject).
