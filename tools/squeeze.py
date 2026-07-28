"""squeeze.py -- typed lossy compression: verbose blob -> load-bearing signal.

Why: /rnd's thesis ledger (see SPEC.md, S:I.3)
must stay token-minimal even though evidence keeps arriving as noisy tool
output, research dumps, social scans, and kill-check transcripts. This is the
INTAKE FILTER: run any blob through squeeze() BEFORE it enters context or gets
written into a thesis file's SC/SQ sections.

Provenance: ports skibidiskib/Ai-squeeze (github.com/skibidiskib/Ai-squeeze,
src/squeeze.ts + src/index.ts) - the MECHANISM (detect -> typed compressor,
THRESHOLD=20 lines, HEAD=10, TAIL=10, 4 chars/token, the exact CLI footer)
plus its json/generic compressors. The source repo's five coding-agent kinds
(typescript-errors, test-results, npm-install, stack-trace, git-log) were
deliberately dropped: no /rnd move ever produces them (a ponytail-review cut,
~240 lines; git history has them if a fork wants them back). Adds three
ledger-domain kinds the source repo has no notion of:
  - research-dump   deep-research prose with VERIFIED/SUSPECTED lines, claim
                     lines, and cited URLs buried in it -> keep signal, drop prose.
  - social-scan     subreddit/score/upvote scan rows -> keep top-scored rows
                     (with their URLs), dedup near-identical ones.
  - kill-transcript  a Move-4 skeptic kill-check transcript -> keep the verdict
                     line plus any load-bearing / falsifier lines, drop the rest.

Public API:
    squeeze(text, kind=None) -> dict with keys:
        compressed, kind, orig_lines, comp_lines, orig_chars, comp_chars,
        tokens_saved (estimated at 4 chars/token)
    detect_type(text) -> one of the KINDS below.

CLI:
    python squeeze.py [--kind KIND] <file>      # compress a file
    <command> | python squeeze.py               # or read stdin
    python squeeze.py --selftest                # run the built-in self-test

STDLIB ONLY. No pip installs (matches the source repos: zero runtime deps).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Defaults (ported verbatim from ai-squeeze src/squeeze.ts)
# ---------------------------------------------------------------------------

THRESHOLD = 20      # lines; at or under this, output passes through untouched
HEAD_LINES = 10
TAIL_LINES = 10
CHARS_PER_TOKEN = 4  # ai-trim's estimate, reused here for the footer stat

# KINDS is derived from _COMPRESSORS at the bottom of this module - a
# hand-kept second copy is one edit away from drifting.


# ---------------------------------------------------------------------------
# ANSI stripping (ported: stripAnsi() in squeeze.ts)
# ---------------------------------------------------------------------------

_ANSI_CSI_RE = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")
_ANSI_OSC_RE = re.compile(r"\x1b\].*?\x07")
_ANSI_CHARSET_RE = re.compile(r"\x1b[()][AB012]")


def strip_ansi(text: str) -> str:
    """Strip ANSI escape codes (CSI/OSC/charset-select) and lone CRs."""
    text = _ANSI_CSI_RE.sub("", text)
    text = _ANSI_OSC_RE.sub("", text)
    text = _ANSI_CHARSET_RE.sub("", text)
    return text.replace("\r", "")


# ---------------------------------------------------------------------------
# Detection (structure ported from detectType(); coding-agent kinds cut)
# ---------------------------------------------------------------------------

_URL_RE = re.compile(r"https?://\S+")
_VERIFIED_SUSPECTED_RE = re.compile(r"\b(VERIFIED|SUSPECTED)\b")
_CLAIM_LINE_RE = re.compile(r"(?i)^\s*[-*\d.]*\s*claim\s*:")
_SOCIAL_SIGNAL_RE = re.compile(r"(?i)\b(subreddit|upvotes?|r/\w+)\b")
_SCORE_KW_RE = re.compile(r"score[:\s]+(\d+)", re.I)
_SCORE_UNIT_RE = re.compile(r"(\d+)\s*(?:upvotes?|points?|pts)\b", re.I)
_KILL_KEYWORDS_RE = re.compile(r"(?i)\b(verdict|load-bearing|falsifier)\b")


def detect_type(text: str) -> str:
    """Classify a blob so the right compressor runs. See KINDS for the list."""
    lines = text.split("\n")

    trimmed = text.strip()
    if len(trimmed) > 500 and (trimmed.startswith("{") or trimmed.startswith("[")):
        try:
            json.loads(trimmed)
            return "json-blob"
        except (json.JSONDecodeError, ValueError):
            pass

    # -- ledger-domain kinds (not in the source repo) --------------------
    if len(_KILL_KEYWORDS_RE.findall(text)) >= 3 and re.search(r"(?i)\bverdict\b", text):
        return "kill-transcript"

    social_signal_lines = sum(
        1 for l in lines if _SOCIAL_SIGNAL_RE.search(l) and _URL_RE.search(l)
    )
    if social_signal_lines >= 3:
        return "social-scan"

    research_signal_lines = sum(
        1
        for l in lines
        if _URL_RE.search(l) or _VERIFIED_SUSPECTED_RE.search(l) or _CLAIM_LINE_RE.search(l)
    )
    if research_signal_lines >= 3:
        return "research-dump"

    return "generic"


# ---------------------------------------------------------------------------
# Compressors (json/generic ported from squeeze.ts; ledger kinds are ours)
# ---------------------------------------------------------------------------

def compress_json(output: str) -> str:
    trimmed = output.strip()
    try:
        parsed = json.loads(trimmed)
    except (json.JSONDecodeError, ValueError):
        return output

    result = []
    if isinstance(parsed, list):
        result.append(f"JSON array: {len(parsed)} items")
        if parsed and isinstance(parsed[0], dict):
            keys = list(parsed[0].keys())
            result.append(f"Schema: {{ {', '.join(keys)} }}")
            result.append("")
            result.append("First 2 items:")
            for item in parsed[:2]:
                dumped = json.dumps(item, indent=2)
                result.append("\n".join("  " + l for l in dumped.split("\n")))
    elif isinstance(parsed, dict):
        keys = list(parsed.keys())
        result.append(f"JSON object: {len(keys)} keys")
        result.append(f"Keys: {', '.join(keys)}")
        preview_lines = json.dumps(parsed, indent=2).split("\n")
        if len(preview_lines) > THRESHOLD:
            result.append("")
            result.append("Preview (truncated):")
            result.extend("  " + l for l in preview_lines[:15])
            result.append(f"  ... {len(preview_lines) - 15} more lines")

    return "\n".join(result)


def compress_generic(output: str) -> str:
    lines = output.split("\n")

    # dedup consecutive identical lines
    deduped: list[list] = []
    for line in lines:
        if deduped and deduped[-1][0] == line:
            deduped[-1][1] += 1
        else:
            deduped.append([line, 1])

    deduped_lines = []
    for line, count in deduped:
        deduped_lines.extend([f"{line}  (x{count})"] if count > 2 else [line] * count)

    if len(deduped_lines) <= THRESHOLD + 5:
        return "\n".join(deduped_lines)

    head = deduped_lines[:HEAD_LINES]
    tail = deduped_lines[-TAIL_LINES:]
    omitted = len(deduped_lines) - HEAD_LINES - TAIL_LINES

    return "\n".join(
        head + ["", f"--- {omitted} lines omitted ({len(deduped_lines)} total) ---", ""] + tail
    )


# ---------------------------------------------------------------------------
# Ledger-domain compressors (new: not in ai-squeeze)
# ---------------------------------------------------------------------------


def compress_research_dump(output: str) -> str:
    """Keep lines carrying a URL, VERIFIED/SUSPECTED, or a claim; drop prose."""
    lines = output.split("\n")
    kept = [
        l
        for l in lines
        if _URL_RE.search(l) or _VERIFIED_SUSPECTED_RE.search(l) or _CLAIM_LINE_RE.search(l)
    ]
    dropped = len(lines) - len(kept)
    header = f"Research dump: kept {len(kept)} signal line(s), dropped {dropped} prose line(s)"
    if not kept:
        return header
    return "\n".join([header, ""] + kept)


def _line_score(line: str) -> int | None:
    m = _SCORE_KW_RE.search(line)
    if m:
        return int(m.group(1))
    m = _SCORE_UNIT_RE.search(line)
    if m:
        return int(m.group(1))
    return None


def compress_social_scan(output: str) -> str:
    """Keep the top-scored signal lines (with their URLs), deduped."""
    lines = [l for l in output.split("\n") if l.strip()]
    scored: list[tuple[int, str]] = []
    seen: set[str] = set()

    for line in lines:
        score = _line_score(line)
        if score is None:
            continue
        key = re.sub(r"\s+", " ", line.strip()).lower()
        if key in seen:
            continue
        seen.add(key)
        scored.append((score, line))

    scored.sort(key=lambda t: t[0], reverse=True)
    top = scored[:HEAD_LINES]

    header = f"Social scan: {len(lines)} lines -> {len(scored)} scored signal(s), top {len(top)} kept"
    if not top:
        return header
    body = [f"  [{score}] {line.strip()}" for score, line in top]
    return "\n".join([header, ""] + body)


def compress_kill_transcript(output: str) -> str:
    """Keep the verdict line plus any load-bearing / falsifier lines."""
    lines = output.split("\n")
    kept = [l for l in lines if _KILL_KEYWORDS_RE.search(l)]
    dropped = len(lines) - len(kept)
    header = f"Kill transcript: kept {len(kept)} verdict/load-bearing/falsifier line(s), dropped {dropped}"
    if not kept:
        return header
    return "\n".join([header, ""] + kept)


# ---------------------------------------------------------------------------
# Main entry point (ported: squeeze() in squeeze.ts + formatStats() in index.ts)
# ---------------------------------------------------------------------------

_COMPRESSORS = {
    "json-blob": compress_json,
    "research-dump": compress_research_dump,
    "social-scan": compress_social_scan,
    "kill-transcript": compress_kill_transcript,
    "generic": compress_generic,
}


KINDS = tuple(_COMPRESSORS)


def squeeze(text: str, kind: str | None = None) -> dict:
    """Compress `text` and return stats + the footer-annotated result.

    kind: force a kind instead of auto-detecting (must be one of KINDS).
    Short input (<= THRESHOLD lines) always passes through untouched, same
    as the source -- forcing a kind does not un-shortcut it.
    """
    lines = text.split("\n")
    orig_lines = len(lines)
    orig_chars = len(text)

    if orig_lines <= THRESHOLD:
        detected = "generic"
        compressed = text
    else:
        detected = kind or detect_type(text)
        compressor = _COMPRESSORS.get(detected, compress_generic)
        compressed = compressor(text)

    comp_lines = len(compressed.split("\n"))
    comp_chars = len(compressed)
    saved_chars = orig_chars - comp_chars
    tokens_saved = max(0, round(saved_chars / CHARS_PER_TOKEN))
    pct = round((saved_chars / orig_chars) * 100) if orig_chars > 0 else 0

    footer = ""
    if tokens_saved > 0:
        footer = f"\n-- squeezed [{detected}]: {orig_lines} -> {comp_lines} lines | ~{tokens_saved:,} tokens saved ({pct}%) --"

    return {
        "compressed": compressed + footer,
        "kind": detected,
        "orig_lines": orig_lines,
        "comp_lines": comp_lines,
        "orig_chars": orig_chars,
        "comp_chars": comp_chars,
        "tokens_saved": tokens_saved,
    }


# ---------------------------------------------------------------------------
# Self-test fixtures
# ---------------------------------------------------------------------------


def _fake_research_dump(n_lines: int = 60) -> str:
    prose = [
        "The market for AI-assisted changelog tooling is still forming, and most "
        "vendors have not published clear claims about data handling this year.",
        "Several public statements suggest interest in automated release notes but few "
        "teams cite concrete evidence one way or the other in coverage so far.",
        "Analysts continue to debate whether a small dev team counts as a warm lead "
        "for developer-tool outreach campaigns this quarter.",
    ]
    signal = [
        "VERIFIED: RivalCo bundles changelog generation free inside the base tier (https://example.com/pricing)",
        "SUSPECTED: AcmeDev markets an 'AI release-notes' feature with no public writeup (https://acme.example/product)",
        "Claim: small dev teams are reachable through warm intros via meetup groups",
        "VERIFIED: the platform ToS requires a published data-handling policy (https://example.org/tos)",
        "SUSPECTED: industry newsletters mention AI tools but endorse no vendor (https://example.net/newsletter)",
        "Claim: paid pilots under $500 stay below the procurement-review threshold",
    ]
    lines: list[str] = []
    i = 0
    while len(lines) < n_lines:
        lines.append(prose[i % len(prose)])
        lines.append("")
        lines.append(signal[i % len(signal)])
        lines.append("")
        i += 1
    return "\n".join(lines[:n_lines])


def _fake_social_scan(n: int = 30) -> str:
    subs = ["r/SaaS", "r/smallbusiness", "r/artificial", "r/webdev"]
    lines = []
    for i in range(n):
        score = (i * 37) % 500
        sub = subs[i % len(subs)]
        lines.append(
            f'{sub} | score {score} | upvotes {score} | "thread about AI changelog tools" | https://reddit.com/{sub}/thread{i}'
        )
    return "\n".join(lines)


def _fake_kill_transcript(n: int = 25) -> str:
    lines = ["verdict: reshape (conf 0.7)"]
    for i in range(n):
        if i % 3 == 0:
            lines.append(f"load-bearing claim C{i}: rivals bundle the feature free -- holds")
        elif i % 3 == 1:
            lines.append(f"falsifier check F{i}: no paying user cites a missing free rival -- holds")
        else:
            lines.append(f"note: background context line {i}, not load bearing")
    return "\n".join(lines)


def run_selftest() -> bool:
    ok = True

    def check(label: str, cond: bool, detail: str = "") -> None:
        nonlocal ok
        status = "ok" if cond else "FAIL"
        print(f"  [{status}] {label}{(' - ' + detail) if detail and not cond else ''}")
        if not cond:
            ok = False

    print("squeeze.py self-test")

    print("research-dump (~60 lines, mixed prose + signal):")
    dump = _fake_research_dump(60)
    r1 = squeeze(dump)
    print(f"  kind={r1['kind']} lines {r1['orig_lines']} -> {r1['comp_lines']}"
          f" tokens_saved={r1['tokens_saved']}")
    check("auto-detected as research-dump", r1["kind"] == "research-dump", r1["kind"])
    check("compressed lines < original", r1["comp_lines"] < r1["orig_lines"])
    check("footer present", "-- squeezed [" in r1["compressed"])

    print("json-blob (~200 keys):")
    blob = json.dumps({f"key_{i}": {"n": i, "note": "x" * 30} for i in range(200)}, indent=2)
    r2 = squeeze(blob)
    print(f"  kind={r2['kind']} lines {r2['orig_lines']} -> {r2['comp_lines']}"
          f" tokens_saved={r2['tokens_saved']}")
    check("auto-detected as json-blob", r2["kind"] == "json-blob", r2["kind"])
    check("compressed lines < original", r2["comp_lines"] < r2["orig_lines"])
    check("footer present", "-- squeezed [" in r2["compressed"])

    print("social-scan (~30 lines):")
    social = _fake_social_scan(30)
    r3 = squeeze(social)
    print(f"  kind={r3['kind']} lines {r3['orig_lines']} -> {r3['comp_lines']}")
    check("auto-detected as social-scan", r3["kind"] == "social-scan", r3["kind"])
    check("compressed lines < original", r3["comp_lines"] < r3["orig_lines"])
    check("top row kept has a URL", "https://reddit.com" in r3["compressed"])

    print("kill-transcript (~25 lines):")
    kill = _fake_kill_transcript(25)
    r4 = squeeze(kill)
    print(f"  kind={r4['kind']} lines {r4['orig_lines']} -> {r4['comp_lines']}")
    check("auto-detected as kill-transcript", r4["kind"] == "kill-transcript", r4["kind"])
    check("compressed lines < original", r4["comp_lines"] < r4["orig_lines"])
    check("verdict line survives", "verdict:" in r4["compressed"])
    check("a non-load-bearing note line was dropped", "not load bearing" not in r4["compressed"])

    print("generic passthrough (short input, <= THRESHOLD lines):")
    short = "\n".join(f"line {i}" for i in range(5))
    r5 = squeeze(short)
    check("kind=generic", r5["kind"] == "generic", r5["kind"])
    check("unchanged (no footer, tokens_saved=0)", r5["compressed"] == short and r5["tokens_saved"] == 0)

    print("generic dedup + head/tail (long repetitive input):")
    noisy = "\n".join(["same line"] * 3 + [f"unique {i}" for i in range(40)] + ["same line"] * 3)
    r6 = squeeze(noisy, kind="generic")
    check("compressed lines < original", r6["comp_lines"] < r6["orig_lines"])
    check("dedup marker present", "(x3)" in r6["compressed"])
    check("omission marker present", "lines omitted" in r6["compressed"])

    print("forced --kind bypasses detection:")
    r7 = squeeze(_fake_research_dump(60), kind="kill-transcript")
    check("kind honored", r7["kind"] == "kill-transcript", r7["kind"])

    print("PASS" if ok else "FAIL (see above)")
    return ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="squeeze.py",
        description="compress a verbose blob down to load-bearing signal (ai-squeeze port + ledger kinds)",
    )
    ap.add_argument("file", nargs="?", help="file to read (omit to read stdin)")
    ap.add_argument("--kind", choices=sorted(KINDS), default=None, help="force a kind instead of auto-detecting")
    ap.add_argument("--selftest", action="store_true", help="run the built-in self-test and exit")
    args = ap.parse_args(argv)

    if args.selftest:
        return 0 if run_selftest() else 1

    if args.file:
        try:
            raw = Path(args.file).read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"cannot read {args.file!r}: {type(e).__name__}: {e}", file=sys.stderr)
            return 1
    else:
        raw = sys.stdin.read()

    cleaned = strip_ansi(raw)
    result = squeeze(cleaned, kind=args.kind)
    sys.stdout.write(result["compressed"])
    if not result["compressed"].endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from ledger import fix_console_encoding
    fix_console_encoding()
    sys.exit(main())
