# ULTRON: notes for anyone working on it (including Claude)

## What and why
A learner that writes programs in **a language it builds itself**, to explain what it sees
from a few examples. There is no pretrained model and no language model.

The goal is general intelligence that improves itself, then goes beyond human. The next
thing to prove is that its language gains words that say something new (learned words,
[docs/MECHANISM.md](docs/MECHANISM.md)). The whole plan is one page:
[docs/PLAN.md](docs/PLAN.md). Keep it that way: simple, and judged by the scoreboard.

## The loop
1. Solve: the shortest program that explains each task.
2. Grow the language: unexplained puzzles give meaning to learned words; a word is kept
   only if several puzzles share it and it passes an example it never trained on.
3. Count what is new: a learned word no hand-written program imitates is a new primitive.
4. Climb: harder tasks.

## Rules
- No pretrained model and no language model inside Ultron.
- Learned words never enter the frozen list of 38 hand-written operations.
- Measure on tasks it has never seen. The ARC evaluation split is opened only by the
  logged `python -m ultron arc --split evaluation`, rarely.
- Self-changes are sandboxed, kept only if held-out scores rise with nothing broken, and
  approved by the owner. Ultron never edits its own tests.
- Report failures as plainly as successes.

## Commands
- `python -m ultron score [--quick]`: the scoreboard (`reports/scoreboard.md`). It covers the
  held-out learning round, ARC-AGI-1 training and the lessons.
- `python -m ultron learn [--quick]`: rounds of the learning loop (its language, dreams, guide;
  curve in `reports/learning_curve.md`).
- `python -m ultron words teach|g0 [--quick]`: learned words. `teach` trains the interpreter
  on the hand-written words (about two hours on four CPU cores); `g0` runs the first gate and
  writes `reports/words_g0.md`.
- `python -m ultron net train|score [--quick] [--device cuda]`: the old engine 2 (M2, no
  longer the main line; see docs/history/PLAN_M1_M2.md).
- `python -m ultron arc`: score ARC-AGI (training by default).
- `python -m ultron train`: retrain lessons 0–33 (about 20 minutes, byte-identical).
  Lesson 30 needs a Wikimedia film that some environments can't fetch.
- `python -m pytest`: the tests. `python -m ultron stress`: the failure lab.

## Layout
- `ultron/words`: learned words (interpreter, free words, search, the G0 gate).
- `ultron/arc`: the ARC learner with hand-written words (solve, compose, grow, library).
- `ultron/brain`: the explanation engine.
- `ultron/senses`, `ultron/env`, `ultron/trainer`: the lesson worlds.
- `ultron/judge`: exams and the failure lab.
- `ultron/score.py`: the scoreboard.
- `docs/history/`: earlier plans, kept as a record.

## Branches
- `claude/integrate-stages-5hnowy` (PR #12): earlier work combined.
- `ultron-final`: this plan (learned words).
- `claude/dreamy-darwin-neiflp` (draft PR #13): the plan before it (M1 and M2).
- `claude/stage-coding-engc-1j7rdc`: Ultron reading code (Engc, Python, its own functions).
- `park/room`: the simulated room, parked.
