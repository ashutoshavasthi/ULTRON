"""The learning loop that compounds (arc/loop.py): its language is kept, grown and tested
on held-out tasks it never learns from."""

import pytest

from ultron.arc import compose, data, loop


def test_the_halves_never_mix_and_never_include_evaluation_tasks():
    tasks, practice, held = loop.halves()
    assert not set(practice) & set(held)
    assert not (set(practice) | set(held)) & data.evaluation_names()


def test_a_round_keeps_its_language_and_learns_only_from_practice(tmp_path):
    tasks, practice, held = loop.halves(quick=True)
    state = loop.load(str(tmp_path / "none.json"))
    row = loop.round_(state, tasks, practice[:12], held[:6], 20_000, 1, "test")
    assert set(state["explained"]) <= set(practice[:12])
    assert row["round"] == 1 and row["held_out"] == 6
    path = str(tmp_path / "language.json")
    loop.save(state, path)
    again = loop.load(path)
    assert again["explained"] == state["explained"]
    assert [compose.describe_step(e) for e in again["words"]] == \
        [compose.describe_step(e) for e in state["words"]]
    # the next round only works on what it hasn't explained yet
    row2 = loop.round_(again, tasks, practice[:12], held[:6], 20_000, 1, "test")
    assert row2["round"] == 2 and row2["explained"] >= row["explained"]


def test_modes_are_not_mixed(tmp_path):
    path = str(tmp_path / "language.json")
    loop.save({"rounds": [{"mode": "quick"}], "explained": {}, "words": [],
               "without": [0, 0]}, path)
    with pytest.raises(ValueError):
        loop.run(rounds=1, quick=False, state_path=path)
