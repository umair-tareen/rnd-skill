"""squeeze.py -- typed lossy compression: verbose blob -> load-bearing signal.

Why: /rnd's thesis ledger (see OS\\capabilities\\rnd-thesis-ledger-SPEC.md, S:I.3)
must stay token-minimal even though evidence keeps arriving as noisy tool
output, research dumps, social scans, and kill-check transcripts. This is the
INTAKE FILTER: run any blob through squeeze() BEFORE it enters context or gets
written into a thesis file's SC/SQ sections.

Provenance: ports skibidiskib/Ai-squeeze (github.com/skibidiskib/Ai-squeeze,
src/squeeze.ts + src/index.ts) line-for-line where the shapes match, same
defaults (THRESHOLD=20 lines, HEAD=10, TAIL=10, 4 chars/token estimate, and
the exact CLI footer format). Adds three ledger-domain kinds the source
repo has no notion of, because /rnd evidence is not CLI tool output:
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

KINDS = (
    "typescript-errors",
    "test-results",
    "npm-install",
    "stack-trace",
    "git-log",
    "json-blob",
    "research-dump",
    "social-scan",
    "kill-transcript",
    "generic",
)


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
# Detection (ported: detectType() in squeeze.ts, + 3 ledger-domain additions)
# ---------------------------------------------------------------------------

_TS_ERROR_RE = re.compile(r"error TS\d+", re.M)
_TS_ERROR_LOC_RE = re.compile(r"\.tsx?\(\d+,\d+\):\s*error", re.M)
_TEST_TESTS_RE = re.compile(r"Tests?:\s+\d+", re.M)
_TEST_PASSFAIL_RE = re.compile(r"(?:passed|failed|skipped)", re.I)
_TEST_PASSFAIL_LINE_RE = re.compile(r"(?:PASS|FAIL)\s+\S+", re.M)
_TEST_SUITES_RE = re.compile(r"Test Suites?:", re.M)
_TEST_CHECKMARK_LINE_RE = re.compile(r"^\s*[✓✗✕●]\s")
_NPM_ADDED_RE = re.compile(r"added \d+ packages?", re.M)
_NPM_WARN_RE = re.compile(r"(?:npm|pnpm|yarn) warn", re.I | re.M)
_ERROR_HEADER_RE = re.compile(r"(?:Error|Exception|TypeError|ReferenceError|SyntaxError):")
_AT_LINE_RE = re.compile(r"^\s+at\s")
_GIT_HASH_LINE_RE = re.compile(r"^[a-f0-9]{7,12}\s")

_URL_RE = re.compile(r"https?://\S+")
_VERIFIED_SUSPECTED_RE = re.compile(r"\b(VERIFIED|SUSPECTED)\b")
_CLAIM_LINE_RE = re.compile(r"(?i)^\s*[-*\d.]*\s*claim\s*:")
_SOCIAL_SIGNAL_RE = re.compile(r"(?i)\b(subreddit|upvotes?|r/\w+)\b")
_SCORE_KW_RE = re.compile(r"score[:\s]+(\d+)", re.I)
_SCORE_UNIT_RE = re.compile(r"(\d+)\s*(?:upvotes?|points?|pts)\b", re.I)
_KILL_KEYWORDS_RE = re.compile(r"(?i)\b(verdict|load-bearing|falsifier)\b")


def detect_type(text: str) -> str:
    """Classify a blob so the right compressor runs. See KINDS for the list."""
    if _TS_ERROR_RE.search(text) or _TS_ERROR_LOC_RE.search(text):
        return "typescript-errors"

    lines = text.split("\n")
    checkmark_lines = sum(1 for l in lines if _TEST_CHECKMARK_LINE_RE.match(l))
    if (
        (_TEST_TESTS_RE.search(text) and _TEST_PASSFAIL_RE.search(text))
        or (_TEST_PASSFAIL_LINE_RE.search(text) and _TEST_SUITES_RE.search(text))
        or checkmark_lines > 5
    ):
        return "test-results"

    if _NPM_ADDED_RE.search(text) or _NPM_WARN_RE.search(text):
        return "npm-install"

    if _ERROR_HEADER_RE.search(text):
        at_lines = sum(1 for l in lines if _AT_LINE_RE.match(l))
        if at_lines >= 3:
            return "stack-trace"

    hash_lines = sum(1 for l in lines if _GIT_HASH_LINE_RE.match(l))
    if hash_lines > 10:
        return "git-log"

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
# Compressors ported from squeeze.ts (same behavior/defaults as the source)
# ---------------------------------------------------------------------------

_TS_ERROR_LINE_RE = re.compile(r"^(.+?)\((\d+),(\d+)\):\s*error\s+(TS\d+):\s*(.+)$")


def compress_typescript_errors(output: str) -> str:
    lines = output.split("\n")
    errors = []
    non_error_lines = []
    for line in lines:
        m = _TS_ERROR_LINE_RE.match(line)
        if m:
            errors.append(
                {"file": m.group(1), "line": int(m.group(2)), "code": m.group(4), "message": m.group(5)}
            )
        elif line.strip():
            non_error_lines.append(line)

    if not errors:
        return output

    files = {e["file"] for e in errors}
    by_code: dict[str, int] = {}
    for e in errors:
        by_code[e["code"]] = by_code.get(e["code"], 0) + 1
    sorted_codes = sorted(by_code.items(), key=lambda kv: kv[1], reverse=True)

    result = [f"TypeScript: {len(errors)} errors in {len(files)} files", "", "By error code:"]
    for code, count in sorted_codes[:5]:
        result.append(f"  {code}: {count} occurrences")
    if len(sorted_codes) > 5:
        result.append(f"  ... and {len(sorted_codes) - 5} more error types")

    result.append("")
    result.append("First errors:")
    shown: set[str] = set()
    for e in errors:
        key = f"{e['code']}:{e['message']}"
        if key in shown:
            continue
        shown.add(key)
        result.append(f"  {e['file']}:{e['line']} {e['code']}: {e['message']}")
        if len(shown) >= 5:
            break

    summary_line = next((l for l in non_error_lines if re.search(r"Found \d+ error", l, re.I)), None)
    if summary_line:
        result.append("")
        result.append(summary_line)

    return "\n".join(result)


def compress_test_results(output: str) -> str:
    lines = output.split("\n")
    result = []

    summary_lines = [
        l
        for l in lines
        if re.search(r"Test Suites?:", l, re.I)
        or re.search(r"Tests?:", l, re.I)
        or re.search(r"Snapshots?:", l, re.I)
        or re.search(r"Time:", l, re.I)
        or re.search(r"^Ran \d+ tests?", l, re.I)
    ]

    fail_blocks: list[str] = []
    in_fail_block = False
    current_block: list[str] = []

    for line in lines:
        if re.match(r"^\s*(?:FAIL|✗|✕|●)\s", line):
            if current_block:
                fail_blocks.append("\n".join(current_block))
            current_block = [line]
            in_fail_block = True
        elif in_fail_block:
            if line.strip() == "" and len(current_block) > 3:
                fail_blocks.append("\n".join(current_block))
                current_block = []
                in_fail_block = False
            elif re.match(r"^\s*(?:PASS|FAIL|✓|✗|✕|●)\s", line):
                fail_blocks.append("\n".join(current_block))
                if re.search(r"(?:FAIL|✗|✕)", line):
                    current_block = [line]
                else:
                    current_block = []
                    in_fail_block = False
            else:
                current_block.append(line)
    if in_fail_block and current_block:
        fail_blocks.append("\n".join(current_block))

    error_lines = [
        l
        for l in lines
        if re.search(r"Expected:", l)
        or re.search(r"Received:", l)
        or re.search(r"AssertionError", l)
        or re.search(r"thrown:", l)
        or re.search(r"Error:", l)
    ]

    if summary_lines:
        result.extend(l.strip() for l in summary_lines)

    pass_count = sum(1 for l in lines if re.match(r"^\s*(?:PASS|✓)\s", l))
    fail_count = sum(1 for l in lines if re.match(r"^\s*(?:FAIL|✗|✕)\s", l))

    if not summary_lines and (pass_count > 0 or fail_count > 0):
        result.append(f"Results: {pass_count} passed, {fail_count} failed")

    if fail_blocks:
        result.append("")
        result.append("FAILURES:")
        for block in fail_blocks[:5]:
            result.append("\n".join(block.split("\n")[:6]))
            result.append("")
        if len(fail_blocks) > 5:
            result.append(f"... and {len(fail_blocks) - 5} more failures")
    elif error_lines:
        result.append("")
        result.append("Errors:")
        result.extend("  " + l.strip() for l in error_lines[:5])

    return "\n".join(result)


def compress_npm_install(output: str) -> str:
    lines = output.split("\n")
    result = []

    summary_line = next((l for l in lines if re.search(r"added \d+ packages?", l, re.I)), None)
    if summary_line:
        result.append(summary_line.strip())

    warnings = [l for l in lines if re.search(r"npm warn|pnpm warn|yarn warn", l, re.I)]
    deprecations = [l for l in warnings if re.search(r"deprecated", l, re.I)]
    vulnerabilities = next((l for l in lines if re.search(r"\d+ vulnerabilit", l, re.I)), None)

    if deprecations:
        result.append(f"{len(deprecations)} deprecation warning(s)")
    if len(warnings) - len(deprecations) > 0:
        result.append(f"{len(warnings) - len(deprecations)} other warning(s)")
    if vulnerabilities:
        result.append(vulnerabilities.strip())

    fund_line = next((l for l in lines if re.search(r"\d+ packages? are looking for funding", l, re.I)), None)
    if fund_line:
        result.append(fund_line.strip())

    return "\n".join(result) if result else "npm install completed (no summary found)"


def compress_stack_trace(output: str) -> str:
    lines = output.split("\n")
    result = []

    error_idx = next((i for i, l in enumerate(lines) if _ERROR_HEADER_RE.search(l)), -1)
    if error_idx == -1:
        return output

    context_start = max(0, error_idx - 2)
    result.extend(lines[context_start : error_idx + 1])

    at_lines = [l for l in lines[error_idx + 1 :] if _AT_LINE_RE.match(l)]
    user_frames = [l for l in at_lines if "node_modules" not in l and "internal/" not in l]
    lib_frames = [l for l in at_lines if "node_modules" in l or "internal/" in l]

    result.extend(user_frames[:5])
    if len(user_frames) > 5:
        result.append(f"    ... {len(user_frames) - 5} more user frames")
    if lib_frames:
        result.append(f"    ... {len(lib_frames)} library/internal frames")

    after_stack = [l for l in lines[error_idx + 1 :] if not _AT_LINE_RE.match(l) and l.strip()]
    if after_stack:
        result.append("")
        result.extend(after_stack[:3])

    return "\n".join(result)


def compress_git_log(output: str) -> str:
    lines = [l for l in output.split("\n") if l.strip()]
    total = len(lines)
    if total <= THRESHOLD:
        return output

    result = [f"Git log: {total} entries", "", "Recent:"]
    result.extend("  " + l for l in lines[:10])

    if total > 15:
        result.append(f"  ... {total - 15} more commits ...")
        result.append("")
        result.append("Oldest shown:")
        result.extend("  " + l for l in lines[-5:])

    return "\n".join(result)


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
        if count > 2:
            deduped_lines.append(f"{line}  (x{count})")
        elif count == 2:
            deduped_lines.append(line)
            deduped_lines.append(line)
        else:
            deduped_lines.append(line)

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
    "typescript-errors": compress_typescript_errors,
    "test-results": compress_test_results,
    "npm-install": compress_npm_install,
    "stack-trace": compress_stack_trace,
    "git-log": compress_git_log,
    "json-blob": compress_json,
    "research-dump": compress_research_dump,
    "social-scan": compress_social_scan,
    "kill-transcript": compress_kill_transcript,
    "generic": compress_generic,
}


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


def _fake_ts_errors(n_errors: int = 480) -> str:
    codes = ["TS2322", "TS2345", "TS2554", "TS7006", "TS2531"]
    lines = []
    for i in range(n_errors):
        f = f"src/module{i % 12}.ts"
        code = codes[i % len(codes)]
        lines.append(f"{f}({i % 200 + 1},{i % 40 + 1}): error {code}: Type mismatch in expression #{i}.")
    lines.append(f"Found {n_errors} errors.")
    return "\n".join(lines)


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

    print("typescript-errors (~500 lines):")
    ts = _fake_ts_errors(480)
    r2 = squeeze(ts)
    print(f"  kind={r2['kind']} lines {r2['orig_lines']} -> {r2['comp_lines']}"
          f" tokens_saved={r2['tokens_saved']}")
    check("auto-detected as typescript-errors", r2["kind"] == "typescript-errors", r2["kind"])
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
    # cp1252 console guard: reconfigure to utf-8 so a stray unicode char
    # (checkmarks in test-results input, etc.) never crashes stdout.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    sys.exit(main())
