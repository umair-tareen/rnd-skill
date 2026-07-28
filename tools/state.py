"""state.py -- the /rnd run manifest: checkpoint, crash, resume.

Spec: SPEC.md at the repo root.

WHY THIS EXISTS. Usage limits kill long runs; that is the environment, not a
failure. The skill has always SAID "checkpoint every move, resume from the
first PENDING" -- but saying it made it a promise the model had to remember to
keep, and the identical shape of bug is already in the log as B1 (the
recheck/diff loop specified claim revision while ledger.py had no mutation
API, so run 2 hand-edited the file). A resume path that exists only in prose
is a resume path that has never been tested. This module makes it mechanical.

THE CORRECTNESS PROPERTY THAT MATTERS: a move interrupted mid-flight is left
marked WIP. On resume, WIP resolves to PENDING and is REDONE, never skipped.
Only DONE is skipped. Getting this backwards silently drops the exact work the
crash interrupted -- the failure would look like a clean resume and produce a
run missing a move, which is far worse than redoing one step.

Manifest lives at <run-folder>/STATE.md, is markdown (a human and a model both
read it for ~100 tokens), and is written atomically so a kill mid-write cannot
corrupt it.

Public API = the module's function signatures; CLI = `state.py --help`.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
from datetime import date as _date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ledger import _atomic_write, _today, _split_row as _base_split_row, \
    fix_console_encoding as _fix_console_encoding  # ponytail: shared, not re-rolled

STATE_FILE = "STATE.md"

# the lean 4-move run; EVIDENCE splits into its two lanes so a limit-kill
# between them keeps the lane that already landed.
DEFAULT_MOVES = [
    "FRAME",
    "EVIDENCE-research",
    "EVIDENCE-voice",
    "INTERROGATE",
    "CONCLUDE",
]

PENDING, WIP, DONE, FAILED, SKIPPED = "PENDING", "WIP", "DONE", "FAILED", "SKIPPED"
VALID_ST = {PENDING, WIP, DONE, FAILED, SKIPPED}
# DONE and SKIPPED are settled. WIP is NOT: it means "a run died here".
SETTLED = {DONE, SKIPPED}

def _split_row(line: str):
    """ledger's unescaped-pipe split, plus stripping the empty edge cells the
    leading/trailing table pipes produce."""
    cells = _base_split_row(line)
    while cells and cells[0] == "":
        cells.pop(0)
    while cells and cells[-1] == "":
        cells.pop()
    return cells


def _cell(v) -> str:
    s = "" if v is None else str(v)
    s = s.replace("|", "\\|").replace("\n", " ").strip()
    return s if s else "-"


def _state_path(run_folder) -> Path:
    return Path(run_folder) / STATE_FILE


def render(doc: dict) -> str:
    lines = [
        f"# RUN STATE: {doc.get('slug', '-')}",
        f"target: {doc.get('target', '-')}",
        f"started: {doc.get('started') or _today()}",
        f"thesis: {doc.get('thesis') or '-'}",
        "",
        "Resume rule: redo the first move that is not DONE/SKIPPED. A move left",
        "WIP means a run died inside it -- redo it, never skip it.",
        "",
        "| # | move | st | artifact | note |",
        "|---|---|---|---|---|",
    ]
    for i, m in enumerate(doc.get("moves", []), start=1):
        lines.append(
            f"| {i} | {_cell(m['move'])} | {_cell(m['st'])} | "
            f"{_cell(m.get('artifact', '-'))} | {_cell(m.get('note', '-'))} |"
        )
    return "\n".join(lines) + "\n"


def read(run_folder) -> dict:
    """Parse STATE.md. Missing file -> a doc with no moves (a fresh run)."""
    path = _state_path(run_folder)
    doc = {"slug": Path(run_folder).name, "target": "-", "started": "",
           "thesis": "", "moves": [], "exists": path.exists()}
    if not path.exists():
        return doc
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# RUN STATE:"):
            doc["slug"] = s.split(":", 1)[1].strip()
        elif s.startswith("target:"):
            doc["target"] = s.split(":", 1)[1].strip()
        elif s.startswith("started:"):
            doc["started"] = s.split(":", 1)[1].strip()
        elif s.startswith("thesis:"):
            doc["thesis"] = s.split(":", 1)[1].strip()
        if "|" not in line:
            continue
        cells = _split_row(line)
        if len(cells) != 5 or not cells[0].isdigit():
            continue  # header row, the |---| rule, or prose containing a pipe
        st = cells[2].strip().upper()
        if st not in VALID_ST:
            continue
        doc["moves"].append({
            "move": cells[1], "st": st, "artifact": cells[3], "note": cells[4],
        })
    return doc


def _write(run_folder, doc) -> dict:
    _atomic_write(_state_path(run_folder), render(doc))
    return doc


def init(run_folder, target: str, moves=None, thesis=None, force=False) -> dict:
    """Create STATE.md for a run. Existing manifest is PRESERVED unless
    force=True -- re-invoking /rnd on an interrupted run must resume it, not
    silently wipe the record of what already completed."""
    existing = read(run_folder)
    if existing["exists"] and not force:
        return existing
    doc = {
        "slug": Path(run_folder).name,
        "target": target,
        "started": _today(),
        "thesis": thesis or "-",
        "moves": [{"move": m, "st": PENDING, "artifact": "-", "note": "-"}
                  for m in (moves or DEFAULT_MOVES)],
    }
    return _write(run_folder, doc)


def _set(run_folder, move: str, st: str, note=None, artifact=None) -> dict:
    doc = read(run_folder)
    hit = next((m for m in doc["moves"] if m["move"].lower() == move.lower()), None)
    if hit is None:
        raise KeyError(f"move {move!r} not in manifest "
                       f"({[m['move'] for m in doc['moves']]})")
    hit["st"] = st
    if note is not None:
        hit["note"] = note
    if artifact is not None:
        hit["artifact"] = artifact
    return _write(run_folder, doc)


def start(run_folder, move: str) -> dict:
    return _set(run_folder, move, WIP, note=f"started {_today()}")


def done(run_folder, move: str, note: str = "-", artifact: str = "-") -> dict:
    return _set(run_folder, move, DONE, note=note, artifact=artifact)


def fail(run_folder, move: str, why: str) -> dict:
    """A move that errored. FAILED is NOT settled: resume retries it."""
    return _set(run_folder, move, FAILED, note=why)


def skip(run_folder, move: str, why: str) -> dict:
    """Deliberately not doing this move (e.g. a lane degraded away). Settled,
    so resume moves past it -- but the reason is on the record."""
    return _set(run_folder, move, SKIPPED, note=why)


def next_pending(run_folder):
    """The move to run now: the first that is not DONE/SKIPPED. None = finished.
    A WIP move (a run died inside it) comes back as the next move to run."""
    for m in read(run_folder)["moves"]:
        if m["st"] not in SETTLED:
            return m["move"]
    return None


def resume_brief(run_folder) -> str:
    """The line to print on invoke, before spending anything."""
    doc = read(run_folder)
    if not doc["exists"]:
        return f"no {STATE_FILE} in {run_folder} -- this is a fresh run"
    settled = [m for m in doc["moves"] if m["st"] in SETTLED]
    nxt = next_pending(run_folder)
    interrupted = [m["move"] for m in doc["moves"] if m["st"] in (WIP, FAILED)]
    out = [f"RESUME {doc['slug']} (target: {doc['target']}, started {doc['started']})",
           f"  settled: {len(settled)}/{len(doc['moves'])} "
           f"[{', '.join(m['move'] for m in settled) or 'none'}]"]
    if interrupted:
        out.append(f"  interrupted mid-flight (will REDO): {', '.join(interrupted)}")
    out.append(f"  next: {nxt}" if nxt else "  next: ALL-DONE (nothing to resume)")
    if settled:
        out.append("  reuse the settled moves' artifacts; do NOT re-run them.")
    return "\n".join(out)


# --- CLI ---------------------------------------------------------------------

def main() -> int:
    _fix_console_encoding()
    ap = argparse.ArgumentParser(prog="state.py",
                                 description="/rnd run manifest: checkpoint + resume")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="create STATE.md (preserves an existing one)")
    p.add_argument("run_folder")
    p.add_argument("--target", required=True)
    p.add_argument("--moves", default=None, help="comma-separated (default: the 5 lean moves)")
    p.add_argument("--thesis", default=None)
    p.add_argument("--force", action="store_true", help="overwrite an existing manifest")

    for name, helptext in (("start", "mark a move WIP"), ("done", "mark a move DONE"),
                            ("fail", "mark a move FAILED"), ("skip", "mark a move SKIPPED")):
        q = sub.add_parser(name, help=helptext)
        q.add_argument("run_folder")
        q.add_argument("move")
        q.add_argument("--note", default=None)
        q.add_argument("--artifact", default=None)

    for name, helptext in (("next", "print the move to run now"),
                            ("show", "print the resume brief")):
        q = sub.add_parser(name, help=helptext)
        q.add_argument("run_folder")

    args = ap.parse_args()

    if args.cmd == "init":
        moves = [m.strip() for m in args.moves.split(",")] if args.moves else None
        init(args.run_folder, args.target, moves, args.thesis, force=args.force)
        print(resume_brief(args.run_folder))
    elif args.cmd == "start":
        start(args.run_folder, args.move)
        print(f"{args.move}: WIP")
    elif args.cmd == "done":
        done(args.run_folder, args.move, args.note or "-", args.artifact or "-")
        print(f"{args.move}: DONE")
    elif args.cmd == "fail":
        fail(args.run_folder, args.move, args.note or "failed")
        print(f"{args.move}: FAILED")
    elif args.cmd == "skip":
        skip(args.run_folder, args.move, args.note or "skipped")
        print(f"{args.move}: SKIPPED")
    elif args.cmd == "next":
        nxt = next_pending(args.run_folder)
        print(nxt if nxt else "ALL-DONE")
    elif args.cmd == "show":
        print(resume_brief(args.run_folder))
    return 0


def _self_test() -> int:
    """Simulates the thing that actually happens: a run dies mid-move. Asserts
    the interrupted move is REDONE and the completed ones are skipped."""
    tmp = Path(tempfile.mkdtemp(prefix="rnd_state_"))
    try:
        rf = tmp / "acme-2026-07-24"

        assert next_pending(rf) is None, "no manifest -> nothing to resume"
        assert "fresh run" in resume_brief(rf)

        init(rf, target="Acme launch", thesis="theses/acme.md")
        assert _state_path(rf).exists()
        assert next_pending(rf) == "FRAME", next_pending(rf)

        start(rf, "FRAME")
        done(rf, "FRAME", note="verified vs assumed split", artifact="00-frame.md")
        assert next_pending(rf) == "EVIDENCE-research"

        start(rf, "EVIDENCE-research")
        done(rf, "EVIDENCE-research", note="8 cited claims", artifact="01-research.md")

        # ---- the kill: a run dies INSIDE the voice lane -------------------
        start(rf, "EVIDENCE-voice")
        del_doc = read(rf)                       # everything below reads from disk only
        assert [m["st"] for m in del_doc["moves"]] == [DONE, DONE, WIP, PENDING, PENDING]

        # ---- resume, in a fresh process's shoes ---------------------------
        assert next_pending(rf) == "EVIDENCE-voice", \
            "a move interrupted mid-flight MUST be redone, never skipped"
        brief = resume_brief(rf)
        assert "settled: 2/5" in brief, brief
        assert "will REDO): EVIDENCE-voice" in brief, brief
        assert "next: EVIDENCE-voice" in brief, brief

        # re-invoking init must NOT wipe the record of completed work
        init(rf, target="Acme launch")
        after = read(rf)
        assert [m["st"] for m in after["moves"]] == [DONE, DONE, WIP, PENDING, PENDING], \
            "re-init must preserve an interrupted run's progress"
        assert after["moves"][0]["artifact"] == "00-frame.md"
        assert after["moves"][1]["note"] == "8 cited claims"

        # a failed lane is also not settled; a deliberately skipped one is
        fail(rf, "EVIDENCE-voice", why="Reddit 403; degraded to WebSearch")
        assert next_pending(rf) == "EVIDENCE-voice"
        skip(rf, "EVIDENCE-voice", why="voice lane dropped, budget")
        assert next_pending(rf) == "INTERROGATE", "SKIPPED is settled; move past it"

        done(rf, "INTERROGATE", artifact="03-interrogate.md")
        done(rf, "CONCLUDE", artifact="04-argument.md")
        assert next_pending(rf) is None
        assert "ALL-DONE" in resume_brief(rf)

        # notes with a pipe must not break the table on the round trip
        done(rf, "CONCLUDE", note="verdict: reshape | conf 0.7", artifact="04-argument.md")
        assert read(rf)["moves"][4]["note"] == "verdict: reshape | conf 0.7"

        # force=True is the only way to start over
        init(rf, target="Acme launch", force=True)
        assert next_pending(rf) == "FRAME"

        try:
            done(rf, "NOT-A-MOVE")
            raise AssertionError("an unknown move must raise, not silently no-op")
        except KeyError:
            pass

        print("PASS: state.py self-test (checkpoint, mid-move kill, resume, "
              "re-init safety) OK")
        print()
        print(_state_path(rf).read_text(encoding="utf-8"), end="")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv or "--selftest" in sys.argv:
        _fix_console_encoding()
        sys.exit(_self_test())
    sys.exit(main())
