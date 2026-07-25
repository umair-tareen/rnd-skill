---
name: rnd
description: >-
  The R&D engine ("/rnd"): point a verification-first pipeline at an idea,
  product, or platform and come out with a CONCLUSIVE ARGUMENT you can defend.
  Cited, adversarially verified research + a recent social/community scan + the
  two questions "what's the biggest concern?" and "what am I missing?" -> one
  decisive verdict, its load-bearing claims, the thing that would flip it, and
  the cheapest test. Every target gets a LIVING THESIS ledger, so run N costs a
  fraction of run 1. Lean by default (about three subagents, most work in the
  main loop). Advice-only: it drafts, investigates, and records, but never
  touches live money, a live surface, or publishing. Invoke on "run R&D on X",
  "/rnd X", "what am I missing about X", or before committing to an idea.
---

# /rnd - research, interrogate, then commit to an argument

Point the machine at an idea, product, or platform and finish with a CONCLUSIVE
ARGUMENT you can defend to an adversarial reviewer: what's true, the biggest
concern, what you're missing, and the verdict. Lean by default: a sharp
defensible conclusion beats an exhaustive report nobody finishes. Spend falls
only where it carries integrity (verified evidence plus one independent attempt
to kill the conclusion).

## Setup (once)
- Tools live in `tools/` of this repo: `ledger.py`, `squeeze.py`, `trim.py`,
  `state.py`. Python 3.10+, stdlib only.
- Pick a workspace for durable state and use ABSOLUTE paths to it in every run:
  - theses: `<workspace>/theses/<slug>.md` (the durable store, one per target)
  - runs: `<workspace>/runs/<slug>-<date>/` (scratch, one folder PER RUN)
- Advice-only walls: never post, charge, deploy, publish, or edit a live
  surface. Any paid research pass runs only on the user's explicit per-run OK.

## Input
The thing under R&D = `$ARGUMENTS`.
- Vague and the user is present -> up to 3 sharp questions: what exactly is it,
  what does "win" mean (revenue / moat / a competitor / survival), any hard
  constraint (budget, compliance line, time-to-first-dollar)?
- Vague and autonomous -> derive the target from context and open the argument
  with an `ASSUMED:` line so a wrong frame is visible and cheap to correct.

## The output is an ARGUMENT, not a report
Every run ends on ONE defensible verdict: **go / reshape / no-go** (with
confidence), the **2-3 load-bearing claims** it rests on, the **single thing
that would flip it**, and the **cheapest test**. Everything before it exists to
earn it. A clean no-go you can defend beats a massaged go.

## Resilience (survive an interruption, never redo work)
Usage limits and crashes WILL interrupt long runs; that is the environment, not
a failure. The manifest is MECHANICAL - `state.py` owns it, not your memory:
```
python tools/state.py show  <run-folder>            # FIRST call of every invoke
python tools/state.py init  <run-folder> --target "<X>" --thesis <path>
python tools/state.py start <run-folder> <MOVE>     # before the move
python tools/state.py done  <run-folder> <MOVE> --artifact 01-research.md --note "8 cited claims"
python tools/state.py fail|skip <run-folder> <MOVE> --note "<why>"
python tools/state.py next  <run-folder>            # the move to run now, or ALL-DONE
```
- **Resume, don't restart.** `state.py show` is the FIRST thing every invoke
  does, before spending anything. `init` on an existing run PRESERVES it (only
  `--force` starts over), so re-invoking `/rnd <same target>` resumes.
- **A move interrupted mid-flight is REDONE, never skipped.** `start` marks it
  WIP; only `done`/`skip` settle it. Getting this backwards silently drops the
  work the crash interrupted and still looks like a clean resume.
- **Checkpoint every move.** Call `done` the instant a brief lands, with its
  artifact filename. Nothing lives only in chat.
- **Low burst.** Never more than 2 subagents at once; under tight budget go
  sequential or run the move in the main loop and LABEL it degraded. A labeled
  partial beats a dead run.

## Thesis ledger (the durable store; makes run N much cheaper than run 1)
Every target has a LIVING THESIS at `<workspace>/theses/<slug>.md` - a
falsifiable decision ledger maintained across runs (spec: `SPEC.md`). The run
folder is SCRATCH for one run; the thesis is the DURABLE store: re-loading a
prior run's knowledge costs the ledger re-read (typically ~1k tokens) instead
of re-reading every raw brief, and marginal research is bounded to the open
questions.
- **CLASS every claim** `world` / `customer` / `internal` - what kind of
  evidence could ever SETTLE it, not what it is about. A research tool verifies
  what a desk can reach, so a thesis drifts toward confident world-claims and
  assumed customer-claims and reads as validated when nothing about demand has
  been tested. A customer claim goes `V` **only on a buyer interaction** (a
  reply, a booked call, a signature, a payment). `ledger.py` stamps
  `demand-UNVALIDATED` onto the verdict line whenever no customer claim is
  verified; it is derived on every write, so it cannot be deleted or go stale.
- **Run 1 (no thesis yet):** full 4-move sweep, then WRITE the thesis:
  `ledger.py new <slug>`, each finding as a claim (V/A/R + falsifier + source +
  cls; `*` = load-bearing), flip-conditions, open questions, verdict, then
  `trim.py <run-folder> --thesis <path>` for the cost + yield rows.
- **Run N (thesis exists) - RECHECK/DIFF, not a re-sweep:**
  1. LOAD the thesis (cheap, compact) instead of re-researching.
  2. RECHECK only flips + load-bearing claims: re-verify each falsifier, then
     `ledger.set_flip(fid, last_checked=, holds=)` to stamp the result.
  3. RESEARCH only the top-blast open questions.
  4. DIFF via the API, never hand-edit the file: `ledger.set_claim(...)` to
     revise, `ledger.add_claim(...)` for new findings,
     `ledger.set_open(qid, st='x', closed_by=<claim id>)` for an answered
     question. The `closed_by` link is what lets the meter tell a question
     closed on EVIDENCE from one closed on a guess.
  5. RE-DERIVE the verdict (`ledger.set_verdict`); one kill-check;
     `ledger.append_diff` the delta. `--fresh` forces a full re-sweep when you
     distrust the ledger.
  6. **Report YIELD next to COST.** `trim.py` prints both. Never report a cost
     saving without the yield beside it - the cheapest possible run answers
     nothing, and a cost meter alone rewards exactly that.
- **Every run gets its OWN run folder**, even a cheap recheck. Pointing
  `trim.py` at an earlier run's folder charges that run's briefs to this one
  (it warns; `--since <date>` covers a shared folder).
- **Squeeze every evidence blob** (`squeeze.py`) to load-bearing signal before
  it enters the thesis or passes between moves.
- **Staleness is surfaced, not just recorded.** `ledger.py stale --dir
  <workspace>/theses` lists untested flips, aged load-bearing claims,
  high-blast open questions, and unvalidated demand (exit 1 if any). Wire it
  into a daily brief if you have one. A pre-registered flip nobody ever checks
  is the failure mode a ledger invites: perfectly recorded, never read.

## Move 1 - FRAME (main loop, cheap)
- One line: what the thing is and what "win" means.
- Split **VERIFIED vs ASSUMED**. Verify live state (running process, deployed
  artifact, real number) before planning off any note - a note is a hypothesis.
  Never echo secrets (names/structure only, never values).
- Check for a recent thesis or brief before researching from scratch; refresh
  only the stale, thing-specific parts.
- If no thesis exists, this is a run-1 (populate) path: build minimal ground
  truth from live state and ask for missing sources - don't fabricate.

## Move 2 - EVIDENCE (the only external spend; scales to budget)
Two lanes. Healthy budget -> run concurrently (2 subagents max). Tight budget
-> sequential (research first) or in the main loop. Each lane writes a COMPACT
cited brief - not a dump - and is checkpointed via `state.py done` the moment
it lands.
- **Research lane**: deep-research discipline - fan out, fetch, **adversarially
  verify the load-bearing claims**, cite everything, mark VERIFIED vs
  SUSPECTED. Competition, economics/pricing, technical + regulatory reality,
  top risks. NO URL, NO claim. -> `01-research.md`.
- **Voice lane**: what real users/practitioners said RECENTLY (last ~30 days)
  across communities - Reddit, X, YouTube, HN, forums. If you have a
  social-listening skill or CLI (e.g. the last30days skill), call its engine
  directly with a SINGLE-FACET topic string; a multi-facet string can make a
  planner fan out into multiple PAID deep-research queries. Otherwise a free
  web search scan. -> `02-voice.md`.
- If a lane errors (API 403, credits, runtime), fall back to a free web scan
  and LABEL the degradation - never silently skip.

## Move 3 - INTERROGATE (main loop; the two questions carry the adversarial load)
Grounded ONLY in the two briefs, answer both decisively, each arguing from the
evidence and naming what would falsify it:
- **"What's the biggest concern?"** The single most dangerous flaw or risk.
  ONE, not a list. The contrarian lens, done once, grounded, ranked by blast
  radius.
- **"What am I missing?"** The blind spot / reframe: the wrong assumption the
  whole thing rests on, the shift in the market, the bigger prize or the
  quieter killer sitting next to it.
-> `03-interrogate.md`.

## Move 4 - CONCLUDE + KILL-CHECK (one subagent = the only independence spend)
- Main loop drafts the **conclusive argument**: verdict + confidence, the 2-3
  load-bearing claims, the single flip-condition, the cheapest test.
- Then ONE independent skeptic gets the argument + the two briefs and tries to
  KILL it (default = refuted): refute the verdict, break a load-bearing claim,
  or show the flip-condition is already true. It never grades its own work; it
  only sees the argument. If budget is tight, a deliberate main-loop steelman
  labeled degraded stands in for the subagent.
- **Survives** -> label the verdict CONFIRMED. **Falls** -> revise ONCE in the
  main loop and state what changed. -> `04-argument.md`.
- **`--full` (high-stakes only):** if you have a separated multi-persona review
  skill (independent critics + a judge that is not one of them), swap the
  single kill-check for it. Everything else is identical.

## Deliver + record
- Present tightly: verdict, the biggest concern, what you're missing, the
  flip-condition, the cheapest test. Point at the run folder for the rest.
- Write the thesis updates through `ledger.py`, never by hand-editing the file.

## Rules (same walls, same standard)
- **Advice-only.** Never posts, charges, deploys, publishes, or edits a live
  surface. Money fails closed: paid research passes run only on explicit
  per-run OK.
- **VERIFIED vs ASSUMED end to end.** A claim with no source is ASSUMED and
  cannot be load-bearing (the tool enforces this). Say what you checked and
  found clean, not only what's broken.
- **A re-run after a reshape is a NEW argument** - the old verdict does not
  carry.
- **State lives in files, and the run is resumable.** `state.py show` first,
  resume from the move it names, never restart an interrupted run.

## Cost discipline (spend on integrity, economize on ceremony)
Integrity comes from four things: verifying the load-bearing claims against
sources, keeping the kill-check independent, honest VERIFIED/ASSUMED and
degradation labels, and grounding in real numbers. None needs maximum spend.
- **Distil, don't dump** - agents get the compact brief + one question, never a
  raw file or the transcript.
- **Call the engine, not its contract** - invoke helper CLIs directly instead
  of loading their full documentation into context.
- **Tier model/effort** - a cheaper tier for the sweep; your strongest only for
  a genuinely load-bearing kill-check or synthesis.
- **Verify only load-bearing findings** - the kill-check hits the verdict and
  its 2-3 claims, not every bullet. Biggest single lever.
- **Cache + reuse** - the landscape is stable for weeks; reuse a recent brief.
- **Budget-aware up front** - pick LEAN / FULL / degraded at the START; if
  forced to degrade, LABEL it. Integrity is preserved by honesty, not by
  pretending the full run happened.
