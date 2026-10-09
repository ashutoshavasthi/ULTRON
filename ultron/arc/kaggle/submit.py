"""Make an ARC Prize submission file with Ultron, offline (as Kaggle requires).

    python -m ultron.arc.kaggle.submit CHALLENGES.json submission.json [--workers 4]

CHALLENGES.json is the competition's test challenges file (on Kaggle:
/kaggle/input/arc-prize-20XX/arc-agi_test_challenges.json). The output has the official
format: {task_id: [{"attempt_1": grid, "attempt_2": grid}, ...]}, one entry per test
input, in order. A test input Ultron has no answer for gets a 1x1 grid (an honest
"don't know"; the format requires two attempts).
"""

import argparse
import json
import time

import numpy as np

from .. import library, solve

DONT_KNOW = [[0]]


def _task(job):
    tid, task, budget = job
    train = [(np.array(p["input"], dtype=np.int8), np.array(p["output"], dtype=np.int8))
             for p in task["train"]]
    tests = [np.array(p["input"], dtype=np.int8) for p in task["test"]]
    try:
        attempts, used, _ = solve.predict(train, tests, budget=budget)
    except Exception:           # one bad task must never sink the submission
        attempts, used = [[] for _ in tests], []
    out = []
    for a in attempts:
        a = [x.tolist() for x in a] + [DONT_KNOW, DONT_KNOW]
        out.append({"attempt_1": a[0], "attempt_2": a[1]})
    return tid, out, solve.show(used[0]) if used else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("challenges")
    ap.add_argument("output")
    ap.add_argument("--budget", type=int, default=solve.BUDGET)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-library", action="store_true")
    a = ap.parse_args(argv)
    if not a.no_library:
        solve.LIBRARY[0] = library.load() or None
    with open(a.challenges) as f:
        tasks = json.load(f)
    jobs = [(tid, tasks[tid], a.budget) for tid in sorted(tasks)]
    t0 = time.time()
    if a.workers > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(a.workers) as pool:
            done = pool.map(_task, jobs, chunksize=1)
    else:
        done = [_task(j) for j in jobs]
    sub = {tid: out for tid, out, _ in done}
    with open(a.output, "w") as f:
        json.dump(sub, f)
    found = sum(1 for _, _, p in done if p)
    print(f"{len(sub)} tasks, a program found for {found}, {time.time() - t0:.0f} s; "
          f"written to {a.output}")
    with open(a.output.rsplit(".", 1)[0] + "_programs.json", "w") as f:
        json.dump({tid: p for tid, _, p in done}, f, indent=0)


if __name__ == "__main__":
    main()
