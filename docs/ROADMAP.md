# Ultron roadmap: toward general intelligence

> The full architecture and campaign are in [MASTER_PLAN.md](MASTER_PLAN.md). The first
> stages are planned in detail in [STAGE_1_PLAN.md](STAGE_1_PLAN.md),
> [STAGE_2_PLAN.md](STAGE_2_PLAN.md) and [STAGE_3_PLAN.md](STAGE_3_PLAN.md). Every known
> way to fail is in [FAILURE_ATLAS.md](FAILURE_ATLAS.md).

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
| Stage 1 (in progress) | Survives 20% wrong records, ±20% noise and 20% outliers; notices confounders; updates when the world changes; 0 false laws in 100; ARC-AGI-1 evaluation **12.75%** (51 of 63 answers right) | [`STAGE_1_PLAN.md`](STAGE_1_PLAN.md), [`ARC_REPORT.md`](ARC_REPORT.md) |
| Stage 3, language (begun) | Finds kinds of thing (colours, sizes, shapes) before any word, then learns words from sentences it overhears about tables; picks out the thing meant in word pairs it never heard (200/200), refuses words never taught, never answers wrong. In films, learns words for what happens and for comparing, bound to its own kinds of law and to quantities it measures (heavier by its momentum law): 200/200 and 113/120, never a false word | [`STAGE_3_PLAN.md`](STAGE_3_PLAN.md) |

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
| **1. The scalable core** *(verdict written: A2–A3 not met, see below)* | Search is exponential: Ultron finds small laws, not big programs | Robustness to bad data; laws of change; lists; speed; library learning on its own laws; an intuition trained on its own searches; ARC-AGI as the battlefield | The criteria in [STAGE_1_PLAN.md](STAGE_1_PLAN.md): R1–R6 (bad data), S1–S2 (laws of size 12, 10× less search), E1–E2 (oscillation, logistic, lists), A2–A3 (≥ 25%, then ≥ 40% on ARC-AGI-1 evaluation) |
| **2. The real world through its eyes** *(V1–V2 met; V3–V6 in progress alongside stage 3)* | It has seen one real film, and its eyes don't generalise | First, **eyes that generalise** (double noise, faint and touching things). Then lesson 26 (the microscope film), then many real videos: falling, swinging, bouncing, colliding | Rediscovers g, pendulum periods, restitution and diffusion from **real footage**, within measured error |
| **3. Language** *(now: L1–L3 met; paused at L4 on 2026-10-11 by the owner's decision, until the coding work passes)* | It knows 37 grounded words, all about numbers; it cannot understand, say or ask a sentence | Words by pointing, then words for its own laws, then a grammar it finds by MDL, then understanding, answering, speaking, asking and being told. All grounded in concepts it already has; no pretrained language | The criteria in [STAGE_3_PLAN.md](STAGE_3_PLAN.md): L1–L10 on held-out scenes and sentences, against fixed baselines, including SCAN (≥ 95% on the jump and length splits) and COGS (≥ 90%), with ≤ 10,000 sentences heard |
| **4. Interactive worlds** | It has acted only with one kick in a world whose rules it was told | Grid games with unknown rules (like ARC-AGI-3). Ultron explores, runs experiments, learns the rules **and the goal** as laws, and plans in its own learned model. Laws that recur across games become priors | Wins held-out games it has never seen, in close to the fewest actions; later games need fewer actions than earlier ones (learning compounds) |
| **5. The reader** | It knows only what it experienced | Open data, then text (which needs stage 3), read as **claims with sources**, checked against its laws, other sources and experiment; reading driven by curiosity | Learns laws from open data it was never taught and predicts held-out data. Catches ≥ 90% of planted false claims. Reaches a target accuracy with ≥ 100× fewer bytes read than a fixed, named small language-model baseline |
| **6. A body in 3D** | Its actions are 2D and few | A 3D physics simulator (MuJoCo or PyBullet), goals, planning with its own world model, tools | Solves new manipulation tasks by planning: a taller tower than it has ever seen, using an object as a tool |
| **7. Code, itself, and Engc** | It can't write real programs | Its program language grows into a general one. It studies its own Python source as a world. It learns [Engc-V1](https://github.com/ashutoshavasthi/Engc-V1) and writes its twin in Engc | Correct programs for unseen specs; predicts its own modules' behaviour; its Engc twin passes every exam with identical answers |
| **8. Self-improvement, safely** | Its building blocks are still designed by people | Proposes changes to its own code and grammar, each sandboxed, kept only if every exam passes and learning measurably improves, reversible, and **approved by a human** | Measurably better at *learning*, with zero regressions; invents a building block nobody gave it, and uses it |
| **9. A scientist** | Everything it knows, someone knew before | Cross-domain analogy, its own experiment design, real literature read as claims, deep mastery of one field (for example, mathematics with machine-checked proofs) | **Discovers something new** in a field it was not taught, verified independently |

### The safety track runs alongside, not at the end

Safety pieces are built **before** the stage that needs them:

| Built before | What |
|---|---|
| Stage 5 (the reader: first contact with text written to deceive) | Exams and sandbox Ultron cannot modify (read-only, hash-checked by the Judge); an audit log of every belief change with its evidence; untrusted text can never become an instruction, only a claim |
| Stage 8 (self-improvement) | Human approval of every self-change; rollback; a kill switch |

### What we learned building Stage 1 (and changed in the plan)

- **Library learning needs material.** On ARC, Ultron's solutions are one or two steps of
  big hand-written operations, so no piece recurred and MDL rightly learned no blocks (a
  null result, recorded). Library learning now starts on the brain's own laws, where
  structure does recur, and returns to ARC once learned laws compose. Measured again
  with a wake–sleep loop that also learns from near-misses (descriptions with
  exceptions): 2 blocks per half, 0 tasks gained on unseen tasks. **On ARC, growing its
  own operations needs a finer-grained base language**, where solutions are long and
  share pieces.
- **Search order is not ARC's bottleneck; expressiveness is.** A learned intuition ranks
  the right step first (median rank 1 of ~200) and cuts search 3.9×, yet the score does
  not move: most unsolved tasks have no explanation in two or three of the 38 operations.
- **Intuition v1 (operation order from four task features) changed nothing**, measured
  by cross-validation. v2 predicts law families and program pieces, trained on solved
  searches plus "dreams".
- **What worked was Ultron's own law-finding, applied to the things it sees.** Hand-written
  ARC operations are frozen at 38. New ARC ability came from laws learned per task (thing
  laws, marks, which thing, how things move, symmetry, copies, lines, summaries,
  arrangements), which took ARC-AGI-1 evaluation from 7.75% to 12.75%; training gains
  reached evaluation at about one third, and the families hit diminishing returns.
- **Benchmarks hide leaks.** ARC-AGI-2's training set contains 376 of ARC-AGI-1's
  evaluation tasks. Ultron's experience excludes every evaluation task by name.
- **Precision matters as much as score.** Ultron answers only when a law fits, and every
  report states how many of its answers were right.

### Language restored as stage 3 (2026-10-11)

The first roadmap (2026-09-30) had **grounded language** as phase 5, with the rule
"language after the concepts it names; only then reading". When the roadmap was
revised on 2026-10-09, reading was split into its own stage and put **before** language,
and each stage inserted later pushed language further back, to stage 5. It never had a
stage plan or an exit test with numbers, and nothing has been built for it since lesson 4's
words. The owner noticed it was missing. Language is now stage 3, right after the real
world, because the reader cannot check what a text claims until Ultron understands the
text. Its exit test is fixed in [STAGE_3_PLAN.md](STAGE_3_PLAN.md), which also records
the history commit by commit.

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

- **Stages 1, 2, 4 and 5** are where the bet gets tested. Each is hard but concrete, and
  each could fail in a way we would learn from.
- **Stages 3, 6 and 7** are open research problems. The pieces exist but have never been
  combined well.
- **Stages 8–9** are unsolved in general. Nobody, including us, can promise them.

## Next steps (Stages 2 and 3, in parallel)

**Stage 1 verdict** ([`reports/stage1_verdict.md`](../reports/stage1_verdict.md)):
R1–R6, S1, E1–E2, A0–A1 met; S2 met only combined with library learning; A2–A3
(ARC ≥ 25%, ≥ 40%) not met. **Correction (2026-10-11):** the owner moved the main line to
Stage 2 because further ARC work was not paying off. ARC returns in Stage 4 (interactive
worlds) and in the fixed AGI battery.

Stage 2 plan and exit test: [STAGE_2_PLAN.md](STAGE_2_PLAN.md).
1. ✅ **Eyes that generalise:** every eyes row of the failure lab now 24–25/25 (look
   longer at still scenes, adapt to the light, step back for big things, broader
   handling).
2. ✅ **Lesson 26:** diffusion from the real microscope film: D within 4% of the
   scientists' tool, Einstein's law found, in the curriculum (29 lessons).
3. ✅ **g from real footage** (lesson 29): the law of falling found from three real lab
   films; g = 9.65 ± 0.15 m/s² against 9.80
   ([`stage2_v3_falling.md`](../reports/stage2_v3_falling.md)).
4. ✅ **Detection on par with a lab tool** (V6): Ultron's positions match the lab's own
   hand marks on both marked films ([`stage2_v4_v6.md`](../reports/stage2_v4_v6.md)).
5. **Pendulum periods and the √length law, restitution** (V4, V5): not met, with parts
   met. Lesson 30: from three real pendulums (0.5, 0.785 and 1 m) Ultron finds by itself
   that L/T² stays the same, and the √length law passes its fixed rule (power
   0.470 ± 0.029; constant 2.023 ± 0.013 against 2.007). Per film, only the 0.5 m film
   passes: 0.785 m is 2% fast, and 1 m shows one swing. V5: the GB Drop film passes
   (e = 0.843 ± 0.003 against the lab's 0.836 ± 0.006), but in the corridor film Ultron
   follows the ball through only one of four bounces
   ([`stage2_v4_v6.md`](../reports/stage2_v4_v6.md)).

**Correction (2026-10-11):** the owner started **Stage 3, language**, before Stage 2's
verdict, when Stage 2's V3–V6 seemed blocked on footage. Real footage has since been
found, so the two stages now run in parallel. Stage 2 stays open; its exit test is
unchanged.

**Lesson numbers (2026-10-11).** Stage 2 and Stage 3 were built side by side and both
took lessons 29 and 30. In the combined curriculum, Stage 2 keeps 29 (g from real
footage) and 30 (real pendulums), and the language lessons become 31 and 32. Their
seeds, and so their teaching and exam worlds, are the ones fixed when they were 29 and
30; only the number changed.

Stage 3 plan and exit test: [STAGE_3_PLAN.md](STAGE_3_PLAN.md).
1. ✅ **L1, words by pointing** (lesson 31): from sentences it overhears about tables,
   with nobody saying which word means what or which thing is meant, it finds its own
   kinds of thing (4 colours, 2 sizes, shapes), then the words: 200/200 on word pairs it
   never heard (baselines 39% and 20%), words never taught refused 30/30, never a wrong
   answer in the exam or the failure lab.
2. ✅ **L2, words for its own laws** (lesson 32): in films, it sees each motion as one of
   its own kinds of law and learns falls, bounces, rolls, stops, and the comparing words
   faster, heavier (by its momentum law), before, after, more, fewer. Naming what things
   never seen doing it do: 200/200 (a word counter given its kinds also 200/200);
   filling in the comparing word: 113/120 (counter 100/120), never a false word in the
   exam or the failure lab (32 lessons).
3. ✅ **L3, a grammar found by MDL** (lesson 33): from 300 sentences about tables, with
   nobody saying which thing is meant or what a word does, it finds what each word does
   and how it combines (a small categorial grammar). On held-out sentences: 69/70 nested
   deeper than any it heard, 59/60 with more phrases joined, 70/70 with words in new
   places; never a wrong answer in the exam or the failure lab (34 lessons).
4. ⏸ **L4, SCAN and COGS**: paused on 2026-10-11 (the owner's decision) until the coding
   work passes. Published baselines confirmed and recorded in the plan.

Network note (updated 2026-10-11): this environment reaches GitHub, the Python Package
Index, Wikimedia (which rate-limits original files), YouTube and archive.org; earlier the
last three were blocked. Stage 4 (interactive worlds) needs arcprize.org; otherwise it
falls back to games we write ourselves.
