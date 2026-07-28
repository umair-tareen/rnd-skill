"""test_fixture.py -- parse a COMMITTED artifact this process did not create.

This exists because of SPEC bug B6, and because B6 was the FOURTH time this
repo shipped a rule that lived only in prose (see also B1: mutation API,
B4: resume manifest, and server.py's absolute-path rule).

B6 in one line: a cp1252/utf-8 round trip mojibake'd the parser's section-sign
regexes, and every self-test STAYED GREEN because each one writes and parses
with the same corrupted symbols -- self-consistently blind -- while every real
thesis on disk parsed as empty. The lesson recorded was "always verify against
one artifact the current process did not create." A lesson is prose. This file
is the mechanism.

`examples/acme/acme.md` is checked into git, byte-stable, and was produced by
an earlier process. Parsing it and asserting known-good values is therefore a
true cross-process check: any writer+reader corruption, any silent schema
break, any encoding regression makes THIS fail while the self-tests still
pass. Run in CI on every push, on both OSes and both Python versions.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import ledger  # noqa: E402
import trim    # noqa: E402

THESIS = ROOT / "examples" / "acme" / "acme.md"
RUN2 = ROOT / "examples" / "acme" / "run-2-recheck"
RUN1 = ROOT / "examples" / "acme" / "run-1-full-sweep"


def main() -> int:
    assert THESIS.exists(), f"fixture missing: {THESIS}"

    raw = THESIS.read_text(encoding="utf-8")
    # 1. the §-sections survived as real U+00A7, in the FILE, not in a string
    #    this process just wrote. This is the exact B6 detector.
    for section in ("§T THESIS", "§C CLAIMS", "§F FLIPS",
                    "§Q OPEN", "§D DIFF"):
        assert f"## {section}" in raw, f"section heading corrupted: {section!r}"
    assert "Â§" not in raw, "mojibake: section sign double-encoded in the fixture"

    # 2. the parser actually reads it (B6 made this return zero claims)
    doc = ledger.parse(THESIS)
    assert len(doc["claims"]) == 8, f"expected 8 claims, parsed {len(doc['claims'])}"
    assert len(doc["flips"]) == 2, doc["flips"]
    assert len(doc["opens"]) == 3, doc["opens"]
    assert len(doc["diffs"]) == 2, doc["diffs"]

    by_st = {}
    for c in doc["claims"]:
        by_st[c["st"]] = by_st.get(c["st"], 0) + 1
    assert by_st == {"V": 4, "A": 3, "O": 1}, by_st
    assert sum(1 for c in doc["claims"] if c["load_bearing"]) == 2

    # 3. classes parsed (the added column did not shift cells)
    by_cls = {}
    for c in doc["claims"]:
        by_cls[c.get("cls", "-")] = by_cls.get(c.get("cls", "-"), 0) + 1
    assert by_cls == {"world": 4, "customer": 2, "internal": 2}, by_cls

    # 4. the derived demand stamp is present on the stored verdict line AND
    #    recomputes to the same thing (V10 end to end, on a real file)
    assert "demand-UNVALIDATED" in raw, "stamp missing from the committed fixture"
    ds = ledger.demand_status(doc)
    assert ds["unvalidated"] is True and ds["total"] == 2 and ds["verified"] == 0, ds
    assert "C4" in ds["flag"] and "C5" in ds["flag"], ds["flag"]

    # 5. verdict fields round-trip (the trailing derived flag must not leak
    #    into the parsed date -- the regex that broke once already)
    v = doc["verdict"]
    assert v["verdict"] == "reshape", v
    assert abs(v["conf"] - 0.6) < 1e-9, v
    assert v["run"] == 2 and v["date"] == "2026-07-25", v

    # 6. §Q closed_by survived (evidence-vs-guess accounting depends on it)
    q1 = next(q for q in doc["opens"] if q["id"] == "Q1")
    assert q1["st"] == "x" and q1["closed_by"] == "C8", q1

    # 7. the meter + yield reproduce on committed run folders
    assert RUN1.exists() and RUN2.exists(), "example run folders missing"
    m = trim.measure_run(RUN2, THESIS, model="opus")
    assert m["fixed"]["tokens"] > 0 and m["marginal"]["tokens"] > 0, m
    y = trim.measure_yield(THESIS, run=2)
    assert y["available"] and y["run"] == 2, y
    assert y["claims_added"] == 1 and y["load_bearing_added"] == 0, y
    assert y["closed"]["evidence"] == ["Q1<-C8"], y["closed"]
    assert y["demand"]["unvalidated"] is True

    # 8. staleness reads the fixture (the morning-brief path)
    rep = ledger.stale_report(doc, days=0, today="2026-07-26")
    assert rep["any"] is True
    assert any(f["id"] == "F1" for f in rep["never_checked"]), rep["never_checked"]

    print("PASS: fixture test -- committed examples/acme parsed clean "
          "(8 claims, classes intact, stamp derived, meter+yield reproduce)")
    return 0


if __name__ == "__main__":
    ledger.fix_console_encoding()
    sys.exit(main())
