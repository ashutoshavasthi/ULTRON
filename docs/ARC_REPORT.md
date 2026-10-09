# Ultron on ARC-AGI: a small, transparent, self-extending program learner

*Technical report, draft. Every number below is reproduced by the command next to it.*

## Abstract

Ultron is a learner built on one principle: **the shortest description that explains
every observation wins** (minimum description length, MDL). It has no neural language
model, no pretraining and no internet-scale data. It runs on a CPU and gives the same
answer on any machine.

On ARC-AGI it searches for the shortest program, over a frozen set of 38 generic grid
operations, that maps every training input of a task to its output exactly. It answers
with up to two such programs and says nothing when it has none.

New abilities may come only from Ultron itself. Library learning turns pieces that recur
in its own solved programs into building blocks, and keeps a block only when it shortens
the total description of everything solved.

Results so far (official scoring, evaluation split opened only by the logged scoring
command):
- **ARC-AGI-1 evaluation: 7.75%**;
- **ARC-AGI-2 evaluation: 0%**;
- at about 2.4 CPU-seconds per task;
- when Ultron does answer, it is right **31 times out of 33**.

## 1. What is being measured, and how it is kept honest

- **Official rule.** Each test output scores 1 if one of at most two attempts matches it
  exactly. A task scores the fraction of its test outputs matched.
- **The evaluation split is locked.** Development code raises `EvaluationLocked` if it
  asks for it. Only `python -m ultron arc --split evaluation` opens it, and every such
  run is appended to `reports/arc_runs.log` (time, set, score, budget, library size).
  Evaluation is scored only at milestones.
- **Leak-free experience.** ARC-AGI-2's public training set contains 376 of ARC-AGI-1's
  evaluation tasks.
  - Ultron learns only from `data.experience()`: ARC-AGI-1 training (400 tasks) plus
    the 233 ARC-AGI-2 training tasks that appear in no evaluation split.
  - The match is by name, read from the manifest, so no evaluation file is opened.
- **Pinned data.** Both datasets are cloned at pinned commits, and every file is checked
  against a SHA-256 manifest (`ultron/arc/manifest.json`).
- **Deterministic.**
  - The search budget is counted in grid operations (40,000 per task), not seconds.
  - numpy runs single-threaded.
  - Parallel runs solve tasks independently and are tested to give identical answers.

## 2. Method

### 2.1 Perception (5 generic primitives, `grid.py`)

- background;
- things (connected pieces, 4- or 8-connected, single- or multi-colour);
- a thing's box, size and colours;
- separator lines;
- halves.

### 2.2 Operations: frozen at 38 (`ops.py`, `PRIMITIVES.md`)

Each operation is generic (symmetries, cropping to a thing chosen by a property, scaling,
tiling, recolouring, filling enclosed areas, gravity, outlines, symmetry completion,
panel logic, pattern completion, rays, counting...). Each has a one-line justification
in a counted list.

A test enforces the freeze: `tests/test_arc.py::test_hand_written_operations_are_frozen`.

### 2.3 Learned per task, from the task's own examples

- **A colour mapping:** one consistent recolouring.
- **A local law** (`cells.py`): a cell's new colour as a table over the smallest set of
  features (its colour, its neighbours, the size of its thing, ...) that agrees with
  every example. A test situation never seen in the examples gives *no answer*, not a
  guess.

### 2.4 Search

Programs are chains of operations, enumerated shortest first. The search:
- drops programs that do the same thing to every example (observational equivalence);
- caches each operation's result;
- keeps a program only if it reproduces **every** training output.

Programs are ranked by description length: 1 per operation, plus what a learned table
must spell out. The two shortest different answers are submitted.

### 2.5 Library learning (`library.py`): Ultron grows its own operations

From the programs Ultron found for tasks in its experience, it collects every piece of
2–4 steps. Each piece also gets abstracted variants:
- one colour left open (chosen per task);
- one inner step left open ("turn, *do something*, turn back").

A piece becomes a block only if

    uses × (steps saved per use) > cost of writing the block down

that is, only if it shortens the total description of everything solved. The search
then tries each block as a single step, so programs too long to reach become short.

### 2.6 Intuition (`guide.py`), a null result

Ultron counted which operations helped under which task features (output smaller,
colours added, panels, ...) and tried promising operations first. Cross-validated on
the training split, it changed nothing (20.5% → 20.5%, 23.5% → 23.5%). It is off by
default and reported as a null result.

## 3. Results

| Milestone | Set | Split | Score | Logged |
|---|---|---|---|---|
| A0 (first engine) | ARC-AGI-1 | evaluation (400) | 3.75% | yes |
| A0 | ARC-AGI-2 | evaluation (120) | 0% | yes |
| **A1 (operations frozen)** | ARC-AGI-1 | evaluation (400) | **7.75%** | yes |
| A1 | ARC-AGI-2 | evaluation (120) | 0% | yes |
| | ARC-AGI-1 | training (400) | 22.8% (24.1% at 10× budget) | dev split |

Reproduce: `python -m ultron arc --split evaluation --sets arc1 arc2 --workers 4`.

**Cost.**
- 2.4 s per task on average (max 15 s) on one CPU core.
- The whole ARC-AGI-1 evaluation takes 4 minutes on 4 cores.
- No GPU, no network.

**It knows when it doesn't know.** On the evaluation split Ultron found a program for 33
tasks and was right on 31. On the other 367 it gave no answer rather than a guess.

**Transparency.** Every answer comes with its program in words, for example
`crop_content ▸ upscale(2)`, or `fill_enclosed(2) ▸ recolour 0→3`. Lists for every task
are in `reports/arc_evaluation.md` and `reports/arc_training.md`.

## 4. Does Ultron's own learning help? (the learning curve)

*In progress: `python -m ultron.arc.curve` (cross-validated: practise on one half of the
experience, learn blocks, test on the unseen half with and without them; two rounds so
learning can compound).*

**First finding.** On ARC-AGI-1 training alone, even at 10× budget, Ultron's 96 solutions
contain no piece that recurs often enough to pay for itself. Almost all are single
operations with a learned recolouring or local law. MDL therefore learns **no** blocks.
We report this rather than lower the bar.

## 5. Limits, stated plainly

- Most ARC tasks need a concept that no short chain of the 38 operations expresses.
  Ultron then says nothing. That accounts for most of the 92% it misses on ARC-AGI-1
  evaluation.
- ARC-AGI-2 is designed against exactly this kind of search, and Ultron scores 0% there.
- The perception and operations were written by a person (counted and frozen). The
  claim is not "no prior knowledge", but "a small, counted, generic prior, plus learning
  that must pay for itself".

## 6. Reproducing everything

```
python -m ultron arc --split training --workers 4      # development split
python -m ultron arc --split evaluation --sets arc1 arc2 --workers 4   # logged
python -m ultron.arc.curve --rounds 2 --workers 4      # learning curve
python -m ultron.arc.kaggle.check                       # Kaggle package, end to end
python -m pytest -q tests/test_arc.py
```
