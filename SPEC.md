# SPEC - the /rnd thesis ledger (a living, falsifiable decision store)

Turns `/rnd` from a stateless one-shot report into a LIVING THESIS: one durable
ledger file per idea/product/platform. Run 1 populates it at full cost; every
run after re-checks only the falsifiers and researches only the open questions,
so run N costs a FRACTION of run 1 - and the meter proves it. Written in the
caveman `§`-format below (it dogfoods ai-codex's FORMAT.md, the format the
ledger itself uses). Symbols: `→` leads to · `∴` therefore · `∀` for all ·
`!` must · `⊥` never · `≤`/`≥` at most/least · `&`/`|` and/or.

Provenance: embeds the workings of three MIT token-economy repos by skibidiskib:
[ai-codex](https://github.com/skibidiskib/Ai-codex) (compact index that replaces
re-derivation + its FORMAT.md), [ai-squeeze](https://github.com/skibidiskib/Ai-squeeze)
(typed lossy compression), [ai-trim](https://github.com/skibidiskib/ai-trim)
(always-loaded token-tax meter). Mapping in §I.3.

All examples below use a fictional target: "Acme", a paid changelog tool for
small dev teams.

## §G GOAL
One line: make the cost of knowing curve DOWN over time. A decision that
accumulates verified evidence, tracks which load-bearing claims still hold, and
only spends on the delta since last run.

## §C CONSTRAINTS
- C1: one file per thesis → `<workspace>/theses/<slug>.md`. ⊥ one-file-per-run
  sprawl (the run folder stays as scratch; the thesis is the durable store).
- C2: re-read EVERY run ∴ ! token-minimal. Caveman-encoded, addressable `§S.n`,
  ≤ 500 lines (compact §D oldest-first before ever splitting - ai-codex
  one-file rule).
- C3: advice-only; money fail-closed; VERIFIED vs ASSUMED preserved end-to-end.
  claim with ⊥ source → ASSUMED & ⊥ load-bearing.
- C4: append-only where audit matters (§D diff-log; refuted claims stay in §C).
- C5: recheck reuses PRE-REGISTERED falsifiers (§F) → ⊥ re-tune after seeing
  results.
- C6: model/tool-agnostic - plain markdown; any research/critique backend
  writes in through `ledger.py`.

## §I INTERFACES

### §I.1 - the thesis file (SCHEMA)
Fixed sections, fixed order. Every `/rnd` run reads it whole, cheap.

`§T THESIS` - the verdict, DERIVED from §C (⊥ hand-set):
```
verdict: reshape (conf 0.7) · as-of run 2 · 2026-07-23 · ⚠ demand-UNVALIDATED: 2 customer claim(s), 0 verified by buyer contact (C3,C5)
one-line: <the conclusive argument in a sentence>
```
The `⚠ demand-*` stamp is DERIVED from §C on every write (V10) - ⊥ stored, ⊥
hand-set, ⊥ deletable: strip it and the next mutation puts it straight back. A
verdict therefore cannot be read without seeing whether its customer basis is
assumed.

`§C CLAIMS` - the ledger heart. pipe table, monotonic ids, `*`=load-bearing:
```
id  | st | cls      | claim                                      | conf | falsifier                            | source          | seen
C1* | V  | world    | rivals bundle changelog generation free    | 0.85 | a paying user cites no free rival    | example.com/faq | 07-21
C2* | V  | world    | platform ToS driver = should, not must-buy | 0.7  | a ToS enforcement hits a small team  | example.org/tos | 07-21
C3  | A  | customer | small dev teams are reachable warm         | 0.3  | 0 warm intros after outreach         | -               | 07-21
C7  | R  | world    | the $500 pilot design is fine as-is        | -    | (refuted: inside procurement review) | example.gov/reg | 07-21
```
st: `V` verified · `A` assumed · `R` refuted (kept, ⊥ deleted) · `O` open.
biggest-concern = highest-blast unrefuted risk claim (tag risk in the claim text).

**cls (V10) = what kind of evidence could ever SETTLE the claim**, ⊥ what it is
about. `world` a desk settles it (competitors, regulation, pricing bands, tech) ·
`customer` ONLY buyer contact settles it (reachable? will they pay?) ·
`internal` our own data settles it (our hours, our capacity). WHY: a research
engine verifies what a desk can reach, ∴ a thesis drifts to confident `world` +
assumed `customer` and READS as validated while demand is untested. A
`customer` claim → `V` only on a BUYER INTERACTION (reply / booked call /
signature / payment); a pricing comparable or analyst report is `world`
evidence and ⊥ verifies willingness to pay. Keep the two separate as separate
claims: "the price sits in the market band" (world, verifiable) ≠ "these teams
will pay US it" (customer, only contact settles).

`§F FLIPS` - pre-registered kill conditions (the subset of load-bearing
falsifiers that flip the VERDICT). Re-checked EVERY run:
```
id | if this becomes true -> verdict flips to | last-checked | holds?
F1 | a rival ships the same artifact -> no-moat | 07-22 | y
F2 | 8+ warm intros book a demo -> go           | 07-22 | untested
```

`§Q OPEN` - what's NOT yet investigated ("what am I missing", durable). Drives
the NEXT run's research; nothing else gets fresh spend:
```
id | st | question                             | blast | cites | closed_by
Q1 | x  | is the rival's 'AI release-notes' real?| high  | C1    | C9
Q2 | ~  | do platform marketplaces channel tools?| high  | C2    | -
```
st: `.` todo · `~` researching · `x` answered (→ promoted to a §C claim).
`closed_by` = the §C claim that actually answered it. ! set it when flipping to
`x`: once st reads `x`, a question closed on hard evidence and one closed on a
guess look identical, and only this link tells them apart (feeds §Y).

`§D DIFF` - append-only backprop log (proves the cost curve + audit trail):
```
run | date  | delta                          | verdict | cost
1   | 07-21 | +10 claims, full sweep         | reshape | 25k tok / $0.38
2   | 07-23 | F1 re-held, 3 of 4 Qs answered | reshape | 1.3k tok re-read + 4 free searches
```

`§M METER` - cost accounting (ai-trim): fixed (ledger re-read = "always-loaded")
+ marginal (new research = "on-demand") = total tok/$; run1 vs runN delta + a
trim recommendation.

`§Y YIELD` - what the run BOUGHT. ! reported beside §M, ⊥ alone:
```
claims added: 3 (V=2 A=1 R=0), 0 load-bearing
mean confidence of what it added: 0.52
questions closed: 2 on EVIDENCE [Q1<-C9, Q2<-C10], 1 on an ASSUMPTION [Q4<-C11]
  !! 0 load-bearing claims added: cheap, but it moved nothing the verdict rests on
```
WHY: a cost meter alone rewards spending less, and the cheapest possible run
answers nothing ∴ "run 2 = 5% of run 1" is meaningless until you can see 5% of
the cost bought WHAT. Yield is what separates an efficient run from a shallow
one, and nothing else in the ledger can tell them apart. Claims are attributed
to a run by `seen` ∈ [runN.date, runN+1.date).

### §I.2 - the RECHECK/DIFF loop (why run N ≪ run 1)
Run N on an existing thesis:
1. **LOAD** the ledger (compact caveman file) → cheap. This REPLACES
   re-research (ai-codex principle): you read the index, not the world.
2. **RECHECK** - ∀ §F flip + load-bearing §C claim → re-verify ONLY its
   falsifier against current reality (targeted search, ⊥ full deep-research).
   Squeeze each result (§I.3). Stamp via `set_flip`.
3. **DIFF** - new evidence vs stored claims → `set_claim` the changed ones
   (V→R, conf ±), `add_claim` the new.
4. **RESEARCH-NEW** - only the top-blast `§Q` open questions get fresh research
   (budget-gated). Squeeze in → new §C rows; answered §Q flip `. → x` with
   `closed_by` set.
5. **RE-DERIVE** - recompute §T from updated §C (`set_verdict`); ONE
   independent kill-check on the NEW verdict.
6. **METER + APPEND** - `append_diff` the §D row; `trim.py` prints §M + §Y;
   report run1 vs runN WITH the yield.

Cost(N) ≈ read(small file) + recheck(few targeted queries) + research(only new
Q) ≪ Cost(1) = full sweep. The stable majority of the landscape (regulatory
map, competitive set, pricing band) is ⊥ re-researched. `--fresh` forces a full
re-sweep when you distrust the ledger.

### §I.2b - the RUN MANIFEST (`state.py`; why an interruption is free)
Usage limits WILL kill long runs ∴ the manifest is MECHANICAL, ⊥ prose. One
`STATE.md` per run folder, owned by `tools/state.py`
(`init`/`start`/`done`/`fail`/`skip`/`next`/`show`).
```
| # | move             | st      | artifact       | note                |
| 1 | FRAME            | DONE    | 00-frame.md    | ground truth set    |
| 2 | EVIDENCE-research| DONE    | 01-research.md | 8 cited claims      |
| 3 | EVIDENCE-voice   | WIP     | -              | started 2026-07-24  |  <- died here
```
`state.py show` is the FIRST call of every invoke, before any spend. Settled =
`DONE`|`SKIPPED` only. **`WIP` and `FAILED` are ⊥ settled: the interrupted move
is REDONE.** Skipping it instead would silently drop the work the crash
interrupted while still looking like a clean resume - the worst available
failure, because it is invisible. `init` on an existing run PRESERVES it
(`--force` alone starts over) ∴ re-invoking `/rnd <same target>` resumes.

### §I.3 - EMBEDDED WORKINGS (the three repos)
| repo | its working | where it lives in the ledger |
|---|---|---|
| **ai-codex** | compact pre-built index that replaces re-derivation; FORMAT.md caveman spec (§-sections, symbols, pipe tables, monotonic ids, status cells, one-file ≤500ln) | the thesis file IS a codex-for-a-decision. Adopt FORMAT.md verbatim. Re-read every run instead of re-researching (§I.2 step 1). |
| **ai-squeeze** | `detectType(blob)` → typed lossy compression: count + top-N + head/tail + dedup; report tokens saved (defaults THRESH 20 / HEAD 10 / TAIL 10) | INTAKE filter: `squeeze(blob, kind)` before ANY evidence enters the ledger or passes between moves. kinds: `research-dump` → claims+sources+risks · `social-scan` → top-signals+counts+quote+URL · `kill-transcript` → verdict+LB-claims+falsifiers · `json-blob` · `generic`. (The source repo's five coding-agent kinds were cut by a ponytail review - no /rnd move produces them; git history keeps them.) |
| **ai-trim** | 4 chars/token est; per-model $/token; always-loaded vs on-demand split; recommend cuts | the §M METER. fixed = ledger re-read ("always-loaded"); marginal = new research ("on-demand"). Emit tok + $ + run1-vs-runN + trim rec. |

## §V INVARIANTS
- V1: §T verdict ! DERIVED from §C claims, ⊥ hand-set.
- V2: claim with ⊥ source → st=A, ⊥ load-bearing (⊥ `*`). Tool-enforced.
- V3: §F falsifiers pre-registered BEFORE recheck; ⊥ re-tune post-hoc.
- V4: refuted claims stay in §C (st=R) + logged in §D; ⊥ silent delete.
- V5: the kill-check ⊥ grades its own verdict; independent.
- V6: recheck touches only §F + load-bearing §C + §Q; full re-sweep only on
  `--fresh`.
- V7: money fail-closed (paid pass = explicit OK); advice-only (⊥ live surface).
- V8: every run appends §D (delta + cost) + updates §M. audit survives a crash
  (atomic writes).
- V9: file > 500 ln → compact §D oldest-first (ai-codex one-file rule), ⊥ split.
- V10: ∀ claim ! carries a `cls` (world/customer/internal). A `customer` claim
  → `V` ONLY with TYPED buyer evidence: source prefixed
  `buyer:reply|call|signature|payment` - the tool REFUSES free text (a
  comparable or analyst note is `world` evidence). While ⊥ customer claim
  carries such evidence, §T ! carry the derived `⚠ demand-UNVALIDATED` stamp
  (recomputed each write, ⊥ stored, ⊥ deletable). Semantics, stated honestly:
  tamper-EVIDENT, ⊥ a lie detector - it enforces that the buyer-contact
  question is ASKED in a checkable form; the truth of the evidence is the
  operator's.
- V11: ⊥ report a cost saving without §Y YIELD beside it. A run that answers
  nothing is the cheapest run there is.
- V12: a move interrupted mid-flight (`WIP`/`FAILED`) is REDONE on resume, ⊥
  skipped. Only `DONE`/`SKIPPED` settle. `state.py show` runs before any spend.
- V13: an untested §F flip ! SURFACE (`ledger.py stale`, wired into a daily
  brief if you have one). Recording ≠ surfacing; a ledger nobody reads is a
  ledger that changes nothing.

## §B BUGS (backprop log from the first live deployment; append a row when a
run breaks an invariant. Kept because every invariant above was EARNED.)
```
id | date | cause | fix->invariant
B1 | 2026-07-24 | the recheck/diff loop (I.2) specified claim revision but ledger.py had no mutation API -> run 2 hand-edited the parsed doc | added set_claim/set_open/set_flip; the Run-N loop now calls them by name. Found by an adversarial self-review of the skill.
B6 | 2026-07-25 | a maintainer edit round-tripped ledger.py through a cp1252 read / utf-8 write, double-encoding every section-sign in the parser's regexes. THE SELFTEST STAYED GREEN - it writes and parses with the same corrupted symbols, so it was self-consistently blind - while every REAL thesis parsed as empty (0 claims, "NOT FOUND"). No data was touched; only the parser's eyes broke. Caught within minutes because a real file was checked right after the selftest. | reverted from git; patch reapplied by an encoding-declaring tool; selftest now carries an encoding CANARY (section-sign pinned to U+00A7) so source corruption fails loudly instead of passing green. Lesson: a selftest that round-trips through its own writer cannot see writer+reader corruption - always verify against one artifact the current process did not create.
B2 | 2026-07-24 | trim.py charged EVERY .md in the run folder to the current run. Run 2 shared run 1's folder, so the meter that exists to prove the cost curve reported 105% of run 1 when the truth was ~5% | --since mtime filter (excluded files REPORTED, not dropped) + stale_folder_warning(); run N ! gets its own folder -> V8
B3 | 2026-07-24 | the ledger measured COST and nothing else, so a run that got cheaper by getting shallower scored as a win; separately, every VERIFIED claim was desk-reachable and both customer-facing claims were assumed - the thesis read validated with demand untested | §Y YIELD beside §M (V11) + §Q closed_by; claim cls + the derived demand stamp (V10). Found by running /rnd's own two questions on /rnd.
B4 | 2026-07-24 | SAME SHAPE AS B1: the resilience section told the model to checkpoint to STATE.md and resume, but nothing owned that file - a promise, never exercised by a real kill | built state.py + wired the skill to call it; rehearsed a mid-move kill resumed by a COLD process, redoing only the interrupted move -> V12
B5 | 2026-07-25 | FOUND BY A 5-PERSONA ADVERSARIAL REVIEW + INDEPENDENT JUDGE (verdict: reshape 0.85, as-is 3/10). (a) install doc copied SKILL.md alone while every command was cwd-relative -> first call crashed for any adopter; (b) free text cleared the demand stamp -> "tool-enforced" was overclaimed; (c) the cost meter measured markdown written not spend, rendered in 4-decimal dollars, and failed OPEN on a missing run folder; (d) every piece of evidence was gitignored (a repo configured to never contain its own demo); (e) server.py had no CI and its absolute-path rule lived in prose (B1's shape, third occurrence); (f) LICENSE described upstream provenance without reproducing the notice | (a) skill installs WITH tools/, ∀ command <skill-dir>-absolute; (b) typed buyer evidence buyer:reply\|call\|signature\|payment REFUSED otherwise + stamp reframed tamper-EVIDENT -> V10; (c) unit line in §M, "~$ est." only, exit 2 on missing folder; (d) examples/acme committed, generated by the tools; (e) test_server.py in CI + _abs() enforcement; (f) upstream MIT notice reproduced in LICENSE. Independent scores: concept 8/10, reshaped direction 8/10 - the artifact was never the problem; the claims about it were.
```
