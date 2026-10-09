"""Scoring Ultron on ARC-AGI with the official rule, and writing the report.

Official scoring: each test output is scored 1 if one of (at most) two attempts matches
it exactly; a task's score is the fraction of its test outputs scored; the total is the
sum over tasks divided by the number of tasks.
"""

import datetime
import json
import os
import time

import numpy as np

from . import data, solve

LOG = os.path.join(data.ROOT, "reports", "arc_runs.log")


def score_set(name, split, limit=None, budget=solve.BUDGET, scoring=False, ids=None,
              tasks=None):
    tasks = tasks or data.load(name, split, i_am_scoring=scoring)
    ids = ids or (sorted(tasks)[:limit] if limit else sorted(tasks))
    rows, total, started = [], 0.0, time.time()
    for tid in ids:
        t = tasks[tid]
        t0 = time.time()
        attempts, used, spent = solve.predict(t["train"], [i for i, _ in t["test"]],
                                              budget=budget)
        ok = [o is not None and any(np.array_equal(a, o) for a in att)
              for att, (_, o) in zip(attempts, t["test"])]
        s = sum(ok) / len(ok)
        total += s
        rows.append({"task": tid, "score": s, "program": solve.show(used[0]) if used else None,
                     "ops": [n for n, _ in used[0]] if used else [],
                     "found": bool(used), "operations": spent,
                     "seconds": round(time.time() - t0, 2)})
    result = {"set": data.SETS[name], "split": split, "tasks": len(ids), "score": total,
              "percent": 100 * total / len(ids), "seconds": round(time.time() - started, 1),
              "budget": budget, "rows": rows}
    if split == "evaluation":
        _log(result)
    return result


def _log(result):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps({"when": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"), "set": result["set"], "split": result["split"],
            "tasks": result["tasks"], "percent": round(result["percent"], 2),
            "budget": result["budget"]}) + "\n")


def report(results):
    lines = ["# Ultron on ARC-AGI", "",
             "Official scoring (2 attempts per test output). Development uses the training "
             "split only; every evaluation run is logged in `reports/arc_runs.log`.", "",
             "| Set | Split | Tasks | Score | Seconds | Budget (operations per task) |",
             "|---|---|---|---|---|---|"]
    for r in results:
        lines.append(f"| {r['set']} | {r['split']} | {r['tasks']} | **{r['percent']:.1f}%** "
                     f"({r['score']:.1f}) | {r['seconds']} | {r['budget']} |")
    for r in results:
        solved = [x for x in r["rows"] if x["score"] > 0]
        wrong = [x for x in r["rows"] if x["found"] and x["score"] == 0]
        lines += ["", f"## {r['set']} {r['split']}: what it found", "",
                  f"{len(solved)} tasks solved; {len(wrong)} where a program fitted every "
                  f"example but gave the wrong answer on the test (wrong generalisation); "
                  f"{r['tasks'] - len(solved) - len(wrong)} with no program within budget.", "",
                  "| Task | Program Ultron found |", "|---|---|"]
        for x in solved:
            lines.append(f"| {x['task']} | `{x['program']}` |")
    return "\n".join(lines) + "\n"


def learn_guide(result, tasks):
    """Intuition from solved training tasks: their features and the operations used."""
    from . import guide
    solved = [(guide.task_features(tasks[r["task"]]["train"]), r["ops"])
              for r in result["rows"] if r["score"] > 0 and r["ops"]]
    return guide.learn(solved)
