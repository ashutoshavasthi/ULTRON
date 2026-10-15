# Ultron roadmap: growing up

> The architecture and the rules are in [MASTER_PLAN.md](MASTER_PLAN.md). Where every
> earlier result now sits is in [DEVELOPMENT_MAP.md](DEVELOPMENT_MAP.md). The current ages
> are planned in detail in [AGE_0_1_PLAN.md](AGE_0_1_PLAN.md). Every known way to fail is
> in [FAILURE_ATLAS.md](FAILURE_ATLAS.md).

## North star

**Human-like general intelligence, grown from a newborn.** Ultron is raised through the
ages a child passes through, each ending at a gate of milestones that real children are
tested on, until it learns, reasons, talks and explains itself like a capable adult, from
about as much experience as a person gets.

That is a bet, not a promise. So every age has a gate that **could fail**, checked on
situations Ultron has never met, against baselines, against what children actually do,
and by someone who did not build it. A claim is earned only when its gate is passed.

## Principles

1. **Grow in order.** Objects before words, acting before reasoning, other minds before
   school, concrete before abstract. An age is the main line only when the one before it
   has passed its gate.
2. **Understanding before memorising.** Every milestone is tested on situations it has
   never met, against memorising baselines.
3. **A child's amount of experience.** Experience is counted in simulated days and
   compared with what children get. No pretrained models, no language model, no
   internet-sized data.
4. **People are evidence, not truth.** What a caregiver, a book or a web page says is a
   claim with a source. Ultron checks it against what it knows, and trusts people who turn
   out to be right.
5. **Honest about limits.** It says "I can't" when it can't. Reports state failures as
   plainly as successes.
6. **Safety grows with the child.** The more Ultron can do, the stronger the sandbox, the
   exams and human oversight. It can never edit its own exams, drives or goals.

## The ages

| Age | Human equivalent | Status | What develops | Gate (fixed in its plan before the work) |
|---|---|---|---|---|
| **0. Newborn** | 0–3 months | **main line, now** | A body in a continuous nursery world with a caregiver; eyes; habituation; a body map; the caregiver and where they look; memory of its days and sleep | N1–N6 in [AGE_0_1_PLAN.md](AGE_0_1_PLAN.md) |
| **1. Infant** | 3–12 months | planned (exit tests fixed) | Object permanence, solidity, support, gravity; what its actions do; means-end action; gaze following; imitation | I1–I10 in [AGE_0_1_PLAN.md](AGE_0_1_PLAN.md): IntPhys 2019, A-not-B, cloth pulling, gaze following, deferred imitation, Baby Intuitions Benchmark |
| **2. Toddler** | 1–3 years | to be planned at Age 1's gate | First words from the caregiver, the vocabulary spurt, fast mapping, short sentences, categories, tool use, mirror self-recognition, small numbers | Wordbank (MacArthur-Bates CDI) norms; fast mapping and mutual exclusivity; mirror-mark test; stick-to-reach; give-N up to three |
| **3. Preschool** | 3–6 years | to be planned | Theory of mind, causal learning by intervention, counting, asking and being told with selective trust, telling what happened, rule switching, grammar, games with unknown rules | False-belief tests; blicket tasks; give-N (cardinal principle); selective trust; DCCS; SCAN and COGS; W1–W5 |
| **4. School child** | 6–12 years | results banked | Conservation, school arithmetic, measuring and simple science, reading simple texts as claims, core-knowledge puzzles, first programming | Conservation tasks; TIMSS grade 4 released items; ARC-AGI-1 and -2; ARC-AGI-3; Code C1–C3, C5 |
| **5. Adolescent** | 12–18 years | results banked | Abstract reasoning, algebra and proof, laws from real data and films, laws about laws, algorithms and learning machines, a model of itself, a 3D body, reading at length | TIMSS grade 8 and PISA released items; machine-checked proofs; real footage V2–V6; 3D manipulation; Code C4, C6–C8 |
| **6. Adult** | 18+ years | the horizon | Expertise, learning new fields fast, self-improvement under human approval, science | The adult battery in [MASTER_PLAN.md](MASTER_PLAN.md) §5; then C9 and a verified discovery |

"Results banked" means work already done that belongs to that age (lessons 5–30, ARC, the
Code stage). It is kept, keeps passing as a regression check, and is **re-examined at its
own age's gate** against that age's outside yardstick. It is not claimed as that age's
gate until then.

## Rules of development

The full list is in [MASTER_PLAN.md](MASTER_PLAN.md) §4. The short version:

1. Only the current age is the main line; later-age work is a labelled prototype.
2. Every gate has an outside yardstick with human data **and** the owner's blind check.
3. Ages 0–3 happen in the nursery, through the body and the caregiver.
4. Experience is counted in simulated days, next to children's.
5. The innate endowment is fixed; additions need the owner's approval.
6. A ledger of hand-built mechanisms per age; it should shrink.
7. Merge to `main` at every gate.
8. Exit tests fixed before the work; changed protocols reported with both results.

## Where Ultron stands (2026-10-15)

**A patchy mental age.** Ultron has strong school-age and teenage islands, built at a desk
in worlds we designed: arithmetic with invented negative numbers and fractions, Newton's
and Kepler's laws, energy, irrational numbers, logarithms, laws from real films, a grammar
for its tables, and reading Engc and Python. Underneath them, almost everything a baby and
a toddler learn is missing:

| Missing foundation | Why it matters |
|---|---|
| A body that lives in one continuous world | Everything later is learned through acting, not handed over as tables |
| A caregiver and other minds | Most of what a child learns, it learns from people: where to look, what things are called, what others believe |
| Joint attention, imitation, play | How words, tools and games are picked up |
| Theory of mind | Understanding people, being told things, trusting the right people |
| Memory of its own days, and sleep | Learning across days, telling what happened |
| Counting learned rather than innate | Earlier lessons gave exact counting as innate; children learn it at three to four |

Where Ultron was measured against the outside world rather than its own designed worlds,
the gap shows: ARC-AGI-1 evaluation 12.75% (target 25%), and real pendulum and bouncing
films only partly met (V4, V5). Its blind tests were written by the same model that built
it. The new gates fix that by requiring outside yardsticks and the owner's own check.

## Next steps (Age 0, then Age 1)

From [AGE_0_1_PLAN.md](AGE_0_1_PLAN.md):

1. **WP0, outside yardsticks:** obtain IntPhys 2019 and the Baby Intuitions Benchmark and
   copy their scoring and published human and model results into the plan, before any run.
   If either can't be obtained, the plan's written fallback applies.
2. **WP1, the nursery and the body:** one continuous 2D room built on the existing
   camera, scenes, retina and eyes (`senses/`); gaze, two hands, touch; days and nights.
3. **WP2, the caregiver:** a scripted person with a face, gaze and hands; its script is
   committed before any milestone is measured, and it never teaches an exam.
4. **WP3, drives, memory and sleep:** curiosity, habituation and comfort; episodic memory;
   nightly consolidation.
5. **WP4, re-hosting:** lesson 19 (eyes from touch) in the nursery.
6. **WP5, the Age 0 gate,** then Age 1's work packages, then **the Age 1 gate**: the
   owner's blind check, the ledger, merge to `main`, and the Toddler plan written with
   its exit tests fixed.

Language L4 onwards and the Code stage C4(b) onwards **pause as main-line work**. They
are banked results for Ages 3–5 and may continue only as labelled prototypes.

## How we got here

- **2026-06-17.** PRD v1 and v2: a knowledge graph, an NLP pipeline, web checking, a
  theorem prover. Replaced in practice by grounded learning from experience; kept as
  history.
- **2026-09-30.** The first roadmap: a learner built like a child (Brain, Environment,
  Trainer, Judge), with Phase 1 "Baby Ultron". But its lessons began at counting and
  arithmetic, with counting innate, not at the baby stage.
- **Phases 1–3** (to 2026-10-09): inventing numbers and laws, eyes from touch, laws from
  video, new kinds of explanation, acting by running laws backwards
  ([`judge_verdict.md`](../reports/judge_verdict.md),
  [`phase2_verdict.md`](../reports/phase2_verdict.md),
  [`phase3_verdict.md`](../reports/phase3_verdict.md),
  [`phase3_senses_verdict.md`](../reports/phase3_senses_verdict.md)).
- **2026-10-09 to 10-12, the 9-stage campaign:**
  - **Stage 1** (the core and ARC): the verdict met robustness, speed and expressiveness,
    but not ARC ≥ 25% ([`stage1_verdict.md`](../reports/stage1_verdict.md)).
  - **Stage 2** (eyes and real films): V1 and V2 met, V3 and V6 met, V4 and V5 partly met.
  - **Stage 3** (language): L1–L3 met.
  - **Stage 4** and the **Code stage**: planned. C1–C3 and C4(a) were met on the Code
    branch.
  - All of it was integrated in PR #12 ([`integration.md`](../reports/integration.md)).
- **2026-10-15, the review.** The campaign:
  - moved on whenever a stage got hard (Stage 1 to 2 to 3 to Code, with four stages open
    at once);
  - measured itself mostly in worlds it designed;
  - graded itself;
  - never merged to `main`.

  The owner rebuilt the plan around growing a human-like mind from a newborn. Nothing was
  deleted: every result is placed at its age in [DEVELOPMENT_MAP.md](DEVELOPMENT_MAP.md),
  and the old stage plans stay as records.

### What the earlier work taught us (still true)

- **What worked was Ultron's own law-finding applied to what it sees.** Hand-written ARC
  operations (frozen at 38) hit diminishing returns; laws learned per task took ARC-AGI-1
  evaluation from 7.75% to 12.75%.
- **Expressiveness, not search order, was ARC's bottleneck.** A learned intuition ranked
  the right step first and cut search 3.9× without moving the score.
- **Library learning needs material.** It found nothing to compress in a few big
  operations, and needs a finer-grained base where solutions share pieces.
- **Precision matters as much as score.** Ultron answers only when a law fits; every report
  states how many answers were right.
- **Benchmarks hide leaks.** ARC-AGI-2's training set contains 376 of ARC-AGI-1's
  evaluation tasks; experience must exclude held-out tasks by name.
- **Designed worlds flatter.** First-try passes in our own worlds did not carry over to
  outside tests at the same rate. Hence rule 2.

## Competitions

Public benchmarks are **yardsticks**, not the goal. Ultron enters a competition only when
its logged held-out score beats the best published score for that track. We checked ARC
Prize 2026 against this rule and are not entering.

## Honest difficulty

- **Ages 0–1** are concrete: simulated bodies, violation-of-expectation tests and gaze
  following have been built before. The hard part is doing them with one general learner,
  not one hand-built module per milestone (the ledger will show which).
- **Ages 2–3** (words from people, theory of mind) are open research problems for any
  system that is not pretrained on human text.
- **Ages 4–5** have banked results, but those were earned at a desk and must now stand on
  the foundations below them.
- **Age 6** (expertise, self-improvement, discovery) is unsolved in general. Nobody,
  including us, can promise it.
