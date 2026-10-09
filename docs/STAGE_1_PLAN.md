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
| Shapes of law | ✅ settling, straight lines, and **quadratic (invented a new kind on its own)**; ❌ oscillation, damped oscillation, logistic growth, power law t^1.5 |
| Eyes | ✅ 25/25 at the noise it grew up with; ❌ double noise, faint and touching things. Two redesigns tried (dilated 8- and 16-channel networks with contrast adaptation): big things 25/25 and faint 16/25, but the original trays dropped to 37/40, so they weren't adopted. **Open** |

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

**Milestones since A0** (every evaluation run is in `reports/arc_runs.log`):

| Milestone | What changed | ARC-AGI-1 training | ARC-AGI-1 evaluation | ARC-AGI-2 evaluation |
|---|---|---|---|---|
| A0 | First engine | 11.0% | 3.75% | 0% |
| A1 | Hand-written operations **frozen at 38**; local laws, pattern ops | 22.8% | **7.75%** (right 31 of 33 answered) | 0% |
| A2 | Ultron's law-finding applied to things: thing laws, marks and rays, which thing is the answer, how things move | 28.2% | **10.0%** (right 40 of 52 answered) | 0% |

A2 meets the A1 target (≥10%).

**Library learning: an honest null result so far.** Ultron's solved programs are almost
all one operation plus a learned law. No piece recurs often enough to pay for itself
under MDL, even at 10× search budget and with blocks that leave a colour or a whole step
open. So **no blocks are learned**, and the cross-validated learning curve is flat
(15.19% → 15.19% on the unseen half). We do not lower the bar to manufacture blocks.

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

### WP4. Intuition (the neural guide)

- **Model:** a small network (numpy, deterministic) that reads a task's examples and
  predicts which primitives, and which parent → child pairs, a solution will use.
- **Training data:** every search Ultron has ever solved, plus **dreams**: programs sampled
  from its own library and run to make new practice tasks. It never needs outside data.
- **Use:** the search tries programs in order of the guide's probability within each size,
  instead of blindly. Verification is unchanged: **the guide can only make search faster,
  never make it wrong.**

Done when S2 is met (≥ 10× fewer steps on held-out law families), with determinism kept.

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

## Order of attack

| Step | Packages | Milestone |
|---|---|---|
| 1a | WP1 robustness, WP2 speed | R1–R6 met; lab report published |
| 1b | WP6 data and harness, WP5 grids | **A0**: an honest ARC baseline |
| 1c | WP3 library learning | S1; **A1** |
| 1d | WP4 intuition | S2; **A2** |
| 1e | All, iterated on ARC failures | **A3**; Stage 1 verdict |

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
