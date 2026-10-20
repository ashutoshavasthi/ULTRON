"""The scoreboard: is Ultron getting better at learning? (docs/PLAN.md)

One row per run, appended to reports/scoreboard.md:

  * the learning loop, held out: one more round of arc/loop.py. Ultron practises on the
    tasks of its practice half it hasn't explained yet (wake), grows its language again
    from everything it ever explained (sleep), and meets the held-out half, never learned
    from, with and without its words. The gain, and how it changes from round to round,
    says whether learning compounds;
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
          "One row per run of `python -m ultron score` (see [docs/PLAN.md](../docs/PLAN.md)). "
          "Each run is one more round of the learning loop.\n"
          "**Held out**: tasks it never learns from, without and with the words it has grown; "
          "right (wrong) answers. "
          "**Gain**: held-out tasks right with its grown words minus without (and its change "
          "from the last round). **ARC-1 "
          "training**: the main solver, official scoring, with precision (right / answered). "
          "**Lessons**: exams of lessons 0-33 the saved brain still passes.\n\n"
          "| When | Commit | Run | Round | Held out: without | with its words | Gain "
          "| Words | ARC-1 training | Lessons |\n"
          "|---|---|---|---|---|---|---|---|---|---|\n")


def learning_round(quick, workers):
    """One more round of the learning loop (arc/loop.py), on its kept language."""
    from .arc import loop
    path = loop.STATE if not quick else os.path.join("brain", "language_quick.json")
    rows, state = loop.run(rounds=1, quick=quick, workers=workers, state_path=path)
    r = rows[-1]
    return {"round": r["round"], "unseen": r["held_out"], "explained": r["explained"],
            "words": r["words"], "without": tuple(state["without"]),
            "with": (r["right"], r["wrong"]), "gain": r["gain"], "change": r["change"],
            "word_list": r["word_list"]}


def arc_training(quick, workers):
    from .arc import compose, harness, library, loop, solve
    solve.LIBRARY[0] = library.load() or None
    compose.LIBRARY[0] = loop.load_words(loop.STATE if not quick else
                                         os.path.join("brain", "language_quick.json"))
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
           f"({loop['unseen']} held out) | {loop['round']} | {loop['without'][0]} "
           f"({loop['without'][1]}) | {loop['with'][0]} ({loop['with'][1]}) "
           f"| {loop['gain']:+d} ({loop['change']:+d}) | {loop['words']} "
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
