"""The Code stage (docs/STAGE_CODE_PLAN.md): lesson 100, reading Engc expressions (C1)."""

import ast
import pathlib

import pytest

from ultron.code import sandbox

pytestmark = pytest.mark.skipif(not sandbox.available(), reason=f"needs Engc: {sandbox.INSTALL}")

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_sandbox_reports_only_what_was_printed():
    assert sandbox.run("PRINT 3 PLUS 4 .") == {"ok": True, "printed": ["7"], "error": None}
    assert not sandbox.run("PRINT 3 MODULO 0 .")["ok"]
    assert sandbox.run("PRINT 3 PLUS .")["error"] == "does not compile"


def test_ultron_never_sees_the_teachers_tables():
    """The brain-side code reads programs and printed lines only: it imports nothing
    from the Trainer, the Judge or Engc itself."""
    for path in (ROOT / "ultron" / "code" / "reading.py", ROOT / "ultron" / "brain" / "stepping.py"):
        tree = ast.parse(path.read_text())
        names = [n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
        names += [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
        assert not any("trainer" in m or "judge" in m or "engc" in m for m in names), path


def test_stepping_finds_a_law_no_short_program_explains():
    """MODULO: no program of size 7 explains it; stepping (a usual rule, when it fails,
    what instead) does, and it holds far beyond what was seen."""
    import copy

    from ultron.brain import stepping
    from ultron.brain.brain import Brain
    from ultron.brain.dsl import safe_evaluate
    brain = Brain.load(str(ROOT / "brain" / "ultron_brain.json"))
    lib = copy.deepcopy(brain.library)
    expr, step, story, runs = stepping.by_stepping(
        "mod", lambda x, y: x % y, lib, brain.constants(), brain.primitives())
    assert expr is not None and runs <= 40
    assert lib.cycles.get(step.name) == "param"
    for x, y in [(999, 7), (12345, 97), (5, 9), (0, 3), (-7, 3)]:
        assert safe_evaluate(expr, {"x": x, "y": y}, lib) == x % y


def test_lesson_100_reads_held_out_expressions(trained):
    """C1: >= 190/200 held-out expressions, precision >= 99%, >= 30 points over the best
    baseline, from <= 400 runs."""
    _, results = trained
    r = results[100]
    s = r["items"][0]["scores"]
    assert r["passed"]
    assert s["ultron"][0] >= 190 and r["precision"] >= 0.99
    best = max(v[0] for k, v in s.items() if k != "ultron")
    assert s["ultron"][0] - best >= 60
    assert r["runs"]["trainer"] + r["runs"]["own"] <= 400


def test_films_show_each_line_and_memory():
    film = sandbox.trace("SET x TO 2 .\nSET x TO x TIMES 3 .\nPRINT x .\n")
    assert film["printed"] == ["6"]
    assert [s["line"] for s in film["steps"]] == [1, 2, 3]
    assert film["steps"][2]["memory"] == {"x": 6} and film["final"] == {"x": 6}


def test_statement_reader_never_sees_engc_words():
    """No Engc keyword is written into the statement learner: every word it uses
    comes from what it watched."""
    text = (ROOT / "ultron" / "code" / "statements.py").read_text()
    for word in ("SET", "PRINT", "WHILE", "FOR EACH", "END", "ELSE", "CALL", "RETURN",
                 "DEFINE", "THE LIST", "ADDED", "EQUAL TO"):
        assert f'"{word}"' not in text and f"'{word}'" not in text, word


def test_lesson_101_reads_held_out_programs(trained):
    """C2: >= 180/200 held-out programs, precision >= 98%, >= 60 points over the best
    baseline, from <= 1,000 runs."""
    _, results = trained
    r = results[101]
    s = r["items"][0]["scores"]
    assert r["passed"]
    assert s["ultron"][0] >= 180 and r["precision"] >= 0.98
    best = max(v[0] for k, v in s.items() if k != "ultron")
    assert s["ultron"][0] - best >= 60
    assert r["runs"]["trainer"] + r["runs"]["own"] <= 1000
