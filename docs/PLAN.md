# Ultron: the plan, on one page

## What
A learner that writes programs in **a language it builds itself**, to explain what it sees
from a few examples. There is no pretrained model and no language model: everything it
knows, it found.

## Goal
General intelligence that improves itself, and then goes beyond human. The first
checkpoint is human level on ARC-AGI, the public test of learning a rule from a few
examples. Nobody can promise the end goal. The scoreboard says, every round, whether we
are getting closer.

## How: one loop, repeated
1. **Solve.** Write the shortest program, in its own language, that explains each task.
2. **Grow the language.** Pieces that recur in its solutions become new words of the
   language.
3. **Learn to write.** Train its intuition on its own searches, so it writes good programs
   faster.
4. **Climb.** Move on to harder tasks with a bigger language.

"Growing from a child" means this loop climbing from easy tasks to hard ones with a
growing language.

## Self-improvement, in three steps
| Step | What | Where it stands |
|---|---|---|
| 1 | It grows its own language | Exists: `arc/compose.py`, `arc/grow.py`, `arc/library.py` |
| 2 | It improves how it searches | Exists, weakly: `arc/intuition.py` (cut search 3.9×, moved no score yet) |
| 3 | It reads and rewrites its own code | Begun on branch `claude/stage-coding-engc-1j7rdc`: it reads Engc and Python, and its own functions |

Every self-change is tried in a sandbox, kept only if held-out scores rise with nothing
broken, and approved by the owner. Ultron can never edit its own tests. A system that
edits itself will "improve" by gaming its tests unless the tests are out of its reach.

## Scoreboard
`python -m ultron score` adds one row to [`reports/scoreboard.md`](../reports/scoreboard.md):
- **held out:** after practising on one half of its ARC experience, how many tasks of the
  other half (never seen) it gets right without and with the words it grew. The
  **gain** says whether learning compounds;
- **ARC-AGI-1 training:** the main solver, official scoring, with precision;
- **lessons:** how many of the exams of lessons 0–33 still pass;
- **ARC-AGI-1 evaluation,** the official number: only at milestones, through the logged
  `python -m ultron arc --split evaluation`. Last logged: 12.75%.

## Rules (only these)
- No pretrained model and no language model.
- Measure on tasks it has never seen. Open the evaluation split rarely, and log every run.
- Self-changes are sandboxed, scored and approved.
- Report failures as plainly as successes.

## Next
1. **Make the loop compound.** Put the words it grew into the main solver; train its
   intuition on its own language; run rounds; watch the held-out number and the gain per
   round.
2. **Bring in the Code stage** from its branch, so Ultron can read its own code.
3. **The first sandboxed self-change:** it proposes changes to its own search. Each is kept
   only if the scoreboard improves, with the owner's approval.

## Where things are
- [ARCHITECTURE.md](ARCHITECTURE.md): how the code works.
- [ARC_REPORT.md](ARC_REPORT.md): the technical report on ARC-AGI.
- [history/](history/): earlier plans, kept as a record. The 2026-10 detours (simulating a
  child, capability levels with gates) are there too. The simulated room is parked on
  branch `park/room`.
