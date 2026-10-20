# ULTRON: notes for anyone working on it (including Claude)

## What and why
A learner that writes programs in **a language it builds itself**, to explain what it sees
from a few examples. There is no pretrained model and no language model.

The goal is general intelligence that improves itself, then goes beyond human. The first
checkpoint is human level on ARC-AGI. The whole plan is one page:
[docs/PLAN.md](docs/PLAN.md). Keep it that way: simple, and judged by the scoreboard.

## The loop
1. Solve: the shortest program that explains each task.
2. Grow the language: recurring pieces become new words.
3. Learn to write: intuition trained on its own searches.
4. Climb: harder tasks.

## Rules
- No pretrained model and no language model inside Ultron.
- Measure on tasks it has never seen. The ARC evaluation split is opened only by the
  logged `python -m ultron arc --split evaluation`, rarely.
- Self-changes are sandboxed, kept only if held-out scores rise with nothing broken, and
  approved by the owner. Ultron never edits its own tests.
- Report failures as plainly as successes.

## Commands
- `python -m ultron score [--quick]`: the scoreboard (`reports/scoreboard.md`). It covers the
  held-out learning round, ARC-AGI-1 training and the lessons.
- `python -m ultron arc`: score ARC-AGI (training by default).
- `python -m ultron train`: retrain lessons 0–33 (about 20 minutes, byte-identical).
  Lesson 30 needs a Wikimedia film that some environments can't fetch.
- `python -m pytest`: the tests. `python -m ultron stress`: the failure lab.

## Layout
- `ultron/arc`: the ARC learner (solve, compose, grow, library, intuition).
- `ultron/brain`: the explanation engine.
- `ultron/senses`, `ultron/env`, `ultron/trainer`: the lesson worlds.
- `ultron/judge`: exams and the failure lab.
- `ultron/score.py`: the scoreboard.
- `docs/history/`: earlier plans, kept as a record.

## Branches
- `claude/integrate-stages-5hnowy` (PR #12): earlier work combined.
- `claude/dreamy-darwin-neiflp` (draft PR #13): this plan.
- `claude/stage-coding-engc-1j7rdc`: Ultron reading code (Engc, Python, its own functions).
- `park/room`: the simulated room, parked.
