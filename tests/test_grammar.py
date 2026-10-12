"""Stage 3, L3: how words combine, found as the shortest account of what was heard."""

from ultron.brain import grammar as G
from ultron.senses.tabletop import COLOURS, SHAPES, SIZES
from ultron.trainer.grammar_lessons import (EXAM, HowWordsCombine, held_out_use, readings,
                                            sentence_words)

COLOUR, SIZE, SHAPE = sorted(COLOURS), sorted(SIZES), list(SHAPES)
CATEGORIES = {"colour": {"groups": [[i, i] for i in range(4)]},
              "size": {"groups": [[0, 0], [1, 1]]},
              "shape": {"groups": [[0, 0], [1, 1], [2, 2]]}}
KNOWN = {**{c: (("colour", i),) for i, c in enumerate(COLOUR)},
         **{s: (("size", i),) for i, s in enumerate(SIZE)},
         **{s: (("shape", i),) for i, s in enumerate(SHAPE)}, "the": ()}


def _as_seen(things):
    """A table as Ultron would see it, made straight from the true things."""
    table = [{"q": {"place": [t["x"], G.SURE], "height": [-t["y"], G.SURE],
                    "size": [10.0, 2.0]}} for t in things]
    kinds = [{"colour": COLOUR.index(t["colour"]), "size": SIZE.index(t["size"]),
              "shape": SHAPE.index(t["shape"])} for t in things]
    return table, kinds


THE = ("the one", None, G.MOD_AFTER)
LEFT = ("order", ("place", "<"), ("/", G.MOD_BEFORE, G.N))
ABOVE = ("order", ("height", ">"), ("/", G.MOD_BEFORE, G.N))
AND = ("together", None, ("/", G.MOD_BEFORE, G.N))


def _lexicon():
    lex = {w: ("kind", m, G.N if w in SHAPE else G.MOD_AFTER) for w, m in KNOWN.items() if m}
    lex.update({"the": THE, "left": LEFT, "right": ("order", ("place", ">"), LEFT[2]),
                "above": ABOVE, "below": ("order", ("height", "<"), ABOVE[2]), "and": AND,
                "of": ("nothing", None, None), "that": ("nothing", None, None),
                "is": ("nothing", None, None)})
    return lex


def test_the_one_grammar_reads_nesting_and_joining_at_any_depth():
    lesson = HowWordsCombine(3)
    lex = _lexicon()
    for kind, _ in EXAM:
        for said, _, things, meant, _ in lesson.talks(kinds=[(kind, 8)]):
            table, kinds = _as_seen(things)
            got, why = G.understand(lex, [], said.split(), table, kinds)
            assert got == sorted(meant), (said, why)


def test_teaching_never_uses_a_held_out_way_of_speaking():
    lesson = HowWordsCombine(4)
    for said, _, things, meant, kind in lesson.talks(80):
        assert not held_out_use(said.split())
        assert said.count(" and ") <= 1
        assert readings(said.split(), things) == {frozenset(meant)}
    for said, *_ in lesson.talks(kinds=[("words in new places", 10)]):
        assert held_out_use(said.split())


def test_a_grammar_is_found_from_what_was_heard():
    """From sentences alone (no one says which thing is meant or what a word does), the
    shortest account finds what 'the', the relation words and 'and' do and how they
    combine; sizes and colours come before the noun."""
    lesson = HowWordsCombine(5)
    heard = []
    for said, _, things, meant, _ in lesson.talks(160):
        table, kinds = _as_seen(things)
        heard.append((said.split(), table, kinds))
    lex = G.learn_grammar(heard, CATEGORIES, known=KNOWN)
    assert lex["the"] == THE
    assert lex["left"] == LEFT and lex["above"] == ABOVE
    assert lex["right"][1] == ("place", ">")
    assert lex["and"][0] == "together"
    assert lex["red"][2] == G.MOD_AFTER and lex["ball"][2] == G.N
    assert lex["of"][0] == "nothing"


def test_lesson_33_exam(trained):
    """L3 on the trained brain: the things meant >= 95% on each held-out kind of sentence."""
    r = trained[1][33]
    assert r["passed"]


def test_grammar_failure_lab_breakpoints_stay(trained):
    """Breakpoints found by the failure lab (2026-10-11) must never move back, and in no
    row does it give a wrong answer."""
    from ultron.judge import failures
    rows = {r["level"]: r for r in failures.grammar_stress(trained[0])["rows"]}
    for level in ("0% of sentences have a word misheard",
                  "20% of sentences are about another table"):
        assert rows[level]["ok"], level
    for r in rows.values():
        assert r["right"] == r["gave"], r["level"]
