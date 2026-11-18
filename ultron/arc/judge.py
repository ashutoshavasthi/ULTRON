"""The judge: one set of answers from Ultron's engines (docs/history/PLAN_M1_M2.md, M2).

For each test input of a puzzle, at most two answers (the official ARC rule):
  1. its programs (engine 1), when an explanation earns it (it also holds with any one
     example left out);
  2. its network (engine 2), when at least k of the augmented views agree on the same
     answer (k is chosen on calibration puzzles from the practice half, never on the
     held-out ones).

A puzzle counts as right when every test output is among its answers, wrong when it
answered and missed one, and unanswered otherwise. The report compares programs alone,
the network alone and both together on the held-out half.

    python -m ultron net score [--quick]
"""

import multiprocessing as mp

import numpy as np

from . import compose, grow, loop

_SHARED = {}


def _program(job):
    tid, t = job
    attempts, used, _ = compose.predict(t["train"], [i for i, _ in t["test"]],
                                        budget=grow.BUDGET, max_size=grow.MAX_SIZE[0],
                                        loo=True)
    return tid, attempts if used else [[] for _ in t["test"]]


def _init(words, order):
    compose.LIBRARY[0], compose.ORDER[0] = words, order


def programs(tasks, ids, words, order, workers=4):
    """{task: [answers for each test input]} from its programs, answering only when an
    explanation earns it."""
    old = compose.LIBRARY[0], compose.ORDER[0]
    words = list(words) or None
    _init(words, order)
    try:
        jobs = [(t, tasks[t]) for t in ids]
        if workers > 1:
            # fork where there is one; Windows has only spawn, whose workers start fresh and
            # get its language and search order from _init
            method = "fork" if "fork" in mp.get_all_start_methods() else "spawn"
            with mp.get_context(method).Pool(workers, _init, (words, order)) as pool:
                rows = pool.map(_program, jobs, chunksize=1)
        else:
            rows = [_program(j) for j in jobs]
    finally:
        compose.LIBRARY[0], compose.ORDER[0] = old
    return dict(rows)


def combine(prog, votes, tasks, ids, k, use_programs=True, use_net=True):
    """{task: [answers per test input]} from both engines, at most two each."""
    out = {}
    for t in ids:
        answers = []
        for j in range(len(tasks[t]["test"])):
            a = list(prog.get(t, [[]] * (j + 1))[j]) if use_programs else []
            top = votes.get((t, j), []) if use_net else []
            if top and top[0][1] >= k and all(not np.array_equal(top[0][0], b) for b in a):
                a.append(top[0][0])
            answers.append(a[:2])
        out[t] = answers
    return out


def outcomes(answers, tasks):
    """+1 right, -1 wrong, 0 no answer, for each task."""
    out = {}
    for t, per_test in answers.items():
        if not any(per_test):
            out[t] = 0
            continue
        ok = all(any(np.array_equal(a, o) for a in att)
                 for att, (_, o) in zip(per_test, tasks[t]["test"]))
        out[t] = 1 if ok else -1
    return out


def summary(oc):
    right = sum(1 for v in oc.values() if v > 0)
    wrong = sum(1 for v in oc.values() if v < 0)
    answered = right + wrong
    return {"right": right, "wrong": wrong, "net": right - wrong, "tasks": len(oc),
            "precision": right / answered if answered else None}


def score(quick=False, device="cpu", workers=4, path=None):
    """The held-out half judged: programs alone, network alone, both."""
    from .net import train as nettrain
    model, ck = nettrain.load(path or nettrain.CKPT, device)
    tasks, practice, held = loop.halves(quick)
    split = ck["split"]
    calib, held = split["calib"], split["held"]
    state = loop.load() if not quick else {"words": [], "order": None}
    order = dreams_guide(state)
    v = nettrain.votes(model, ck, tasks, calib + held, device)
    k = nettrain.choose_k(tasks, calib, v, len(ck["views"]))
    prog = programs(tasks, held, state["words"], order, workers)
    rows = {}
    for name, up, un in (("programs", True, False), ("network", False, True),
                         ("both", True, True)):
        rows[name] = outcomes(combine(prog, v, tasks, held, k, up, un), tasks)
    gain = loop.interval(rows["both"], rows["programs"])
    return {"k": k, "views": len(ck["views"]), "held_out": len(held),
            "rows": {n: summary(o) for n, o in rows.items()}, "gain_over_programs": gain}


def dreams_guide(state):
    from . import dreams
    return dreams.Guide.from_json(state.get("guide")) or state.get("order") or None
