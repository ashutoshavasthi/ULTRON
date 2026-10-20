"""The scoreboard: is Ultron getting better at learning? (docs/PLAN.md)

One row per run, appended to reports/scoreboard.md:

  * the learning loop, held out: Ultron practises on one half of its ARC experience
    (wake: it writes programs for the tasks; sleep: pieces its programs share become new
    words of its language, arc/compose.py), then meets the other half, never seen,
    with and without the words it grew. What it grew must earn its keep on tasks it never
    practised on: the gain is the number that says whether learning compounds;
  * the main solver on the ARC-AGI-1 training split (official scoring, with precision:
    how many of the answers it gave were right). The evaluation split is not opened here;
    it stays behind the logged `python -m ultron arc --split evaluation`;
  * the lessons: how many of the exams of lessons 0-33 the saved brain still passes.

    python -m ultron score [--quick] [--workers 4] [--skip-lessons]
"""

import datetime
import os
import subprocess
import time

BOARD = os.path.join("reports", "scoreboard.md")
HEADER = ("# The scoreboard\n\n"
          "One row per run of `python -m ultron score` (see [docs/PLAN.md](../docs/PLAN.md)).\n"
          "**Held out**: practise on one half of its ARC experience, then the other half "
          "(never seen) without and with the words it grew; right (wrong) answers. "
          "**Gain**: held-out tasks right with its grown words minus without. **ARC-1 "
          "training**: the main solver, official scoring, with precision (right / answered). "
          "**Lessons**: exams of lessons 0-33 the saved brain still passes.\n\n"
          "| When | Commit | Run | Held out: without | with its words | Gain | Words grown "
          "| ARC-1 training | Lessons |\n"
          "|---|---|---|---|---|---|---|---|---|\n")


def learning_round(quick, workers):
    """One wake-sleep round, practised on half 0 and tested on half 1 (never seen)."""
    from .arc import compose, data, grow
    tasks = data.experience()
    ids = sorted(tasks)
    practice, unseen = ids[0::2], ids[1::2]
    if quick:
        practice, unseen = practice[:60], unseen[:60]
    wake_budget = 50_000 if quick else 200_000
    without = grow.run(tasks, unseen, grow.BUDGET, None, workers)
    wake = grow.run(tasks, practice, wake_budget, None, workers)
    explained = {t: grow._tuple(r["expr"]) for t, r in wake.items() if r["right"]}
    words = compose.learn_library(explained)
    with_words = grow.run(tasks, unseen, grow.BUDGET, words, workers)
    right = lambda rows: len(grow._right(rows))
    wrong = lambda rows: len(grow._wrong(rows))
    return {"unseen": len(unseen), "explained": len(explained), "words": len(words),
            "without": (right(without), wrong(without)),
            "with": (right(with_words), wrong(with_words)),
            "gain": right(with_words) - right(without),
            "word_list": [compose.describe_step(e) for e in words]}


def arc_training(quick, workers):
    from .arc import harness, library, solve
    solve.LIBRARY[0] = library.load() or None
    r = harness.score_set("arc1", "training", limit=40 if quick else None, workers=workers)
    answered = [row for row in r["rows"] if row["found"]]
    right = sum(1 for row in answered if row["score"] == 1)
    return {"tasks": r["tasks"], "percent": r["percent"], "answered": len(answered),
            "right": right}


def lessons(brain_path):
    from .brain.brain import Brain
    from .judge.exams import EXAMS
    brain = Brain.load(brain_path)
    passed, failed = 0, []
    for n, exam in sorted(EXAMS.items()):
        try:
            ok = exam(brain)["passed"]
        except Exception as e:          # a film it can't fetch here, for instance
            ok = False
            failed.append(f"{n} ({type(e).__name__})")
            continue
        passed += ok
        if not ok:
            failed.append(str(n))
    return {"passed": passed, "of": len(EXAMS), "failed": failed}


def run(quick=False, workers=4, skip_lessons=False, brain_path=None):
    started = time.time()
    loop = learning_round(quick, workers)
    arc = arc_training(quick, workers)
    les = None if skip_lessons else lessons(brain_path)
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                            text=True).stdout.strip() or "?"
    when = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
    precision = f"{arc['right']}/{arc['answered']}" if arc["answered"] else "-"
    row = (f"| {when} | `{commit}` | {'quick' if quick else 'full'} "
           f"({loop['unseen']} unseen) | {loop['without'][0]} ({loop['without'][1]}) "
           f"| {loop['with'][0]} ({loop['with'][1]}) | {loop['gain']:+d} | {loop['words']} "
           f"| {arc['percent']:.1f}% of {arc['tasks']} ({precision} right) | "
           + ("skipped" if les is None else
              f"{les['passed']}/{les['of']}"
              + (f" (not: {', '.join(les['failed'])})" if les["failed"] else ""))
           + " |\n")
    os.makedirs("reports", exist_ok=True)
    if not os.path.exists(BOARD):
        with open(BOARD, "w") as f:
            f.write(HEADER)
    with open(BOARD, "a") as f:
        f.write(row)
    return {"loop": loop, "arc": arc, "lessons": les, "row": row,
            "seconds": round(time.time() - started)}
