# Stage 1: the scalable, unbreakable core

**Mission:** make Ultron's core (the explanation engine, its intuition and its library)
strong enough to carry everything that comes after. It must survive bad data, scale past
the exponential wall, express the shapes real laws take, and prove itself on a public
battlefield: **ARC-AGI**, the benchmark built to measure learning from a few examples.

Everything above this stage (real video, reading the internet, language, a body, code)
stands on this core. If the core is fragile or can't scale, the rest falls.

## Where we stand (measured by the failure lab)

| Mechanism | Breakpoint today |
|---|---|
| Program search, size | Finds laws up to about 7 pieces (a³+b²: 916,000 candidates, 59 s); fails at (a+1)(b+2)(a+b) |
| Program search, wrong records | Exact search failed at 5% wrong records → ✅ **fixed** (laws with exceptions): keeps its law and names each mis-recorded experience |
| Hidden causes, pure noise | ✅ refuses to claim a law |
| Few examples | ✅ two examples are enough for a·b+a |
| Search time vs data | ✅ 20 → 400 examples: 6 s → 18 s |
| Measurement laws under bell-curve noise | Lost at ±0.5% → ✅ **fixed** (robust acceptance): found at ±20% |
| Measurement laws with outliers | Lost at any level → ✅ **fixed**: found with 20% bad readings |
| Irrelevant measurements | Was 312 s for 6 irrelevant → ✅ **fixed**: 10 irrelevant in 0.04 s (valid candidates built directly, same order) |
| Confounders | ✅ **fixed**: a law must involve its outcome; equally short rivals are reported ("what I've seen can't tell them apart") |
| Tiny and huge numbers | ✅ 10⁻¹² to 10¹² |
| A changing world | ✅ **fixed**: after 3 failures that agree with each other, it re-measures (believes 80) and keeps the old value as history |
| Shapes of law | ✅ settling, straight lines, quadratic, and now **oscillation, damped oscillation, logistic growth and t^1.5**, each predicted for a new object (E1) |
| Eyes | ✅ 25/25 at the noise it grew up with; ❌ double noise, faint and touching things. Two redesigns tried (dilated 8- and 16-channel networks with contrast adaptation): big things 25/25 and faint 16/25, but the original trays dropped to 37/40, so they weren't adopted. **Moved to Stage 2**, where the eyes meet real footage |

**Also measured:** with laws with exceptions, wrong records are survived up to **20%**, and the
false-law audit found **0 false laws in 100** datasets with nothing to find.

**A0, the first ARC-AGI numbers** (official scoring; evaluation runs logged in
`reports/arc_runs.log`):

| Set | Split | Score |
|---|---|---|
| ARC-AGI-1 | training (400) | **11.0%** |
| ARC-AGI-1 | evaluation (400) | **3.75%** |
| ARC-AGI-2 | evaluation (120) | **0%** |

Step 1e has begun on training failures: local laws (`cells.py`), pattern completion, rays,
and description-length ranking (which fixed an overfit) take the first 100 training tasks
from 11% to 17%.

**Checkpoints** (every evaluation run is in `reports/arc_runs.log`; the exit criteria
A0–A3 are below):

| Checkpoint | What changed | ARC-AGI-1 training | ARC-AGI-1 evaluation | ARC-AGI-2 evaluation |
|---|---|---|---|---|
| C0 | First engine (criterion **A0** met) | 11.0% | 3.75% | 0% |
| C1 | Hand-written operations **frozen at 38**; local laws, pattern ops | 22.8% | **7.75%** (right 31 of 33 answered) | 0% |
| C2 | Ultron's law-finding applied to things: thing laws, marks and rays, which thing is the answer, how things move | 28.2% | **10.0%** (right 40 of 52 answered) | 0% |
| C3 | Symmetry laws (about the picture's own centre, repairing what is missing); the box where a colour is (chosen by a trait); search speedups | 30.8% | **11.75%** (right 47 of 59 answered) | **0.83%** (1 of 120: the first ARC-AGI-2 task solved) |
| C4 | Copies of a template; lines between things; summaries (a colour, a count, one cell per block) | 33.6% | **12.75%** (right 51 of 63 answered) | 0.83% |

**The ARC push: what it found (measured on training, then the stop rule).**
- **Adopted laws** (each measured right or wrong on the unsolved training tasks first):
  - copies of a template (+2);
  - lines between things (+2);
  - summaries: a colour, a count, one cell per block (+8);
  - arrangements of copies (+4).

  Training went 30.8% → 34.6% with nothing lost, and evaluation 11.75% → 12.75% (C4).
- **Tried and reverted, or not adopted:**

  | Idea | Result |
  |---|---|
  | moves after a depth-1 operation | +1 task at 3× the run time |
  | pick then recolour | +0 |
  | "its twin's colour" as a thing-law outcome | +0 |
  | periodic completion | +0 |
  | choosing a panel by a law | no candidate task |
  | 3× search budget | +2 tasks at 2.9× the time |
  | a per-puzzle network (numpy, trained only on the puzzle, must predict each held-out example exactly before it may answer) | 0 right, 1 wrong, 184 silent of 185 |
- **The stop rule triggered:** three families in a row each added fewer than 2 tasks. Hand-picked law families have reached diminishing returns.
- **Training gains reach evaluation at about one third** (+2.8 training points gave +1.0 evaluation). A2 (≥ 25%) and A3 (≥ 40%) are therefore not reachable by more families of this kind. What they need is a mechanism that *generates* hypotheses rather than enumerating them: a far more accurate learned intuition (S2), or per-puzzle networks at CompressARC scale, which need GPU-length training this environment does not have.

**The learned intuition for ARC** (`arc/intuition.py`). It looks at what a half-built program has made against the target: shape, cells right, colours, number of things, closer than before. It learns from Ultron's own searches and from dreams (chains of its operations on real pictures). Measured on held-out halves of the training split:

| Measure | Result |
|---|---|
| Rank of the step that leads to an explanation | median **1** of about 200 (default order: 29); on real multi-step solutions **3.5** (default: 35) |
| Search effort to the first explanation | **3.9× less** in total, median **5.3×** per task (46× and 42× on two real tasks), on 76 held-out tasks |
| Score | **unchanged** (cross-validated: +1 and −3 tasks), so it is not used by default |

**The finding:** search order is not what limits Ultron on ARC. Most unsolved tasks have no explanation within two or three of the 38 frozen operations at all, which is also why 3× and 10× budgets add only 0.5–1.3 points. S2's effort criterion reaches 3.9×, not 10×. The rest is capped by breadth-first search building every one-step program first; a best-first search across depths would lift that cap.

C2 meets criterion **A1** (≥ 10%).

**Library learning: an honest null result so far.** Ultron's solved programs are almost
all one operation plus a learned law. No piece recurs often enough to pay for itself
under MDL, even at 10× search budget and with blocks that leave a colour or a whole step
open. So **no blocks are learned**, and the cross-validated learning curve is flat
(15.19% → 15.19% on the unseen half). We do not lower the bar to manufacture blocks.

**Letting Ultron grow its own operations (wake–sleep, measured; not adopted).** Three
changes gave library learning more to learn from, each true to the core:
- **descriptions with exceptions** (`arc/descriptions.py`): a program plus the cells it
  gets wrong counts as a description of a task when it is shorter, in bits, than
  describing the answers outright. Ultron learns from these, never answers with them;
- **richer blocks** (`arc/library.py`): any parameter may be left open, and a block may
  end "then learn a law of this kind on the result";
- **deeper search** (`arc/solve.py`): such law tails are learned at any depth, and with
  intuition on the search grows the most promising program of any length (best first
  across depths). The default search is unchanged.

| Measure (training experience, 633 tasks) | Result |
|---|---|
| Tasks with a description shorter than the answer | 412: 212 exact, 200 with exceptions |
| Length of those descriptions | 1 step: 249; 2 steps: 157; 3 steps: 1 |
| Blocks that pay (all 633 tasks) | from exact solutions only: 6; adding descriptions with exceptions: **8** |
| Blocks that pay (one half, 316 tasks) | **2** in each half |
| Unseen half, with blocks (cross-validated) | half 0: 23.26% → 22.94% (+0, −1 task, +1 wrong); half 1: 22.4% → 22.4% (+0, −0) |
| Unseen half, blocks and intuition, best first | half 0: 22.94% (+1, −2); half 1: 22.08% (+0, −1, +1 wrong) |

Gate B (≥ 3 more tasks on each unseen half, none lost) failed in both halves, so by the
stop rule round 2 was not run and nothing is switched on. **The finding:** the 38 frozen
operations are too coarse for library learning. Each task is described by one or two
big operations, so few pieces are shared, and most shared pieces ("an operation, then a
cells law") repeat what the search already does after one step. Extra blocks also cost
budget: the one task lost (e3497940) was crowded out. For Ultron to grow its own
operations on ARC, its base language must be **finer-grained**: small, composable steps
whose solutions are long and share structure, as in the brain, where the same rule
gave S1. That is the next move, not more hand-written families.

**Small composable steps (`arc/compose.py`, `arc/grow.py`; measured).** A typed language
of 27 small steps over pictures, things, numbers and colours. A step on things acts on
each one ("for each"), keeping some is a filter ("where"), so "small things turn green"
is `paint(x, recolour(with(things(x), size, 1), 3))`. Search is bottom up, smallest
first, one program per behaviour, within the same 40k budget; a new set of things is
also checked as a finished answer, and a new picture with one learned recolouring.

| Gate | Result |
|---|---|
| 1. Expressiveness | **18 of the 38** frozen operations are short programs of small steps, identical on every training picture. The other 20 (filling enclosed areas, gravity, symmetry, rays, lines, pattern continuation, ...) need loops or per-cell reasoning the language doesn't have |
| 2. Search (training, 40k) | 34 right, 4 wrong on its own; as a fallback when the big operations explain nothing: **+3 right, +1 wrong** (138 → 141). On the 233 held-out ARC-AGI-2 training tasks: +0, −0 |
| 3. Growing its own steps (cross-validated, 3 rounds) | unseen half **18 → 19** and **17 → 19** right in rounds 2 and 3, none lost, wrong answers 2 → 2 and 2 → 1. While practising it explains more each round (22 → 26 → 27; 21 → 23 → 23). Below the bar (≥ 3 per half), so its own steps stay off |

Its own steps are readable and built on each other, for example
`own4 = crop(own2, least(own3, colour))` from `own2 = rot180(x)` and `own3 = things(x)`, and
`own1(C) = paint(paint(x, recolour(fill_box(things(x)), C)), things(x))` ("fill each
thing's box with C, keep the thing on top").

**The finding.** With small steps, library learning has material for the first time:
pieces recur, steps are built from steps, practice compounds, and what it grows
transfers to unseen puzzles without loss (old operations: 0 gained, 1 lost). The
transfer is still small because the language explains few tasks at 40k (about 5–8%
of the experience), so few pieces are shared. Two levers remain: the 20 operations the
language cannot express (they need iteration and per-cell rules), and more search per
task for the wake. The fallback is adopted (more right than wrong added); its own
steps are not, by the rule.

**Leak found and closed.** ARC-AGI-2's training set contains 376 of ARC-AGI-1's
evaluation tasks. Ultron's experience (`data.experience()`) excludes them by name.

## Exit criteria (fixed before work starts)

**Robustness (R)**, all measured by the failure lab:

| # | Criterion |
|---|---|
| R1 | Programs: the right law with up to **20%** wrong records |
| R2 | Measurements: the right law with bell-curve noise up to **±10%**, with Ultron estimating the noise itself |
| R3 | Measurements: the right law with up to **20%** gross outliers |
| R4 | The right law with **10** irrelevant measured quantities, in under 10 s |
| R5 | **Every** exact tie between explanations reported, and a separating experiment proposed when Ultron can act |
| R6 | **Zero** false laws claimed on 100 datasets of pure noise or hidden causes |

**Scale (S):**

| # | Criterion |
|---|---|
| S1 | Laws of size **12** found within 60 s (today: about 7) |
| S2 | Search effort per law falls **≥ 10×** on held-out law families after library learning and intuition |

**Expressiveness (E):**

| # | Criterion |
|---|---|
| E1 | Oscillations, quadratic motion and power laws with fractional exponents explained (today: none) |
| E2 | Programs over lists and grids: map, filter, count, objects, symmetry |

**ARC-AGI (A):** the public benchmark, run with the official scoring (2 attempts per test
grid).

| # | Criterion |
|---|---|
| A0 | Harness and an honest baseline score with today's engine on ARC-AGI-1 and ARC-AGI-2 |
| A1 | ≥ **10%** on the ARC-AGI-1 evaluation set |
| A2 | ≥ **25%** |
| A3 | ≥ **40%**: the conquest target for this stage |
| Dream | ≥ **60%** on ARC-AGI-1, and a real score on ARC-AGI-2 |

**Status of every criterion** (updated as each is met):

| Criterion | Status |
|---|---|
| R1, R3, R4, R6 | ✅ met (20% wrong records; 20% outliers; 10 irrelevant in 0.04 s; 0 false laws in 100) |
| R2 | ✅ met. Not told its noise, it **measures it from repeated trials** (1.3% for a true 1%, 12.5% for 10%) and finds F = m·a up to ±20%. Repeated trials also expose a ±5% hidden cause (0 false laws). Without repeats it accepts only a law that explains ≥ 90% of the spread, so it holds to ±2%: without repeating a measurement nobody can tell noise from a small hidden cause |
| R5 | ✅ met. When two measurement laws tie, it sets up the offered experiment where they disagree most. Starting from a wrong law (a label that always equalled the mass), one designed experiment gave F = m·a |
| S1 | ✅ met. **Abstraction sleep** (`brain/abstraction.py`) lines its laws up against each other (anti-unification) to find pieces they share that nobody taught. A piece is kept only if it makes the total description shorter. From five practice laws it extracted (x+1)(y+1), then (x+1)(y+2) built from it, and found held-out laws of **15 and 16 pieces written out in 12 s and 9 s**; without the pieces, nothing (lab: *library learning*). On its real library MDL accepts no piece yet (the best saves 0), so the curriculum is unchanged |
| WP2 speed | Search **5× faster** (a³+b²: 59 s → 12 s). Answers too big to hold are refused before the columns are written out (they were being written to about 200 digits), laws that behave identically are tried once, and candidates are first imagined on 8 examples and checked on all only if they pass |
| S2 | 🟡 **Combined: met. Intuition alone: not met (ARC: 3.9× less effort per explanation; brain search: 1.0× and 0.7×).** Library learning cuts effort by more than 1,400× on held-out family laws. For intuition, v2 (try the guessed laws first) gave 1.0×. v3 measures description length in bits given what intuition expects (DreamCoder's prior): the search runs in that cost (`synthesize(costs=...)`, `dsl.cost`) and the budget is counted in the same currency. On 38 held-out laws (lab laws plus dreams from an unseen seed) it gives **0.7×, with 1 law lost and 4 found longer** (lab: *intuition*). An early reading of 9.6× was an artifact: a budget still counted in nodes made failures cheap, and that is how a³+b² was lost. Variants tried: a usage prior from its own library 0.4×; both combined 0.6×; a softer scale 0.7×. **Why:** a wrong guess pushes a needed law to a dearer level, and search grows exponentially per level, so the losses outweigh the gains at this level of accuracy. By its own rule (kept only if it measurably helps), the brain does **not** use the prior; the machinery stays, and changes nothing when absent (retrain byte-identical). Next for intuition: a recognition model accurate enough to pay, trained on many more of its own solved searches |
| E1 | ✅ met. Two generic additions to the grammar of kinds: a kind applied to a **power of the reading**, and a **recurrence** (the next reading a fixed mix of the last few). Oscillation, damped oscillation, logistic growth (1/y settles) and t^1.5 (y^(2/3) rises evenly) are explained and **predicted for a new object** (lab). Lesson 27 adds pendulums, shock absorbers, yeast and funnels. The never-measured period, damping, capacity and emptying time all come out within about 0.1–0.5%, first attempt |
| E2 | ✅ met. Rows of numbers in the brain's own language: how many, each one stepped, those above or below or equal to something, combined with a law from its library, paired by a law. Lesson 28: "the total" is found as a fold with **its own addition**. On rows 3× longer than any it saw: 120/120; lookup and nearest-neighbour baselines 0–8/30 |
| A0, A1 | ✅ met (C0, C2) |
| A2, A3 | ❌ open |

**No regressions:** all 26 lessons pass on the first attempt, every blind test stays at
100%, and retraining is identical byte for byte.

## Work packages

### WP1. Data that lies (robustness)

| Task | Files | Done when |
|---|---|---|
| Laws with exceptions for programs (MDL: program + listed exceptions); one anomaly prompts a short look for a bigger law, then the law is kept | `synth.py`, `brain.py` | ✅ R1 in tests; lab dial to be extended to 20% |
| Statistical acceptance for measurement laws: typical scatter (median absolute deviation) judged against expected noise; far-off readings set aside | `invariants.py` | ✅ R2, R3 in the lab. Still to do: noise estimated by Ultron when no precision is known |
| Relevance screening: drop quantities whose variation never changes the outcome, before the search | `invariants.py`, `brain.py` | R4 |
| Ties: report every equally short rival; for quantities as for programs, design the experiment that separates them | `invariants.py`, `brain.py` (`propose`) | R5 |
| A false-law audit: 100 noise and hidden-cause datasets in the lab | `judge/failures.py` | R6 |
| Change: when an established law breaks for good, recent experience outweighs old (keep the history, re-measure) | `brain.py` | Lab: *a changing world* |
| Degenerate laws: an invariant made only of things that are always equal says nothing about the world; reject it and report the confounding | `invariants.py` | Lab: *confounders* |
| Eyes that generalise: train on varied noise, sizes, contrast and crowding; look at several scales; self-teach on what lasts | `senses/eyes.py`, lesson 19 | Lab: *eyes* all ≥ 23/25 |

### WP2. Speed

| Task | Done when |
|---|---|
| Check candidates on a small sample first; full check only for survivors | 3× fewer evaluations |
| Vectorised evaluation of candidate programs (numpy) | 5× faster per candidate |
| Size budgets in time, not just candidates; search reports where it stopped | Lab timings |

### WP3. Library learning (the library grows its own primitives)

After laws are confirmed, Ultron looks across everything it knows for **repeated pieces**
(sub-programs used in several laws). A piece becomes a new primitive if adding it
**shortens the total description** of all its laws (MDL over the whole library). This is
the "abstraction sleep" of DreamCoder, done with Ultron's own rule. Big laws become small,
and the wall moves.

Done when S1 is met on law families with shared structure, and every new primitive is
justified by the compression it buys (reported).

**Correction (measured).** Built for ARC first (`arc/library.py`, `arc/curve.py`). It
learned **no** blocks: Ultron's ARC solutions are one or two steps of big hand-written
operations, so nothing recurs often enough to pay for itself. The cross-validated
learning curve was flat (15.19% → 15.19%). Library learning now runs first on the
brain's own laws, where structure recurs, and returns to ARC once learned laws compose.

### WP4. Intuition (the neural guide)

- **Model:** a small network (numpy, deterministic) that reads a task's examples and
  predicts which primitives, and which parent → child pairs, a solution will use.
- **Training data:** every search Ultron has ever solved, plus **dreams**: programs sampled
  from its own library and run to make new practice tasks. It never needs outside data.
- **Use:** the search tries programs in order of the guide's probability within each size,
  instead of blindly. Verification is unchanged: **the guide can only make search faster,
  never make it wrong.**

Done when S2 is met (≥ 10× fewer steps on held-out law families), with determinism kept.

**Correction (measured).** v1 (`arc/guide.py`) ordered operations by four task features.
Cross-validated, it changed nothing (20.5% → 20.5%, 23.5% → 23.5%). v2 predicts *law
families and quantities* (for `arc/objects.py`) and *program pieces* (for `synth.py`).
It is trained on solved searches plus dreams.

On ARC only, a per-puzzle MDL network (in the style of CompressARC) is allowed as a
second engine. It trains on the puzzle alone, its answer is checked against every
example, and it answers only when no symbolic program fits.

### WP5. Expressiveness

| Task | Done when |
|---|---|
| State and change: a thing's state can be a vector (position, speed); kinds of explanation about change (the change of the state is a law of the state) | E1: oscillation, quadratic motion |
| Non-integer exponents through its fractional repeats | E1: power laws |
| Types for lists and grids; map, filter, fold, zip; bounded recursion | E2 |

### WP6. The battlefield: ARC-AGI

1. **Data:** the public ARC-AGI-1 and ARC-AGI-2 repositories, cloned at pinned commits.
   **Discipline:** development only on the *training* tasks. The *evaluation* set is scored
   only at milestones, and every evaluation run is logged so we can't overfit it quietly.
2. **Grid perception,** generic and justified on its own, never per task:
   - colours;
   - objects as connected pieces;
   - size, position and bounding box;
   - symmetry;
   - counting;
   - background;
   - repetition and tiling.
3. **Grid operations:** crop, rotate and flip, scale, recolour, move, draw, fill, tile,
   overlay, sort and select objects.
4. **Solver:** the explanation engine searches for the shortest program mapping every
   input grid to its output grid (with WP3 and WP4 doing the heavy lifting). Two attempts
   per test grid: the shortest explanation and its best rival.
5. **Report:** score per milestone, solved and failed tasks, and why each one failed
   (missing primitive, search too deep, wrong explanation). The failures feed the next round.

### WP7. Integrity

- The failure lab runs after every change; breakpoints only move outward.
- Every primitive added for ARC is listed with why it's generic. The count is reported.
  A solver made of a thousand special cases is not intelligence.
- Blind tests and the 26 lessons stay green.

## Order of attack (corrected after 1a–1b)

| Step | Work | Milestone |
|---|---|---|
| 1a ✅ | WP1 robustness | R1, R3, R4, R6 met; lab report published |
| 1b ✅ | WP6 data and harness; operations frozen; laws about things | **A0**, **A1** (C0–C2) |
| 1c ✅ | R2 (noise measured by Ultron), R5 (separating experiments for measurement ties) | R2, R5 |
| 1d ✅ | WP5: laws of change; lists | E1, E2 (lessons 27, 28) |
| 1e ✅ | WP2 speed, then WP3 library learning on the brain's laws | S1 |
| 1f 🟡 | WP4 intuition v2 and v3 (description length under intuition's prior): combined effort cut by more than 1,400× via library learning; intuition alone 1.0× and 0.7×, so it is not adopted until it pays | S2 |
| 1g | ARC: compose learned laws, new law families, guided search, per-puzzle MDL engine, library learning on ARC again | **A2**, then **A3** |
| 1h | Independent blind test; `reports/stage1_verdict.md` | Stage 1 verdict |

## Risks and how we beat them

| Risk | Counter |
|---|---|
| ARC rewards hand-built DSLs: we might "solve" it by encoding answers | Generic primitives only, counted and justified; evaluation set untouched in development |
| The neural guide is non-deterministic or slow | numpy, single thread, fixed seeds; it only reorders search |
| Library learning adds junk primitives | A primitive must shrink the total description, and is removed if it stops paying |
| Compute in this environment is modest | Per-task time budgets; report solved within budget |
| Robustness changes break old lessons | All 26 lessons and blind tests re-run on every change |

## First moves (now)

1. Finish WP1 step 1 (laws with exceptions): tests, lab, commit.
2. Statistical acceptance for measurement laws (R2, R3), then re-run the lab.
3. Clone ARC-AGI-1 and ARC-AGI-2 at pinned commits and build the harness. Then the
   **A0 baseline**: the first honest number on the board.
