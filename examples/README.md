# examples/acme - a complete worked example

A SYNTHETIC two-run thesis on a fictional target (Acme, a paid changelog tool
for small dev teams), generated end-to-end by the repo's own tools. Every
number in it is real tool output over these files; none of it is a claim
about a real market.

What to look at:
- `acme.md` - the living thesis after two runs. Note the verdict line: it
  carries the derived `demand-UNVALIDATED` stamp because both customer-class
  claims (C4, C5) are still ASSUMED - by design, no web search can clear
  them; only `buyer:` typed evidence can.
- `run-1-full-sweep/` - the four briefs a full first run writes, plus its
  crash-safe `STATE.md` manifest.
- `run-2-recheck/` - what run N actually is: one small brief. The thesis was
  re-read; the world was not re-researched. Q1 was closed ON EVIDENCE
  (`closed_by C8`); Q2 stayed open because it needs a buyer, not a search.
- `METER.txt` - the real cost + yield output for run 2. The unit line and
  the yield block are the honest part: cheap is only good if it bought
  something, and the meter says so itself.

Reproduce any of it:

```bash
python tools/trim.py examples/acme/run-2-recheck --thesis examples/acme/acme.md
python tools/ledger.py show examples/acme/acme.md
python tools/ledger.py stale --dir examples/acme --days 0
python tools/ledger.py demo          # the stamp, live, in 30 seconds
```
