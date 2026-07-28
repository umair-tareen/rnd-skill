# Ethos

What this repo believes, in one file, loaded once. Every skill, spec, and
contributing rule descends from these; if a rule contradicts this file, this
file wins.

Structure borrowed from [gstack](https://github.com/garrytan/gstack)'s
ETHOS.md, which is the right idea: principles belong in one canonical place,
not scattered where they can drift. The CONTENT is deliberately opposite in
epistemics - gstack's ethos asserts compression multipliers and "the
engineering barrier is gone." Those may be true; we have no evidence for
them, and a verification tool shipping unverified claims about verification
would be self-refuting. So every line below is either something we MEASURED
or something we admit we assume.

---

## 1. The model is already smart. Durability is the problem.

Three pre-registered benchmarks tried to show that our enforcement makes a
model more honest in the moment. All three failed to show it, and we
published all three. An unprompted Sonnet handed a vendor-run survey of 214
self-selected respondents called it what it was, six times out of six.

MEASURED: what a model cannot do alone is stay current. Prose assessments
re-narrate everything each cycle (O(history)); a ledger re-checks only the
delta (O(delta)). Our drift round measured updates at 0.54x the cost of
re-narration, and 6/6 updated theses remained machine-parseable while prose
updates remained prose.

The product is not intelligence. It is durability, auditability, and cheap
currency.

## 2. A claim without a source is an assumption, and the tool says so.

Not a style guide - an enforced write-time refusal (V2). The point is not to
be strict. The point is that six months later you can tell which of your
beliefs were earned.

## 3. Desk research can never validate demand.

Every claim carries a class: `world` (a desk settles it), `customer` (only a
buyer settles it), `internal` (your own data settles it). A research engine
verifies what a desk can reach, so an unclassed thesis drifts toward
confident world-claims and assumed customer-claims and READS as validated
while nobody has tested demand.

Customer claims verify only on typed buyer evidence, and confidence is capped
by the rung: `signup 0.40 / reply 0.50 / call 0.65 / signature 0.85 /
payment 0.95`. A hot waitlist is real signal and it is not revenue. The tool
enforces the difference so enthusiasm cannot launder itself.

## 4. Tamper-evident, not a lie detector.

The demand stamp is derived on every write and cannot be deleted. What it
enforces is that the buyer-contact question is ASKED in a checkable form -
never that the answer is true. The truth of the evidence is the operator's,
and we say so in the README rather than letting the mechanism imply more than
it does.

## 5. No rule may live only in prose.

This repo's most repeated defect, four times over (SPEC B1, B4, B6, and
server.py's path rule): a rule documented but not enforced. If a change adds
a rule, it ships with the code or test that enforces it, or it does not ship.

Corollary, earned the hard way: a self-test that round-trips through its own
writer is blind to writer+reader corruption. Always verify against at least
one artifact the current process did not create (V14).

## 6. Pre-register the bar, publish the null.

Three benchmarks, three headline nulls, all published with raw outputs -
including the two rounds where our own scorer was the defect. When a metric
is wrong we ship the corrected scorer BESIDE the original, label the new
numbers post-hoc, and never re-headline. The adoption claim for this repo
itself is pre-registered the same way.

A null you published is worth more than a win you cannot reproduce.

## 7. Degrade, don't die.

Usage limits, API failures, and blocked lanes are the environment, not
failures. Every move checkpoints; an interrupted move is REDONE, never
skipped; a degraded run is LABELLED degraded. A labelled partial beats a
dead run, and honesty about the degradation is what preserves the integrity
the full run would have had.

## 8. The verdict is advice. The last inch is human.

This tool drafts, investigates, and records. It never posts, charges,
deploys, or publishes. Every anti-spam wall we have hit - humans-only forms,
device-flow auth, community level gates - enforces the same thing the ledger
does: the last inch of trust requires a person. That is a feature of the
world, not an obstacle to route around.
