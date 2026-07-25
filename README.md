# rnd-skill

![rnd-skill: a living thesis ledger for AI research](.github/banner.svg)

A Claude Code skill + toolkit that turns one-shot AI research into a **living,
falsifiable thesis** whose cost curves DOWN over time, and that is built to be
honest about the three ways AI research quietly lies to you.

You point it at an idea ("run R&D on X"), and it ends on one defensible
verdict: **go / reshape / no-go**, the 2-3 load-bearing claims it rests on, the
single condition that would flip it, and the cheapest test. Then it writes all
of that into a compact ledger, so the next run re-checks the falsifiers instead
of re-researching the world.

## The three lies this is built against

**1. Re-derivation.** Most AI research is a one-shot report: expensive, then
thrown away. Ask again next month and you pay full price to rediscover a mostly
unchanged landscape. Here, run 1 populates a per-target thesis ledger; run N
loads it (~1k tokens), re-checks only the pre-registered kill conditions, and
researches only the open questions. On the first live thesis, run 2 cost
**5.3% of run 1** (measured by the included meter, from the files, not
self-reported).

**2. Cheapness masquerading as efficiency.** A cost meter alone rewards
spending less, and the cheapest possible run answers nothing. So the meter
prints **yield beside cost**: claims added, how many are load-bearing, mean
confidence, and questions closed on EVIDENCE versus closed on an ASSUMPTION.
That same 5.3% run 2 also printed: `0 load-bearing claims added`, `1 question
closed on an assumption`. Both numbers, always.

**3. Desk research masquerading as validation.** A research engine verifies
what a desk can reach, so a thesis drifts toward confident world-claims and
assumed customer-claims and reads as validated while nobody has tested demand.
Every claim is classed `world` / `customer` / `internal` by what kind of
evidence could ever settle it. A customer claim reaches VERIFIED only on a
buyer interaction (a reply, a booked call, a payment). While none is, the tool
derives a `demand-UNVALIDATED` stamp onto the verdict line on every write. It
cannot be hand-set, go stale, or be deleted.

## What's in the box

| file | what it is |
|---|---|
| `SKILL.md` | the Claude Code skill: 4 moves (FRAME, EVIDENCE, INTERROGATE, CONCLUDE + independent kill-check), lean by default |
| `SPEC.md` | the design doc: schema, recheck/diff loop, invariants V1-V13, and the bug log that earned them |
| `tools/ledger.py` | deterministic thesis bookkeeping: ids, append-only diff log, the no-source guard, the demand stamp, staleness reporting, one-file compaction |
| `tools/squeeze.py` | typed lossy compression for evidence blobs before they enter context or the ledger |
| `tools/trim.py` | the cost + yield meter: fixed vs marginal tokens, run1-vs-runN delta, evidence-vs-assumption accounting |
| `tools/state.py` | the run manifest: checkpoint every move, resume after a crash, redo (never skip) the interrupted move |
| `tools/server.py` | optional MCP server exposing all of the above as 13 tools to any MCP client |

All four tool modules are stdlib-only Python 3.10+, each with a built-in
self-test. The model supplies judgment; the tools guarantee the mechanics.

## Quickstart

```bash
# install the skill (Claude Code)
mkdir -p ~/.claude/skills/rnd && cp SKILL.md ~/.claude/skills/rnd/

# scaffold a thesis
python tools/ledger.py new acme "Acme changelog tool" --out theses/acme.md

# after a run: what did it cost, and what did it buy?
python tools/trim.py runs/acme-2026-07-21 --thesis theses/acme.md

# what has gone unexamined? (exit 1 if anything needs attention)
python tools/ledger.py stale --dir theses

# self-tests
python tools/ledger.py selftest
python tools/squeeze.py --selftest
python tools/trim.py --self-test
python tools/state.py --self-test
```

Then, in Claude Code: `run R&D on <your idea>`.

## MCP server (optional)

The same mechanics as MCP tools, for Claude Code, Claude Desktop, Cursor, or
any MCP client. The tool modules stay stdlib-only; the server is the one
optional dependency:

```bash
pip install mcp
claude mcp add rnd -- python /absolute/path/to/tools/server.py
```

13 tools: `thesis_new` / `thesis_show` / `thesis_stale`, `claim_add` /
`claim_set`, `open_set`, `flip_set`, `verdict_set`, `diff_append`,
`thesis_compact`, `squeeze_text`, `run_measure` (cost AND yield, always
together), and `run_state` (the crash-safe run manifest). The invariants ride
along: the no-source guard, the derived demand stamp, and the
redo-never-skip resume rule are enforced server-side, not requested politely
in a prompt. Use absolute paths in every call; MCP servers inherit an
arbitrary working directory.

## Why the resume path is mechanical

Usage limits kill long agent runs; that is the environment, not a failure.
Most "resumable" agent designs are prose: the model is told to checkpoint and
resume, and nothing owns the file. `state.py` owns it. The property that
matters, and the one the self-test attacks: **a move interrupted mid-flight is
left WIP and gets REDONE on resume, never skipped.** Skipping it would silently
drop exactly the work the crash interrupted while still looking like a clean
resume, which is the worst available failure because it is invisible.

## The bug log is the point

`SPEC.md` §B records four real defects, all found by turning the skill's own
interrogation ("what's the biggest concern? what am I missing?") on itself:
a mutation API that existed only in prose, a cost meter that reported 105%
when the truth was 5%, a cost meter with no yield counterweight, and a resume
path that had never survived a kill. Every invariant in the spec was earned by
one of them. That is the standard the skill holds its research targets to, so
it is the standard it gets held to.

## Credits

Embeds the workings of three MIT repos by [skibidiskib](https://github.com/skibidiskib):
[ai-codex](https://github.com/skibidiskib/Ai-codex) (the compact re-read index
and its caveman FORMAT.md), [ai-squeeze](https://github.com/skibidiskib/Ai-squeeze)
(typed lossy compression), [ai-trim](https://github.com/skibidiskib/ai-trim)
(the always-loaded token-tax meter). The voice lane pairs well with
[last30days-skill](https://github.com/mvanhorn/last30days-skill) (MIT) if you
have it; it is optional.

## Honest status

- Proven live: the recheck/diff loop end to end (run 1 full sweep, run 2 at
  5.3% with the yield warnings above), the demand stamp, the staleness report,
  and a mid-move kill resumed by a cold process in rehearsal.
- Not yet proven: more than one live thesis, and a resume through a real
  mid-run usage-limit kill (rehearsed mechanically, not yet observed live).

MIT License.
