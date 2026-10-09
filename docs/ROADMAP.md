# Ultron roadmap: toward general intelligence

> The full architecture and campaign are in [MASTER_PLAN.md](MASTER_PLAN.md). The first
> stage is planned in detail in [STAGE_1_PLAN.md](STAGE_1_PLAN.md). Every known way to
> fail is in [FAILURE_ATLAS.md](FAILURE_ATLAS.md).

## North star

**Ultron's goal is general intelligence (AGI), and beyond it, superhuman intelligence
(ASI).** The bet is that intelligence comes from *understanding*, not volume: finding the
simplest explanation that fits, inventing concepts, testing every idea against the world,
and so needing far less data than today's large language models.

That bet is unproven. Ultron is a working prototype of the approach, not proof that it
reaches AGI. So every step below has an **exit test that could fail**, checked on problems
Ultron has never seen, against baselines, and wherever possible by outsiders. A claim is
earned only when its test is passed.

## Principles

1. **Understanding before memorising.** A phase is done only when Ultron solves held-out
   problems that memorisers fail.
2. **Less data, better used.** Ultron should learn from far less data than a large language
   model. We measure that directly: data used per problem solved, against baselines.
3. **The internet is evidence, not truth.** Ultron may read the web, but every fact it reads
   is a *claim* with a source. It is checked against its own laws, other sources and, when it
   can, experiment. It keeps what survives, and remembers why.
4. **Compress, don't hoard.** Ultron extracts laws and concepts from what it reads, not
   copies of it. A good reader turns a thousand pages into a few laws that predict the next
   page.
5. **Honest about limits.** It says "I can't" when it can't. Reports state failures as
   plainly as successes.
6. **Safety grows with capability.** The more Ultron can do, the stronger the sandbox, the
   exams and human oversight. An agent that edits itself must never be able to edit its own
   exams or its sandbox.

## Done so far

| Phase | What Ultron can do | Evidence |
|---|---|---|
| 1. Baby Ultron | Counting, arithmetic, place value and grounded words; physics laws; Kepler's and Boyle's laws from real data; **invented negative numbers and fractions** | [`judge_verdict.md`](../reports/judge_verdict.md) |
| 2. Inventing concepts, generally | Clock numbers, irrational numbers, energy with any number of parts, powers predicted before being met, roots and logarithms | [`phase2_verdict.md`](../reports/phase2_verdict.md) |
| 2+. Closing the gaps | Column arithmetic, fractional repeats, laws about its own laws | [`phase3_verdict.md`](../reports/phase3_verdict.md) |
| 3. Senses, new kinds of explanation, a body | Eyes it learns itself; F = m·a, stiffness and energy from video; **two new kinds of explanation invented and reused**; goals reached on floors it never touched | [`phase3_senses_verdict.md`](../reports/phase3_senses_verdict.md) |
| 3+. The real world (begun) | A real microscope film from the internet: Einstein's law of diffusion measured from raw pixels, matching the scientists' own tool (1.63 vs 1.65 µm²/s) | Scripts work; lesson 26 is Stage 2's first move |
| Stage 1 (in progress) | Survives 20% wrong records, ±20% noise and 20% outliers; notices confounders; updates when the world changes; 0 false laws in 100; ARC-AGI-1 evaluation **10.0%** | [`STAGE_1_PLAN.md`](STAGE_1_PLAN.md), [`ARC_REPORT.md`](ARC_REPORT.md) |

Blind tests by examiners who never saw the code scored 55/60, 54/60 and 45/50 on first
sight. The examiners were the same underlying model as the trainer, so a human's blind
test still counts for more.

## The road ahead

One campaign, numbered the same here and in [MASTER_PLAN.md](MASTER_PLAN.md). Each stage
closes one of the honest gaps between today's Ultron and general intelligence. It is the
main line only once the stage before it has passed **every** exit test on held-out
problems, with no regressions. The order puts the biggest risk first: if the core can't
scale, nothing else matters.

| Stage | The gap it closes | What gets built | Exit test (could fail) |
|---|---|---|---|
| **1. The scalable core** *(now)* | Search is exponential: Ultron finds small laws, not big programs | Robustness to bad data; laws of change; lists; speed; library learning on its own laws; an intuition trained on its own searches; ARC-AGI as the battlefield | The criteria in [STAGE_1_PLAN.md](STAGE_1_PLAN.md): R1–R6 (bad data), S1–S2 (laws of size 12, 10× less search), E1–E2 (oscillation, logistic, lists), A2–A3 (≥ 25%, then ≥ 40% on ARC-AGI-1 evaluation) |
| **2. The real world through its eyes** | It has seen one real film, and its eyes don't generalise | First, **eyes that generalise** (double noise, faint and touching things). Then lesson 26 (the microscope film), then many real videos: falling, swinging, bouncing, colliding | Rediscovers g, pendulum periods, restitution and diffusion from **real footage**, within measured error |
| **3. Interactive worlds** *(new)* | It has acted only with one kick in a world whose rules it was told | Grid games with unknown rules (like ARC-AGI-3). Ultron explores, runs experiments, learns the rules **and the goal** as laws, and plans in its own learned model. Laws that recur across games become priors | Wins held-out games it has never seen, in close to the fewest actions; later games need fewer actions than earlier ones (learning compounds) |
| **4. The reader** | It knows only what it experienced | Open data and text read as **claims with sources**, checked against its laws, other sources and experiment; reading driven by curiosity | Learns laws from open data it was never taught and predicts held-out data. Catches ≥ 90% of planted false claims. Reaches a target accuracy with ≥ 100× fewer bytes read than a fixed, named small language-model baseline |
| **5. Language** | It knows about 40 grounded words | Words by pointing, then grammar, then conversation, all grounded in concepts it already has | Understands new sentences about its worlds, answers questions, detects false statements, asks good questions; human blind evaluation |
| **6. A body in 3D** | Its actions are 2D and few | A 3D physics simulator (MuJoCo or PyBullet), goals, planning with its own world model, tools | Solves new manipulation tasks by planning: a taller tower than it has ever seen, using an object as a tool |
| **7. Code, itself, and Engc** | It can't write real programs | Its program language grows into a general one. It studies its own Python source as a world. It learns [Engc-V1](https://github.com/ashutoshavasthi/Engc-V1) and writes its twin in Engc | Correct programs for unseen specs; predicts its own modules' behaviour; its Engc twin passes every exam with identical answers |
| **8. Self-improvement, safely** | Its building blocks are still designed by people | Proposes changes to its own code and grammar, each sandboxed, kept only if every exam passes and learning measurably improves, reversible, and **approved by a human** | Measurably better at *learning*, with zero regressions; invents a building block nobody gave it, and uses it |
| **9. A scientist** | Everything it knows, someone knew before | Cross-domain analogy, its own experiment design, real literature read as claims, deep mastery of one field (for example, mathematics with machine-checked proofs) | **Discovers something new** in a field it was not taught, verified independently |

### The safety track runs alongside, not at the end

Safety pieces are built **before** the stage that needs them:

| Built before | What |
|---|---|
| Stage 4 (the reader: first contact with text written to deceive) | Exams and sandbox Ultron cannot modify (read-only, hash-checked by the Judge); an audit log of every belief change with its evidence; untrusted text can never become an instruction, only a claim |
| Stage 8 (self-improvement) | Human approval of every self-change; rollback; a kill switch |

### What we learned building Stage 1 (and changed in the plan)

- **Library learning needs material.** On ARC, Ultron's solutions are one or two steps of
  big hand-written operations, so no piece recurred and MDL rightly learned no blocks (a
  null result, recorded). Library learning now starts on the brain's own laws, where
  structure does recur, and returns to ARC once learned laws compose.
- **Intuition v1 (operation order from four task features) changed nothing**, measured
  by cross-validation. v2 predicts law families and program pieces, trained on solved
  searches plus "dreams".
- **What worked was Ultron's own law-finding, applied to the things it sees.** Hand-written
  ARC operations are frozen at 38. New ARC ability came from laws learned per task (thing
  laws, marks, which thing, how things move), which took ARC-AGI-1 evaluation from 7.75%
  to 10.0%.
- **Benchmarks hide leaks.** ARC-AGI-2's training set contains 376 of ARC-AGI-1's
  evaluation tasks. Ultron's experience excludes every evaluation task by name.
- **Precision matters as much as score.** Ultron answers only when a law fits, and every
  report states how many of its answers were right.

### Competitions

Public benchmarks are **yardsticks**, not the goal. Ultron enters a competition only when
its logged held-out score beats the best published score for that track. We checked ARC
Prize 2026 against this rule and are not entering.

## What would count as AGI, and ASI

Claims like these have to be testable, so the bar is fixed **now**, in advance, and does
not move.

- **AGI (our working definition):** across fields it was never trained on, Ultron learns a
  new skill from a handful of examples and some reading, at the level of a capable human
  learner, and explains its answers. **The fixed test battery:**
  - ARC-AGI-1, -2 and -3, scored officially on held-out sets;
  - the held-out exams of every stage;
  - blind tests written by people who never saw its code;
  - data efficiency: data and search per law, against fixed baselines.

  Stages 1–7 are the parts of that.
- **ASI:** consistently beyond the best human experts at producing *verified* new knowledge
  (stage 9 at scale). This is a far horizon. It also needs a level of safety and oversight
  that has to be built before the capability, not after.

## Honest difficulty

- **Stages 1–4** are where the bet gets tested. Each is hard but concrete, and each could
  fail in a way we would learn from.
- **Stages 5–7** are open research problems. The pieces exist but have never been combined
  well.
- **Stages 8–9** are unsolved in general. Nobody, including us, can promise them.

## Next steps (Stage 1, to completion)

1. **R2**: Ultron estimates its own measurement noise when it isn't told it.
2. **R5**: when two measurement laws tie, it designs the experiment that separates them.
3. **E1**: laws of change (oscillation, damped oscillation, logistic growth, t^1.5).
4. **E2**: lists in its program language (map, filter, count, fold).
5. **Speed, then S1**: library learning on its own laws, to reach laws of size 12.
6. **S2**: intuition v2, trained on its own searches and dreams.
7. **A2 (≥ 25%), then A3 (≥ 40%)** on ARC-AGI-1 evaluation, logged at checkpoints only.
8. **The Stage 1 verdict**, with an independent blind test.

Network note: this environment can reach GitHub and the Python Package Index. Wikimedia,
YouTube, archive.org and arcprize.org are blocked. They can be allowed under the cloud
environment's **Network access** settings. Stage 2 needs the first three and stage 3
needs arcprize.org; otherwise those stages fall back to data hosted on GitHub or PyPI and
to games we write ourselves.
