"""ARC-AGI: grid perception, operations, the solver, and evaluation discipline."""

import numpy as np
import pytest

from ultron.arc import data, ops, solve
from ultron.arc.grid import background, parts, things


def g(rows):
    return np.array(rows, dtype=np.int8)


def test_perception():
    x = g([[0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 2]])
    assert background(x) == 0
    ts = things(x)
    assert sorted(t.size for t in ts) == [1, 3]
    split = g([[1, 0, 5, 2, 2], [1, 1, 5, 0, 2]])
    assert [p.tolist() for p in parts(split)] == [[[1, 0], [1, 1]], [[2, 2], [0, 2]]]


def test_operations():
    x = g([[0, 0, 0, 0], [0, 3, 3, 0], [0, 3, 0, 0], [0, 0, 0, 0]])
    assert ops.crop_content(x).tolist() == [[3, 3], [3, 0]]
    ring = g([[0, 0, 0, 0, 0], [0, 2, 2, 2, 0], [0, 2, 0, 2, 0], [0, 2, 2, 2, 0], [0, 0, 0, 0, 0]])
    assert ops.fill_enclosed(ring, 4)[2, 2] == 4
    assert ops.gravity(g([[1, 0], [0, 0]]), "down").tolist() == [[0, 0], [1, 0]]
    assert ops.upscale(g([[1, 2]]), 2).tolist() == [[1, 1, 2, 2], [1, 1, 2, 2]]
    assert ops.downscale(g([[1, 1, 2, 2], [1, 1, 2, 2]]), 2).tolist() == [[1, 2]]


def test_solver_finds_a_two_step_rule():
    # the rule: flip left-right, then fill enclosed holes with 4
    train = []
    rng = np.random.default_rng(0)
    for _ in range(3):
        x = np.zeros((7, 7), dtype=np.int8)
        r, c = rng.integers(0, 4, size=2)
        x[r:r + 3, c:c + 3] = 2
        x[r + 1, c + 1] = 0
        x[0, 6] = 1
        train.append((x, ops.fill_enclosed(x[:, ::-1], 4)))
    test = np.zeros((7, 7), dtype=np.int8)
    test[3:6, 1:4] = 2
    test[4, 2] = 0
    test[6, 0] = 1
    attempts, used, _ = solve.predict(train, [test])
    want = ops.fill_enclosed(test[:, ::-1], 4)
    assert any(np.array_equal(a, want) for a in attempts[0])


def test_learned_colour_map():
    train = [(g([[1, 2], [3, 1]]), g([[5, 6], [4, 5]])), (g([[2, 3]]), g([[6, 4]]))]
    attempts, _, _ = solve.predict(train, [g([[3, 2, 1]])])
    assert attempts[0][0].tolist() == [[4, 6, 5]]


def test_evaluation_split_is_locked():
    with pytest.raises(data.EvaluationLocked):
        data.load("arc1", "evaluation")


def test_hand_written_operations_are_frozen():
    # new abilities must come from Ultron's own library learning, not from its designer
    ctx = {"out_colours": [1, 2], "in_colours": [1, 2], "scales_up": [2], "scales_down": [2],
           "tiles": [(2, 2)], "ratios": [((2, 1), (2, 1))]}
    names = {n for n, _, _ in ops.registry(ctx)}
    assert names == set(ops.FROZEN) and len(ops.FROZEN) == 38


def test_library_learns_a_recurring_piece_and_uses_it():
    from ultron.arc import library
    # three solved tasks share "flip, then fill holes" (with different colours)
    programs = {"a": [["flip_h", None], ["fill_enclosed", 4]],
                "b": [["flip_h", None], ["fill_enclosed", 3]],
                "c": [["flip_h", None], ["fill_enclosed", 6], ["rot90", None]],
                "d": [["rot180", None]]}
    blocks = library.learn(programs)
    top = blocks[0]
    assert top["steps"] == [["flip_h", None], ["fill_enclosed", "C"]] and top["uses"] == 3
    # a piece used once is never worth its own description
    assert all(b["uses"] >= 2 for b in blocks)
    # as one step, the block makes a 3-operation program a 2-step one, so it is preferred
    from ultron.arc import grid
    grid.TASK_BACKGROUND[0] = 0
    train = []
    rng = np.random.default_rng(1)
    for _ in range(3):
        x = np.zeros((7, 7), dtype=np.int8)
        r, c = rng.integers(0, 4, size=2)
        x[r:r + 3, c:c + 3] = 2
        x[r + 1, c + 1] = 0
        x[0, 6] = 1
        train.append((x, ops.flip_v(ops.fill_enclosed(x[:, ::-1], 4), None)))
    solve.LIBRARY[0] = [top]
    try:
        found, _ = solve.solve(train, max_depth=3)
    finally:
        solve.LIBRARY[0] = None
    assert found and any(n.startswith("block") for n, _ in found[0])


def test_thing_law_with_a_default_and_marks_around_things():
    from ultron.arc import grid, objects
    grid.TASK_BACKGROUND[0] = 0
    # things with a hole turn 3; solid things stay as they are
    def pic(holed, solid):
        x = np.zeros((9, 9), dtype=np.int8)
        for r, c, w in holed:
            x[r:r + 3, c:c + w] = 1
            x[r + 1, c + 1:c + w - 1] = 0
        for r, c, h, w in solid:
            x[r:r + h, c:c + w] = 1
        return x
    train = []
    for holed, solid in [([(0, 0, 3)], [(5, 5, 2, 2)]), ([(4, 4, 4), (0, 5, 3)], [(0, 0, 3, 3)]),
                         ([(5, 0, 4)], [(0, 0, 1, 3), (0, 6, 2, 3)])]:
        x = pic(holed, solid)
        y = x.copy()
        for r, c, w in holed:
            y[r:r + 3, c:c + w][x[r:r + 3, c:c + w] == 1] = 3
        train.append((x, y))
    law = objects.learn([i for i, _ in train], [o for _, o in train])
    assert law is not None and law[1] == ("holes",)
    test = pic([(6, 6, 3)], [(0, 0, 2, 2), (3, 3, 2, 3)])
    out = objects.apply(law, test)
    assert (out[6:9, 6:9][test[6:9, 6:9] == 1] == 3).all() and (out[0:2, 0:2] == 1).all()
    # every red dot gets four yellow corners; nothing else is painted
    train = []
    for dots in ([(2, 2), (6, 5)], [(1, 6), (5, 2)], [(4, 4)]):
        x = np.zeros((8, 8), dtype=np.int8)
        y = x.copy()
        for r, c in dots:
            x[r, c] = y[r, c] = 2
            for dr in (-1, 1):
                for dc in (-1, 1):
                    y[r + dr, c + dc] = 4
        train.append((x, y))
    rule = objects.learn_marks([i for i, _ in train], [o for _, o in train])
    assert rule is not None
    t = np.zeros((8, 8), dtype=np.int8)
    t[3, 3] = 2
    out = objects.apply_marks(rule, t)
    assert out is not None and int((out == 4).sum()) == 4 and out[2, 2] == 4


def test_things_move_toward_what_stays_put():
    from ultron.arc import grid, objects
    grid.TASK_BACKGROUND[0] = 0
    # a red bar slides toward the grey block until it touches it, whichever side it is on
    def pic(bar, block):
        x = np.zeros((8, 8), dtype=np.int8)
        x[bar[0]:bar[0] + 1, bar[1]:bar[1] + 2] = 2
        x[block[0]:block[0] + 2, block[1]:block[1] + 2] = 5
        return x
    train = []
    for bar, block, end in [((1, 1), (6, 1), (5, 1)), ((6, 4), (0, 4), (2, 4)),
                            ((3, 0), (3, 5), (3, 3))]:
        train.append((pic(bar, block), pic(end, block)))
    rule = objects.learn_moves([i for i, _ in train], [o for _, o in train])
    assert rule is not None and set(m[0] for m in rule[2].values()) == {"toward"}
    out = objects.apply_moves(rule, pic((0, 6), (5, 6)))
    assert np.array_equal(out, pic((4, 6), (5, 6)))


def test_symmetry_about_its_own_centre_repairs_what_is_hidden():
    from ultron.arc import grid, symmetry
    grid.TASK_BACKGROUND[0] = 0
    rng = np.random.default_rng(3)

    def picture():
        q = rng.integers(1, 6, size=(4, 4)).astype(np.int8)
        full = np.zeros((11, 12), dtype=np.int8)
        sym = np.block([[q, q[:, ::-1]], [q[::-1], q[::-1, ::-1]]])
        full[1:9, 2:10] = sym              # symmetric about a centre that isn't the grid's
        hidden = full.copy()
        r, c = rng.integers(1, 3), rng.integers(2, 4)
        hidden[r:r + 2, c:c + 3] = 9       # a patch of colour 9 hides part of one quarter
        return hidden, full
    train = [picture() for _ in range(3)]
    rule = symmetry.learn([i for i, _ in train], [o for _, o in train], [9])
    assert rule is not None and rule[1] == 9
    x, want = picture()
    assert np.array_equal(symmetry.apply(rule, x), want)


def test_copies_of_a_template_and_lines_between_things():
    from ultron.arc import grid, objects
    grid.TASK_BACKGROUND[0] = 0
    rng = np.random.default_rng(4)
    shape = np.array([[2, 2, 0], [2, 1, 3], [0, 3, 0]], dtype=np.int8)

    def pic():
        x = np.zeros((14, 14), dtype=np.int8)
        x[0:3, 0:3] = shape                              # the template
        y = x.copy()
        for _ in range(2):
            r, c = rng.integers(5, 12), rng.integers(5, 12)
            while x[r - 1:r + 2, c - 1:c + 2].any() or y[r - 1:r + 2, c - 1:c + 2].any():
                r, c = rng.integers(5, 12), rng.integers(5, 12)
            x[r, c] = 5                                  # a marker
            sub = y[r - 1:r + 2, c - 1:c + 2]
            sub[shape != 0] = shape[shape != 0]
        return x, y
    train = [pic() for _ in range(3)]
    rule = objects.learn_copies([i for i, _ in train], [o for _, o in train])
    assert rule is not None and rule[3] == "centre"
    x, want = pic()
    assert np.array_equal(objects.apply_copies(rule, x), want)
    # cells of one colour on a row or column are joined, in their own colour
    def joined(colour):
        x = np.zeros((8, 8), dtype=np.int8)
        x[2, 1] = x[2, 6] = x[5, 3] = colour
        y = x.copy()
        y[2, 2:6] = colour
        return x, y
    train = [joined(c) for c in (1, 3, 4)]
    rule = objects.learn_gaps([i for i, _ in train], [o for _, o in train])
    x, want = joined(7)                                  # a colour it never saw
    assert rule is not None and np.array_equal(objects.apply_gaps(rule, x), want)


def test_summary_laws_count_and_blocks():
    from ultron.arc import grid, summary
    grid.TASK_BACKGROUND[0] = 0
    rng = np.random.default_rng(5)

    def scattered(n):
        x = np.zeros((10, 10), dtype=np.int8)
        cells = rng.choice(100, size=n, replace=False)
        for k in cells:
            r, c = divmod(int(k), 10)
            if all(x[r + dr, c + dc] == 0 for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                   if 0 <= r + dr < 10 and 0 <= c + dc < 10):
                x[r, c] = 4
        y = np.zeros((int((x == 4).sum()),) * 2, dtype=np.int8)
        np.fill_diagonal(y, 4)
        return x, y
    train = [scattered(n) for n in (3, 5, 2)]
    rule = summary.learn([i for i, _ in train], [o for _, o in train])
    x, want = scattered(4)
    assert rule is not None and np.array_equal(summary.apply(rule, x), want)
    # stripes of uniform colour: one cell per block
    pic = np.repeat(np.repeat(np.array([[1, 2], [3, 4]], dtype=np.int8), 3, 0), [2, 4], 1)
    assert np.array_equal(summary.blocks(pic, False), [[1, 2], [3, 4]])


def test_copies_arranged_in_a_grid():
    from ultron.arc import grid, tiles
    grid.TASK_BACKGROUND[0] = 0
    rng = np.random.default_rng(6)
    pics = [rng.integers(0, 4, size=(3, 3)).astype(np.int8) for _ in range(4)]
    make = lambda g: np.block([[g, np.rot90(g, 3)], [np.rot90(g, 1), g[::-1, ::-1]]])
    rule = tiles.learn(pics[:3], [make(g) for g in pics[:3]])
    assert rule is not None and np.array_equal(tiles.apply(rule, pics[3]), make(pics[3]))


def test_intuition_learns_to_rank_the_step_that_leads_somewhere():
    from ultron.arc import intuition as I
    rng = np.random.default_rng(7)
    # looks of half-built programs: those on the way are closer to the target
    X = rng.normal(size=(200, 17))
    y = (X[:, 1] + 0.5 * X[:, 3] > 0.8).astype(float)
    model = I.Model().train(X, y)
    on, off = X[y == 1].mean(axis=0), X[y == 0].mean(axis=0)
    assert model.score(on.copy()) > model.score(off.copy())
    again = I.Model().train(X, y)                       # deterministic
    assert np.allclose(again.w, model.w)


def _flipped_with_holes(seed, n=3):
    rng = np.random.default_rng(seed)
    train = []
    for _ in range(n):
        x = np.zeros((7, 7), dtype=np.int8)
        r, c = rng.integers(0, 4, size=2)
        x[r:r + 3, c:c + 3] = 2
        x[r + 1, c + 1] = 0
        x[0, 6] = 1
        train.append((x, ops.fill_enclosed(x[:, ::-1], 4)))
    return train


def test_a_description_with_exceptions_counts_only_when_it_is_shorter():
    from ultron.arc import descriptions, grid
    grid.TASK_BACKGROUND[0] = 0
    train = _flipped_with_holes(3)
    ins, outs = [i for i, _ in train], [o for _, o in train]
    best = descriptions.Best(ins, outs, 237)
    # "flip" alone gets all but the hole right: a few exceptions, far shorter than
    # listing every cell that changes
    flipped = [i[:, ::-1] for i in ins]
    best.offer((("flip_h", None),), 1, flipped, outs)
    assert best.program == (("flip_h", None),) and best.wrong == 3 and best.saving() > 0
    # a program that leaves everything wrong is no description at all
    worse = descriptions.Best(ins, outs, 237)
    worse.offer((("rot90", None),), 1, [np.full_like(o, 7) for o in outs], outs)
    assert worse.program == ()
    # an exact explanation is the shortest description
    best.offer_exact((("flip_h", None), ("fill_enclosed", 4)), 2)
    assert best.wrong == 0


def test_blocks_with_an_open_parameter_or_a_law_tail_and_best_first_search():
    from ultron.arc import grid, library
    from ultron.arc import intuition as I
    # four tasks share "flip, then fill holes, then a thing law" -- the colour differs
    programs = {t: [["flip_h", None], ["fill_enclosed", c], ["things", None]]
                for t, c in zip("abcd", (4, 3, 6, 1))}
    programs["e"] = [["rot180", None]]
    blocks = library.learn(programs)
    top = blocks[0]
    assert top["steps"] == [["flip_h", None], ["fill_enclosed", "C"], ["things", None]]
    assert library.law_tail(top) == "things" and top["uses"] == 4
    # a two-step piece shared by two tasks doesn't pay for its own description (2 x 1 - 2)
    assert library.learn({"a": programs["a"][1:], "b": programs["b"][1:]}) == []
    # any parameter may be left open, not only a colour
    gravity = {t: [["gravity", d], ["crop_content", None]] for t, d in
               zip("abc", ("down", "up", "left"))}
    assert library.learn(gravity)[0]["steps"] == [["gravity", "*"], ["crop_content", None]]
    # the block runs as one step: flip, fill, and the law is learned on the result
    grid.TASK_BACKGROUND[0] = 0
    train = []
    for i, o in _flipped_with_holes(1):
        i, o = i.copy(), o.copy()
        i[6, 0] = 2                     # a lone speck of the same colour stays as it is
        o = np.where(o == 2, 5, o).astype(np.int8)
        o[6, 6] = 2
        train.append((i, o))
    solve.LIBRARY[0] = [top]
    try:
        found, _ = solve.solve(train, max_depth=2)
        assert found and found[0][0][0] == "block1" and found[0][1][0] == "things"
        # best first across depths (with intuition on) finds it too
        solve.INTUITION[0] = I.Model(np.zeros(2 * I.N_LOOK + 3), np.zeros(2 * I.N_LOOK + 3),
                                     np.ones(2 * I.N_LOOK + 3))
        again, _ = solve.solve(train, max_depth=2)
        assert again and again[0][0][0] == "block1"
    finally:
        solve.LIBRARY[0] = None
        solve.INTUITION[0] = None


def test_small_steps_compose_and_ultron_builds_its_own_from_them():
    from ultron.arc import compose as Cm
    from ultron.arc import grid
    grid.TASK_BACKGROUND[0] = 0
    # "small things turn green": a law about things, written in small steps
    x = g([[1, 0, 0, 2, 2], [0, 0, 0, 2, 2], [4, 0, 0, 0, 0], [0, 0, 5, 5, 5]])
    prog = Cm.parse("paint(x, recolour(with(things(x), size, 1), 3))")
    want = x.copy()
    want[0, 0] = want[2, 0] = 3
    assert np.array_equal(Cm.run(prog, x), want)
    assert Cm.show(prog) == "paint(x, recolour(with(things(x), size, 1), 3))"
    # the search finds a composition no single frozen operation is: blow the picture up
    # by the number of things in it
    train = []
    for dots in ([(0, 0, 1), (2, 2, 2)], [(0, 0, 3), (0, 2, 1), (2, 1, 4)],
                 [(0, 2, 2), (2, 0, 2)]):
        p = np.zeros((3, 3), dtype=np.int8)
        for r, c, v in dots:
            p[r, c] = v
        k = len(dots)
        train.append((p, np.kron(p, np.ones((k, k), dtype=np.int8))))
    found, _ = Cm.search(train, budget=40_000)
    assert found and Cm.show(found[0]) == "upscale(x, count(things(x)))"
    # library learning: a piece several explanations share becomes a step of its own,
    # with a typed hole where they differ, only when it shortens the description
    progs = {t: Cm.parse(s) for t, s in {
        "a": "paint(x, things(flip(x)))", "b": "paint(x, things(flip_v(x)))",
        "c": "paint(x, things(rot180(x)))", "d": "upscale(x, 2)"}.items()}
    lib = Cm.learn_library(progs)
    assert any(Cm.show(e["pattern"]) == "paint(x, things(_a))" and e["args"] == ["G"]
               for e in lib)
    assert Cm.learn_library({"d": progs["d"]}) == []
    # and the search uses it as one step
    Cm.LIBRARY[0] = lib
    try:
        y = g([[1, 0, 0], [0, 2, 0], [0, 0, 0]])
        own = [e for e in lib if Cm.show(e["pattern"]) == "paint(x, things(_a))"][0]
        assert np.array_equal(Cm.run((own["name"], ("transpose", ("x",))), y),
                              Cm.run(Cm.parse("paint(x, things(transpose(x)))"), y))
    finally:
        Cm.LIBRARY[0] = None
