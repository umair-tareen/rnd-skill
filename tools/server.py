"""server.py -- optional MCP server for the rnd toolkit.

Exposes the deterministic thesis mechanics (ledger / state / squeeze / trim)
as MCP tools, so ANY MCP client (Claude Code, Claude Desktop, Cursor, ...)
can maintain a living thesis without shelling out to the CLIs. The judgment
stays with the model; these tools guarantee the mechanics, exactly like the
CLI path.

The four tool modules stay stdlib-only. This server is the one optional
extra and needs the official SDK:

    pip install mcp

Register with Claude Code:

    claude mcp add rnd -- python /absolute/path/to/tools/server.py

Every path argument must be absolute: MCP servers inherit an arbitrary cwd.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ledger as _ledger
import squeeze as _squeeze
import state as _state
import trim as _trim

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("rnd")


def _abs(path: str, what: str = "path") -> str:
    """Every path an MCP client sends must be absolute. This was previously a
    docstring-advisory rule -- the exact defect shape this repo's own bug log
    records twice (B1, B4: a rule living only in prose). Now it is code."""
    p = Path(path)
    if not p.is_absolute():
        raise ValueError(
            f"{what} must be an ABSOLUTE path (got {path!r}). MCP servers "
            f"inherit an arbitrary working directory, so a relative path "
            f"would resolve somewhere neither of us chose.")
    return str(p)


# --- thesis ledger ----------------------------------------------------------

@mcp.tool()
def thesis_new(slug: str, title: str, path: str) -> str:
    """Create a fresh thesis ledger file at `path` (absolute). Fails if the
    file already exists (a thesis is durable; never silently recreate one)."""
    path = _abs(path, "path")
    p = Path(path)
    if p.exists():
        return f"REFUSED: {path} already exists. A thesis is durable; edit it via the claim/flip/open tools."
    text = _ledger.new(slug, title)
    _ledger._atomic_write(p, text)
    return f"created {path}"


@mcp.tool()
def thesis_show(path: str) -> dict:
    """Parse a thesis file and return its full structure: verdict, claims,
    flips, open questions, diff log, meter, bugs, plus the derived demand
    status (customer claims verified by buyer contact vs assumed)."""
    path = _abs(path, "path")
    doc = _ledger.parse(path)
    doc["demand"] = _ledger.demand_status(doc)
    return doc


@mcp.tool()
def thesis_stale(path: str = "", directory: str = "", days: int = 7) -> str:
    """What has gone unexamined: never-tested flips, aged load-bearing claims,
    high-blast open questions, unvalidated demand. Give `path` for one thesis
    or `directory` to scan a folder of them. A pre-registered flip nobody ever
    checks is the failure a ledger invites: recorded, never read."""
    paths = ([Path(p) for p in sorted(Path(_abs(directory, "directory")).glob("*.md")) if p.name != "_index.md"]
             if directory else [Path(_abs(path, "path"))])
    if not paths:
        return f"no thesis files found ({directory or path})"
    out = []
    for p in paths:
        rep = _ledger.stale_report(_ledger.parse(p), days=days)
        rep["slug"] = rep["slug"] if rep["slug"] != "-" else p.stem
        out.append(_ledger.render_stale(rep))
    return "\n".join(out)


@mcp.tool()
def claim_add(path: str, claim: str, st: str, conf: float | None = None,
              falsifier: str = "-", source: str = "-",
              load_bearing: bool = False, cls: str = "-",
              seen: str = "") -> str:
    """Append a claim. st: V verified / A assumed / R refuted / O open.
    cls: world (a desk settles it) / customer (only buyer contact settles it)
    / internal (our own data settles it). Enforced: a claim with no source is
    forced to ASSUMED and can never be load-bearing; a customer claim should
    only be V on a real buyer interaction. Returns the assigned id."""
    path = _abs(path, "path")
    try:
        cid = _ledger.add_claim(path, claim, st, conf, falsifier=falsifier,
                                source=source, load_bearing=load_bearing,
                                seen=seen or None, cls=cls)
    except ValueError as e:
        return f"REFUSED: {e}"
    return f"added {cid}"


@mcp.tool()
def claim_set(path: str, cid: str, st: str = "", conf: float | None = None,
              falsifier: str = "", source: str = "", claim: str = "",
              cls: str = "", load_bearing: bool | None = None) -> str:
    """Revise an existing claim in place (the recheck/diff move: V->R, conf
    up/down, better source). Only the fields you pass change. The no-source
    guard re-applies. Log the change afterwards via diff_append."""
    path = _abs(path, "path")
    try:
        ok = _ledger.set_claim(path, cid,
                               st=st or None, conf=conf,
                               falsifier=falsifier or None,
                               source=source or None,
                               claim=claim or None, cls=cls or None,
                               load_bearing=load_bearing)
    except ValueError as e:
        return f"REFUSED: {e}"
    return f"revised {cid}" if ok else f"NOT FOUND: {cid}"


@mcp.tool()
def open_set(path: str, qid: str, st: str = "", question: str = "",
             blast: str = "", cites: str = "", closed_by: str = "") -> str:
    """Update an open question (st: '.' todo / '~' researching / 'x'
    answered). When marking 'x', ALWAYS pass closed_by = the claim id that
    answered it; that link is what lets the meter tell a question closed on
    evidence from one closed on a guess."""
    path = _abs(path, "path")
    ok = _ledger.set_open(path, qid, st=st or None, question=question or None,
                          blast=blast or None, cites=cites or None,
                          closed_by=closed_by or None)
    return f"updated {qid}" if ok else f"NOT FOUND: {qid}"


@mcp.tool()
def flip_set(path: str, fid: str, last_checked: str = "", holds: str = "",
             condition: str = "") -> str:
    """Stamp a flip re-check: last_checked (YYYY-MM-DD) + holds (y/n/untested).
    Flips are pre-registered kill conditions; re-check them EVERY run."""
    path = _abs(path, "path")
    ok = _ledger.set_flip(path, fid, last_checked=last_checked or None,
                          holds=holds or None, condition=condition or None)
    return f"stamped {fid}" if ok else f"NOT FOUND: {fid}"


@mcp.tool()
def verdict_set(path: str, verdict: str, conf: float, run: int, date: str,
                one_line: str) -> str:
    """Rewrite the verdict (go / reshape / no-go + confidence). Derive it from
    the claims; this performs the mechanical rewrite only. The demand stamp is
    re-derived automatically on every write and cannot be suppressed."""
    path = _abs(path, "path")
    _ledger.set_verdict(path, verdict, conf, run, date, one_line)
    return "verdict set"


@mcp.tool()
def diff_append(path: str, run: int, date: str, delta: str, verdict: str,
                cost: str) -> str:
    """Append one run row to the append-only diff log (delta + verdict +
    cost). This is the audit trail that proves the cost curve."""
    path = _abs(path, "path")
    _ledger.append_diff(path, run, date, delta, verdict, cost)
    return f"appended run {run}"


@mcp.tool()
def thesis_compact(path: str) -> dict:
    """Enforce the one-file rule: if the thesis exceeds 500 lines, drop the
    OLDEST diff rows first (claims are never touched) and log the compaction.
    No-op when under budget."""
    return _ledger.compact(_abs(path, "path"))


# --- evidence compression ---------------------------------------------------

@mcp.tool()
def squeeze_text(text: str, kind: str = "") -> dict:
    """Compress a verbose blob to load-bearing signal BEFORE it enters context
    or the thesis. Auto-detects kind (research-dump / social-scan /
    kill-transcript / json-blob / generic) or force one. Returns the
    compressed text plus tokens saved."""
    return _squeeze.squeeze(text, kind=kind or None)


# --- cost + yield meter -----------------------------------------------------

@mcp.tool()
def run_measure(run_folder: str, thesis: str = "", model: str = "opus",
                since: str = "", run: int | None = None) -> str:
    """Measure a run: cost (fixed ledger re-read vs marginal new research,
    run1-vs-runN delta) AND yield (claims added, load-bearing count, questions
    closed on evidence vs on an assumption). Pass since=YYYY-MM-DD when a
    recheck shares an earlier run's folder. Never report the cost half without
    the yield half."""
    run_folder = _abs(run_folder, "run_folder")
    if thesis:
        thesis = _abs(thesis, "thesis")
    m = _trim.measure_run(run_folder, thesis or None, model, since=since or None)
    rows = []
    if thesis:
        try:
            rows = _trim.parse_diff_log(Path(thesis).read_text(encoding="utf-8"))
        except OSError:
            rows = []
    out = _trim.render_meter(m, rows)
    if thesis:
        out += "\n\n" + _trim.render_yield(
            _trim.measure_yield(thesis, run=run), total_tokens=m["total"]["tokens"])
    return out


# --- run manifest (checkpoint / resume) -------------------------------------

@mcp.tool()
def run_state(action: str, run_folder: str, move: str = "", target: str = "",
              thesis: str = "", note: str = "", artifact: str = "",
              force: bool = False) -> str:
    """The run manifest. action: 'show' (ALWAYS call first; prints what is
    settled and the move to run next) / 'init' (creates STATE.md; preserves an
    existing run unless force) / 'start' / 'done' / 'fail' / 'skip' (with
    move=...) / 'next'. A move interrupted mid-flight stays WIP and is REDONE
    on resume, never skipped."""
    run_folder = _abs(run_folder, "run_folder")
    a = action.strip().lower()
    if a == "show":
        return _state.resume_brief(run_folder)
    if a == "init":
        _state.init(run_folder, target or "-", thesis=thesis or None, force=force)
        return _state.resume_brief(run_folder)
    if a == "next":
        nxt = _state.next_pending(run_folder)
        return nxt if nxt else "ALL-DONE"
    if not move:
        return f"action {a!r} needs move=..."
    if a == "start":
        _state.start(run_folder, move)
        return f"{move}: WIP"
    if a == "done":
        _state.done(run_folder, move, note=note or "-", artifact=artifact or "-")
        return f"{move}: DONE"
    if a == "fail":
        _state.fail(run_folder, move, why=note or "failed")
        return f"{move}: FAILED (will be retried on resume)"
    if a == "skip":
        _state.skip(run_folder, move, why=note or "skipped")
        return f"{move}: SKIPPED"
    return f"unknown action {action!r} (show/init/start/done/fail/skip/next)"


if __name__ == "__main__":
    mcp.run()
