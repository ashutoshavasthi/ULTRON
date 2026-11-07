"""Dreams (puzzles Ultron makes from its own language) and the guide learned from them."""

import numpy as np

from ultron.arc import compose, dreams, loop


def _setup():
    tasks, practice, held = loop.halves(quick=True)
    return tasks, practice, held


def test_dreams_are_reproducible_and_use_only_practice_pictures():
    tasks, practice, held = _setup()
    a = dreams.make(tasks, practice, n=40, seed=3)
    b = dreams.make(tasks, practice, n=40, seed=3)
    assert len(a) == 40
    assert [compose.show(d["program"]) for d in a] == [compose.show(d["program"]) for d in b]
    pictures = {compose.key(g) for t in practice for pairs in (tasks[t]["train"], tasks[t]["test"])
                for g, _ in pairs}
    for d in a:
        for x, y in d["train"] + d["test"]:
            assert compose.key(x) in pictures
            assert np.array_equal(compose.run(d["program"], x), y)    # it knows the answer


def test_the_guide_ranks_steps_for_each_puzzle():
    tasks, practice, held = _setup()
    dreamt = dreams.make(tasks, practice, n=200, seed=1)
    names = [n for n, _, _, _ in compose.STEPS]
    guide = dreams.Guide.fit([(d["train"], d["program"]) for d in dreamt], names, epochs=50)
    a, b = guide(tasks[held[0]]["train"]), guide(tasks[held[1]]["train"])
    assert set(a) == set(names) and all(0 <= v <= 1 for v in a.values())
    assert a != b                                       # different puzzles, different order
    again = dreams.Guide.from_json(guide.to_json())
    assert abs(again(tasks[held[0]]["train"])["paint"] - a["paint"]) < 1e-4
