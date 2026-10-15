# Development map: where every earlier result belongs

When the plan was rebuilt around growing up (2026-10-15, [MASTER_PLAN.md](MASTER_PLAN.md)),
nothing was deleted. This map places every lesson, exam criterion and stage plan built
so far at the **age** it belongs to.

## What the statuses mean

| Status | Meaning |
|---|---|
| **core** | A property of the learning machinery that every age relies on (robustness, speed, expressiveness). Kept as a failure-lab regression at every gate |
| **re-host** | Belongs to Ages 0–3, which must happen in the nursery through the body and the caregiver (rule 3). It was learned at a desk, so it counts only once redone in the nursery |
| **banked** | Belongs to Age 4 or later. It is kept and keeps passing as a regression check. It is re-examined at its own age's gate, against that age's outside yardstick, under the new innate endowment (exact counting no longer innate). It is not claimed before then |
| **open** | Not built yet |

The current age is **0 (newborn)**, so nothing above it counts as passed yet. That is the
point of hard gates: the banked results are real, but they stand on foundations not yet
built.

## Lessons 0–33 (the curriculum in PR #12)

| Lesson | What | Age | Status | Note |
|---|---|---|---|---|
| 0 | Hidden things | 1 | re-host | Object permanence, but given as counts. In the nursery it becomes I1 and I4 (seen, searched for) |
| 1 | Same number | 3 | re-host | One-to-one correspondence; preschool counting |
| 2 | Putting together and taking away | 3 | re-host | Small-number expectations (1 + 1) are an Age 1 stretch; adding counts is preschool |
| 3 | Groups of groups (multiplication) | 4 | banked | School arithmetic |
| 4 | Names for things (number words, place value) | 3 / 4 | re-host / banked | Number words learned from the caregiver at Ages 2–3; place value is school (Age 4) |
| 5 | Pushing, stretching, colliding (F = m·a, stiffness, momentum) | 5 | banked | Quantitative laws; the intuitive "pushes make things move" is I5 |
| 6 | Real measurements (Kepler, Boyle) | 5 | banked | |
| 7 | A lab with cheap instruments | 5 | banked | |
| 8 | Owing (inventing negative numbers) | 4 | banked | |
| 9 | Sharing cakes (inventing fractions) | 4 | banked | |
| 10 | The tough final exam | 5 | banked | Division by reasoning backwards, unseen bodies, "I can't" |
| 11 | The wheel (clock numbers) | 4 | banked | |
| 12 | Hills and valleys (energy) | 5 | banked | |
| 13 | Growing (powers predicted) | 5 | banked | |
| 14 | Hills and a spring (energy with three parts) | 5 | banked | |
| 15 | The diagonal of a tile (irrational numbers) | 5 | banked | |
| 16 | Phase 2 final exam | 5 | banked | |
| 17 | Coiled springs (a law about a law) | 5 | banked | |
| 18 | Phase 3 exam | 5 | banked | |
| 19 | Handling things (eyes trained from touch) | 0 | re-host | Becomes N2: the same training pairs, from its own grasps in the nursery |
| 20 | Seeing numbers | 3 | re-host | Counting what it sees |
| 21 | Watching motion | 1 / 5 | re-host / banked | Following things and expecting motion is Age 1 (I1, I2); F = m·a from video is Age 5 |
| 22 | Cooling cups (inventing a kind of explanation) | 5 | banked | |
| 23 | Bouncing, charging, hanging, burning, wandering | 5 | banked | |
| 24 | Using what it knows (puck goals) | 1 / 4 | re-host / banked | Acting to reach a goal is Age 1 (I5, I6); the friction law and goals on new floors are Age 4 |
| 25 | Phase 3 exam: seeing, inventing, acting | 5 | banked | |
| 26 | The real world: a microscope film (diffusion) | 5 | banked | Stage 2 V2 |
| 27 | Swinging, dying down, growing, emptying | 5 | banked | |
| 28 | Rows of things (lists) | 4 | banked | Stage 1 E2 |
| 29 | The real world: falling (g) | 5 | banked | Stage 2 V3 |
| 30 | The real world: swinging (pendulums) | 5 | banked | Stage 2 V4 (partly met) |
| 31 | Words by pointing | 2 | re-host | Stage 3 L1. Learned by overhearing sentences about tables; at Age 2 the words come from the caregiver, through joint attention |
| 32 | Words for what happens | 2 | re-host | Stage 3 L2 |
| 33 | How words combine (a grammar by MDL) | 3 | re-host | Stage 3 L3 |

## Code stage (lessons 100–104)

These lessons are on branch `claude/stage-coding-engc-1j7rdc`. PR #12 has only the Code
stage's plan. The code and results for C1–C4(a) are **not yet** in PR #12.

| Criterion | What | Age | Status |
|---|---|---|---|
| C1 (met, lesson 100) | Reading Engc expressions | 4 | banked |
| C2 (met, lesson 101) | Reading Engc statements | 4 | banked |
| C3 (met, lessons 102–103) | A second and third language, faster | 4 | banked |
| C4(a) (met, lesson 104) | Laws for its own functions | 5 | banked |
| C4(b) | Its own code, from reading the source | 5 | open |
| C5 | Writing programs in Engc | 4 | open |
| C6 | Algorithms and their cost | 5 | open |
| C7 | AI and machine learning | 5 | open |
| C8 | Its twin, in Engc | 5 | open |
| C9 | Improving itself, under approval | 6 | open |

## Old stage criteria

### Stage 1, the scalable core ([STAGE_1_PLAN.md](STAGE_1_PLAN.md), [verdict](../reports/stage1_verdict.md))

| Criterion | Result | Age | Status |
|---|---|---|---|
| R1–R6 (wrong records, noise, outliers, irrelevant quantities, ties and experiments, no false laws) | met | all | core |
| S1 (laws of size 12 within 60 s) | met | all | core |
| S2 (search per law falls ≥ 10×) | met only combined with library learning | all | core |
| E1 (oscillation, quadratic motion, fractional powers) | met | all | core |
| E2 (lists) | met | all | core |
| A0, A1 (ARC harness; ≥ 10% on ARC-AGI-1 evaluation) | met: 12.75% | 4 | banked |
| A2, A3 (≥ 25%, ≥ 40%) | not met | 4 | open; ARC-AGI is Age 4's outside yardstick |

### Stage 2, the real world through its eyes ([STAGE_2_PLAN.md](STAGE_2_PLAN.md))

| Criterion | Result | Age | Status |
|---|---|---|---|
| V1 (eyes that generalise) | met | 0 | core. Re-checked in the nursery as N2 |
| V2 (diffusion, lesson 26) | met | 5 | banked |
| V3 (g, lesson 29) | met | 5 | banked |
| V4 (pendulums, lesson 30) | not met overall (√length law met) | 5 | banked, open |
| V5 (restitution) | not met overall (one film of two) | 5 | banked, open |
| V6 (detection on par with lab tools) | met | 5 | banked |

### Stage 3, language ([STAGE_3_PLAN.md](STAGE_3_PLAN.md))

| Criterion | Result | Age | Status |
|---|---|---|---|
| L1 (words by pointing) | met (lesson 31) | 2 | re-host |
| L2 (words for its own laws) | met (lesson 32) | 2 | re-host |
| L3 (a grammar by MDL) | met (lesson 33) | 3 | re-host |
| L4 (SCAN and COGS) | paused | 3 | open; an Age 3 outside yardstick |
| L5 (understanding statements) | not started | 3 | open |
| L6 (answering questions) | not started | 3 | open |
| L7 (speaking) | not started | 2–3 | open |
| L8 (asking) | not started | 3 | open |
| L9 (being told, as claims) | not started | 3 | open; selective trust is its developmental form |
| L10 (blind test) | not started | 3 | open |

### Stage 4, interactive worlds ([STAGE_4_PLAN.md](STAGE_4_PLAN.md))

| Criterion | Age | Status |
|---|---|---|
| W1 (what my actions do) | 1 | open; its nursery form is I5 |
| W2 (experiments that decide) | 1 | open; play that separates rival laws |
| W3 (what the game wants) | 3 | open |
| W4 (planning in its own model) | 3 | open |
| W5 (learning compounds) | 3 | open |
| W6 (ARC-AGI-3, sealed games) | 4 | open; an Age 4 outside yardstick |
| W7 (it knows when its model is wrong) | 1 / 3 | open; its nursery form is I10 |
| W8 (blind test of games) | 4 | open |

### Stages 5–9 of the old campaign

| Old stage | Age |
|---|---|
| 5. The reader (open data, text as claims) | 4 (simple texts), 5 (reading at length, trust per source) |
| 6. A body in 3D | Basics of a body at Age 0 (2D); 3D manipulation and tools at Age 5 |
| 7. Code, itself, and Engc | 4–5 (the Code stage, above) |
| 8. Self-improvement, safely | 6 |
| 9. A scientist | 6 |

## What is missing entirely (no earlier work)

Ages 0–3 need these, and nothing built so far provides them:

- a continuous world with days and nights;
- a body map;
- a caregiver;
- habituation;
- episodic memory of its days;
- gaze following and joint attention;
- imitation;
- tool use;
- mirror self-recognition;
- learning to count rather than having counting innate;
- theory of mind (false belief);
- selective trust;
- rule switching;
- telling what happened.
