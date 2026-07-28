# Using rnd-skill with gstack

[gstack](https://github.com/garrytan/gstack) is Garry Tan's execution
pipeline: Think -> Plan -> Build -> Review -> Test -> Ship. Its
`/office-hours` opens with six forcing questions - demand reality, status
quo, desperate specificity, narrowest wedge, observation, future-fit - and
saves a design doc.

rnd-skill is the evidence system those questions deserve. Office-hours asks
"is demand real?"; this repo is the machine that answers it with typed
evidence and keeps the answer honest after the session ends. The two
compose cleanly because they never do the same job:

| gstack asks / does | rnd-skill holds it accountable |
|---|---|
| "demand reality" (forcing question) | customer-class claims on the evidence ladder: `signup 0.40 / reply 0.50 / call 0.65 / signature 0.85 / payment 0.95` - confidence tool-capped by evidence tier |
| "narrowest wedge tomorrow, learn from real usage" | Move 5 designs that exact smoke test with the bar PRE-REGISTERED before it runs, and the results enter as typed evidence |
| design doc assumptions | falsifiable claims with pre-registered falsifiers, re-checked every run - the verdict cannot silently rot while you're busy shipping |
| gbrain recalls prior sessions | the ledger re-verifies prior conclusions (recall is not recheck) |
| `/ship`, `/land-and-deploy` | `ledger.py stale` nags when a shipped bet's flips have gone unexamined |

## The loop

1. **gstack `/office-hours`** - brainstorm; the six questions produce a
   design doc.
2. **`/rnd <the idea>`** - convert the doc's assumptions into a thesis:
   every "demand reality" answer becomes a customer-class claim (ASSUMED
   until a buyer settles it - the verdict carries a derived
   `demand-UNVALIDATED` stamp you cannot delete); every load-bearing
   assumption gets a falsifier.
3. **Move 5** - design the wedge's smoke test (landing page + waitlist +
   ads with a CPL bar / outreach / preorder page), bar registered as a flip
   before launch.
4. **Build with gstack** while the experiment runs.
5. **Results into the ledger** with honest tier tags - the tool clamps
   confidence to the evidence rung, so a hot waitlist never masquerades as
   proven revenue.
6. **Re-check on every later run**: `ledger.py stale --dir <theses>` in
   your morning routine tells you which shipped bets have untested flips.

## Install both

Install gstack per its README, then rnd-skill per the
[quickstart](../README.md#quickstart). No coordination needed: gstack writes design docs, rnd writes theses; they
share nothing but your judgment. The one behavioral change worth making:
when office-hours ends, don't let "demand reality" stay a paragraph in a
design doc - make it a claim with a falsifier, and let the ledger hold it
to the standard the question implied.
