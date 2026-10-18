# Level map: where every earlier result belongs

When the plan was rebuilt as a capability ladder (2026-10-18, [MASTER_PLAN.md](MASTER_PLAN.md)),
nothing was deleted. This map places every lesson, exam criterion and old stage plan at
the **level** it belongs to.

To avoid a clash of names, the old Stage 3 language criteria (once called L1–L10) are
written **S3-L1** to **S3-L10** here. The levels are **L0** to **L6**.

## What the statuses mean

| Status | Meaning |
|---|---|
| **core** | A property of the learning machinery that every level relies on (robustness, speed, expressiveness). Kept as a failure-lab regression at every gate |
| **banked** | Built and passing, and belongs above the current level. It keeps passing as a regression check, and is re-examined at its own level's gate against that level's outside yardsticks. It is not claimed before then |
| **open** | Not built yet |

The current level is **L0**, so nothing above it counts as passed yet. The banked results
are real, but they stand on foundations still being built.

## Lessons 0–33 (the curriculum in PR #12)

| Lesson | What | Level | Status | Note |
|---|---|---|---|---|
| 0 | Hidden things | L0 | banked | Given as counts; in the room it becomes L0-5 and L0-8 (seen, searched for) |
| 1 | Same number | L1 | banked | Number |
| 2 | Putting together and taking away | L1 | banked | Number |
| 3 | Groups of groups (multiplication) | L3 | banked | |
| 4 | Names for things (number words, place value) | L1 / L3 | banked | Number words at L1, place value at L3 |
| 5 | Pushing, stretching, colliding (F = m·a, stiffness, momentum) | L3 | banked | |
| 6 | Real measurements (Kepler, Boyle) | L3 | banked | |
| 7 | A lab with cheap instruments | L3 | banked | |
| 8 | Owing (inventing negative numbers) | L3 | banked | |
| 9 | Sharing cakes (inventing fractions) | L3 | banked | |
| 10 | The tough final exam | L3 | banked | |
| 11 | The wheel (clock numbers) | L3 | banked | |
| 12 | Hills and valleys (energy) | L3 | banked | |
| 13 | Growing (powers predicted) | L3 | banked | |
| 14 | Hills and a spring (energy with three parts) | L3 | banked | |
| 15 | The diagonal of a tile (irrational numbers) | L3 | banked | |
| 16 | Phase 2 final exam | L3 | banked | |
| 17 | Coiled springs (a law about a law) | L3 | banked | |
| 18 | Phase 3 exam | L3 | banked | |
| 19 | Handling things (eyes trained from touch) | L0 | banked | Becomes L0-1: the same method, from its own grasps in the room |
| 20 | Seeing numbers | L1 | banked | |
| 21 | Watching motion | L0 / L3 | banked | Expecting motion is L0 (L0-5, L0-6); F = m·a from video is L3 |
| 22 | Cooling cups (inventing a kind of explanation) | L3 | banked | |
| 23 | Bouncing, charging, hanging, burning, wandering | L3 | banked | |
| 24 | Using what it knows (puck goals) | L0 / L3 | banked | Acting to reach a goal is L0 (L0-9, L0-10); the friction law is L3 |
| 25 | Phase 3 exam: seeing, inventing, acting | L3 | banked | |
| 26 | The real world: a microscope film (diffusion) | L3 | banked | Stage 2 V2 |
| 27 | Swinging, dying down, growing, emptying | L3 | banked | |
| 28 | Rows of things (lists) | L3 | banked | Stage 1 E2 |
| 29 | The real world: falling (g) | L3 | banked | Stage 2 V3 |
| 30 | The real world: swinging (pendulums) | L3 | banked | Stage 2 V4, partly met. Can't run in an environment that can't fetch its Wikimedia film |
| 31 | Words by pointing | L1 | banked | S3-L1; at L1 the words come from a teacher in a world it acts in |
| 32 | Words for what happens | L1 | banked | S3-L2 |
| 33 | How words combine (a grammar by MDL) | L1 | banked | S3-L3 |

## Code stage (lessons 100–104)

These lessons are on branch `claude/stage-coding-engc-1j7rdc` and are not yet in PR #12.

| Criterion | What | Level | Status |
|---|---|---|---|
| C1, C2 (met) | Reading Engc expressions and statements | L4 | banked |
| C3 (met) | A second and third language, faster | L4 | banked |
| C4(a) (met) | Laws for its own functions | L4 | banked |
| C4(b) | Its own code, from reading the source | L4 | open |
| C5 | Writing programs in Engc | L4 | open |
| C6 | Algorithms and their cost | L4 | open |
| C7 | AI and machine learning | L4 | open |
| C8 | Its twin, in Engc | L4 | open |
| C9 | Improving itself, under approval | L6 | open |

## Old stage criteria

### Stage 1, the scalable core ([STAGE_1_PLAN.md](STAGE_1_PLAN.md), [verdict](../reports/stage1_verdict.md))

| Criterion | Result | Level | Status |
|---|---|---|---|
| R1–R6 (wrong records, noise, outliers, irrelevant quantities, ties and experiments, no false laws) | met | all | core |
| S1 (laws of size 12 within 60 s) | met | all | core |
| S2 (search per law falls ≥ 10×) | met only combined with library learning | all | core |
| E1 (oscillation, quadratic motion, fractional powers) | met | all | core |
| E2 (lists) | met | all | core |
| A0, A1 (ARC harness; ≥ 10% on ARC-AGI-1 evaluation) | met: 12.75% | L3 | banked |
| A2, A3 (≥ 25%, ≥ 40%) | not met | L3 | open |

### Stage 2, the real world through its eyes ([STAGE_2_PLAN.md](STAGE_2_PLAN.md))

| Criterion | Result | Level | Status |
|---|---|---|---|
| V1 (eyes that generalise) | met | L0 | core; checked in the room as L0-1 |
| V2 (diffusion), V3 (g), V6 (detection) | met | L3 | banked |
| V4 (pendulums), V5 (restitution) | not met overall | L3 | banked, open |

### Stage 3, language ([STAGE_3_PLAN.md](STAGE_3_PLAN.md))

| Criterion | Result | Level | Status |
|---|---|---|---|
| S3-L1, S3-L2, S3-L3 (words by pointing, words for its laws, grammar by MDL) | met | L1 | banked |
| S3-L4 (SCAN and COGS) | paused | L1 | open; L1's outside yardstick |
| S3-L5 to S3-L7, S3-L10 (understanding, answering, speaking, blind test) | not started | L1 | open |
| S3-L8 (asking) | not started | L1 | open |
| S3-L9 (being told, as claims) | not started | L1 | open |

### Stage 4, interactive worlds ([STAGE_4_PLAN.md](STAGE_4_PLAN.md))

| Criterion | Level | Status |
|---|---|---|
| W1 (what my actions do), W7 (it knows when its model is wrong) | L0 / L2 | open; their room forms are L0-9 and L0-11 |
| W2 (experiments that decide) | L2 | open |
| W3–W5 (the goal, planning, learning compounds) | L2 | open |
| W6 (ARC-AGI-3), W8 (blind test of games) | L2 | open; L2's outside yardsticks |

### Old stages 5–9

| Old stage | Level |
|---|---|
| 5. The reader | L3 (simple texts), L4 (reading at length, trust per source) |
| 6. A body in 3D | L4 |
| 7. Code, itself, and Engc | L4 (the Code stage, above) |
| 8. Self-improvement | L6 |
| 9. A scientist | L6 |

## What no earlier work covers yet

- **L0:** eyes trained in the room, reaching, searching for hidden things, means-end,
  noticing a changed world, IntPhys.
- **L1:** learning words from a teacher in a world it acts in, following gaze, copying a
  demonstration, SCAN and COGS.
- **L2:** modelling other agents' goals and beliefs, games with unknown rules, planning in a
  learned model.
- **L4:** machine-checked proofs; writing programs (C5 onwards).
- **L5–L6:** everything.
