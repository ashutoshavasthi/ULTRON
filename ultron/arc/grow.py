"""Does Ultron grow steps of its own from small ones, and do they help on unseen puzzles?

Cross-validated wake-sleep on the small-steps language (compose.py). Ultron's experience
(data.experience()) is split into two halves. Each round, on one half:

  * wake: it searches every task with the steps it has (a longer search than usual) and
    keeps the shortest program that explains each one exactly;
  * sleep: pieces those programs share become steps of its own when they shorten the
    description of everything it explained (compose.learn_library).

It is then tested on the other half, never seen, at the normal budget, with and without
the steps it grew. Then the halves swap. In round k the wake uses round k-1's steps, so
growth can compound: a step built from steps reaches programs too long to find before.

    python -m ultron.arc.grow [--rounds 3] [--wake 200000] [--workers 4]
"""

import argparse
import json
import multiprocessing as mp
import os

import numpy as np

from . import compose, data

BUDGET = 40_000
PATH = os.path.join(os.path.dirname(__file__), "..", "..", "brain", "arc_steps.json")


def _plain(e):
    return [_plain(a) if isinstance(a, tuple) else a for a in e]


def _tuple(e):
    return tuple(_tuple(a) if isinstance(a, list) else a for a in e)


def to_json(library):
    return [dict(e, pattern=_plain(e["pattern"])) for e in library]


def from_json(rows):
    return [dict(e, pattern=_tuple(e["pattern"])) for e in rows]


def save(library, path=PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({"steps": to_json(library)}, f, indent=1)
        f.write("\n")


def load(path=PATH):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return from_json(json.load(f)["steps"])


def _init(library):
    compose.LIBRARY[0] = library or None


MAX_SIZE = [12]


def _one(job):
    tid, t, budget = job
    attempts, used, spent = compose.predict(t["train"], [i for i, _ in t["test"]],
                                            budget=budget, max_size=MAX_SIZE[0])
    if not used:
        return tid, None
    right = all(any(np.array_equal(p, o) for p in att)
                for att, (_, o) in zip(attempts, t["test"]))
    return tid, {"right": bool(right), "program": compose.show(used[0]),
                 "expr": _plain(used[0]), "size": compose.size(used[0])}


def run(tasks, ids, budget, library, workers):
    """{task: answer} for the tasks where some program explained every example."""
    jobs = [(tid, tasks[tid], budget) for tid in ids]
    if workers > 1:
        with mp.get_context("fork").Pool(workers, _init, (library,)) as pool:
            rows = pool.map(_one, jobs, chunksize=1)
    else:
        _init(library)
        try:
            rows = [_one(j) for j in jobs]
        finally:
            _init(None)
    return {t: r for t, r in rows if r is not None}


def _right(rows):
    return {t for t, r in rows.items() if r["right"]}


def _wrong(rows):
    return {t for t, r in rows.items() if not r["right"]}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--wake", type=int, default=200_000)
    ap.add_argument("--budget", type=int, default=BUDGET)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-size", type=int, default=12)
    ap.add_argument("--out", default="arc_grow.json")
    ap.add_argument("--state", default=None,
                    help="save progress here after each half, and continue from it")
    ap.add_argument("--halves", type=int, default=0,
                    help="stop after this many practice halves (0: run to the end)")
    a = ap.parse_args(argv)
    MAX_SIZE[0] = a.max_size
    tasks = data.experience()
    ids = sorted(tasks)
    halves = [ids[0::2], ids[1::2]]
    state = None
    if a.state and os.path.exists(a.state):
        with open(a.state) as fh:
            state = json.load(fh)
    if state:
        base, rows = state["base"], state["rows"]
        grown = [from_json(g) for g in state["grown"]]
        done = {(r["round"], r["practice_half"]) for r in rows}
    else:
        base = [run(tasks, h, a.budget, None, a.workers) for h in halves]
        grown, rows, done = [[], []], [], set()
    ran = 0
    for k in range(1, a.rounds + 1):
        for f in (0, 1):
            if (k, f) in done:
                continue
            if a.halves and ran >= a.halves:
                return
            ran += 1
            practice, unseen = halves[f], halves[1 - f]
            wake = run(tasks, practice, a.wake, grown[f], a.workers)
            explained = {t: compose.inline(_tuple(r["expr"]), grown[f])
                         for t, r in wake.items() if r["right"]}
            # what it grew is relearned from everything explained so far (a step that
            # stops paying is dropped)
            grown[f] = compose.learn_library(explained)
            test = run(tasks, unseen, a.budget, grown[f], a.workers)
            b0 = base[1 - f]
            row = {"round": k, "practice_half": f, "practised": len(practice),
                   "explained_in_practice": len(explained), "steps": len(grown[f]),
                   "step_list": [compose.describe_step(e) for e in grown[f]],
                   "unseen": len(unseen),
                   "without": {"right": len(_right(b0)), "wrong": len(_wrong(b0))},
                   "with": {"right": len(_right(test)), "wrong": len(_wrong(test))},
                   "gained": sorted(_right(test) - _right(b0)),
                   "lost": sorted(_right(b0) - _right(test))}
            rows.append(row)
            print(f"round {k}, practise on half {f}: explained {len(explained)}, grew "
                  f"{len(grown[f])} steps; unseen half: {row['without']['right']} right "
                  f"({row['without']['wrong']} wrong) without, {row['with']['right']} right "
                  f"({row['with']['wrong']} wrong) with; gained {row['gained']}, lost "
                  f"{row['lost']}", flush=True)
            os.makedirs("reports", exist_ok=True)
            with open(os.path.join("reports", a.out), "w") as fh:
                json.dump(rows, fh, indent=1)
                fh.write("\n")
            if a.state:
                with open(a.state, "w") as fh:
                    json.dump({"base": base, "rows": rows,
                               "grown": [to_json(g) for g in grown]}, fh)


if __name__ == "__main__":
    main()
