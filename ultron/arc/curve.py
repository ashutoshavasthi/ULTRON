"""Does what Ultron grows itself make unseen puzzles easier? (cross-validated wake-sleep)

Ultron's experience (data.experience(): ARC-AGI-1 training plus the ARC-AGI-2 training
tasks in no evaluation split) is split into two halves. Each round, on one half:

  * wake: it searches every task (with what it has grown so far) and keeps the
    shortest description it finds: an exact explanation, or a program with the cells it
    gets wrong when that is shorter than describing the answer outright
    (descriptions.py);
  * sleep, abstraction: pieces that recur across those descriptions become its own
    building blocks, when they shorten the description of everything (library.py);
  * sleep, dreams: it learns again which half-built programs look promising, from its
    own searches and from dreams made with its blocks (intuition.py).

It is then tested on the other half, which it has never seen, at the normal budget:
with nothing it grew, with its blocks, and with its blocks and intuition (searched best
first). Then the halves swap. In round k the wake uses what round k-1 grew, so learning
can compound.

    python -m ultron.arc.curve [--rounds 2] [--wake 40000] [--workers 4]
"""

import argparse
import json
import os

from . import data, descriptions, harness, intuition, library, solve


def _solved(result):
    return {r["task"]: r["steps"] for r in result["rows"] if r["score"] == 1.0}


def _wrong(result):
    return sorted(r["task"] for r in result["rows"] if r["found"] and r["score"] == 0)


def _score(tasks, ids, budget, blocks, intu, workers):
    solve.LIBRARY[0] = blocks or None
    solve.INTUITION[0] = intu
    try:
        return harness.score_set("arc1", "training", tasks=tasks, ids=ids, budget=budget,
                                 workers=workers)
    finally:
        solve.LIBRARY[0] = None
        solve.INTUITION[0] = None


def _describe_one(job):
    tid, train, budget = job
    d = descriptions.best(train, budget=budget)
    if d is None:
        return tid, None
    saving, program, wrong = d
    return tid, {"steps": harness.steps(program), "wrong": wrong,
                 "saving": round(saving, 1)}


def wake(tasks, ids, budget, blocks, intu, workers):
    """The shortest description Ultron finds for each task: {task: {steps, wrong}}."""
    solve.LIBRARY[0] = blocks or None
    solve.INTUITION[0] = intu
    jobs = [(tid, tasks[tid]["train"], budget) for tid in ids]
    try:
        if workers > 1:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(workers, harness._init,
                                             (solve.LIBRARY[0], None, intu)) as pool:
                rows = pool.map(_describe_one, jobs, chunksize=1)
        else:
            rows = [_describe_one(j) for j in jobs]
    finally:
        solve.LIBRARY[0] = None
        solve.INTUITION[0] = None
    return {tid: d for tid, d in rows if d is not None}


def sleep(described, tasks, practice, workers, dreams=True):
    """Blocks from the descriptions; then intuition learned with those blocks."""
    blocks = library.learn({t: d["steps"] for t, d in described.items()})
    intu = None
    if dreams:
        solve.LIBRARY[0] = blocks or None
        try:
            intu = intuition.learn({t: tasks[t] for t in practice}, workers=workers)
        finally:
            solve.LIBRARY[0] = None
    return blocks, intu


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--wake", type=int, default=solve.BUDGET)
    ap.add_argument("--budget", type=int, default=solve.BUDGET)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-dreams", action="store_true")
    a = ap.parse_args(argv)
    tasks = data.experience()
    ids = sorted(tasks)
    halves = [ids[0::2], ids[1::2]]
    rows = []
    base = [_score(tasks, h, a.budget, None, None, a.workers) for h in halves]
    grown = [(None, None), (None, None)]
    for k in range(1, a.rounds + 1):
        for f in (0, 1):
            practice, unseen = halves[f], halves[1 - f]
            blocks, intu = grown[f]
            described = wake(tasks, practice, a.wake, blocks, intu, a.workers)
            blocks, intu = sleep(described, tasks, practice, a.workers,
                                 dreams=not a.no_dreams)
            grown[f] = (blocks, intu)
            b0 = base[1 - f]
            with_blocks = _score(tasks, unseen, a.budget, blocks, None, a.workers)
            tests = {"without": b0, "with blocks": with_blocks}
            if intu is not None:
                tests["with blocks and intuition"] = _score(tasks, unseen, a.budget, blocks, intu,
                                                   a.workers)
            row = {"round": k, "practice_half": f, "practised": len(practice),
                   "described": len(described),
                   "exact": sum(1 for d in described.values() if d["wrong"] == 0),
                   "blocks": len(blocks), "block_list": [library.describe(b) for b in blocks],
                   "unseen": len(unseen)}
            for name, r in tests.items():
                row[name] = {"percent": round(r["percent"], 2), "wrong": len(_wrong(r)),
                             "gained": sorted(set(_solved(r)) - set(_solved(b0))),
                             "lost": sorted(set(_solved(b0)) - set(_solved(r)))}
            rows.append(row)
            print(f"round {k}, practise on half {f}: described {row['described']} "
                  f"({row['exact']} exactly), grew {row['blocks']} blocks; unseen half: "
                  + ", ".join(f"{n} {v['percent']}% ({v['wrong']} wrong, +{len(v['gained'])}"
                              f" -{len(v['lost'])})" for n, v in row.items()
                              if isinstance(v, dict)), flush=True)
            os.makedirs("reports", exist_ok=True)
            with open(os.path.join("reports", "arc_learning_curve.json"), "w") as fh:
                json.dump(rows, fh, indent=1)
                fh.write("\n")


if __name__ == "__main__":
    main()
