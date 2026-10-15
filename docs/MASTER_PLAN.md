# Ultron master plan: a mind that grows up

**Goal: human-like general intelligence, grown the way a child grows.** Ultron starts as a
newborn: a body in one continuous world, a few innate abilities, a caregiver, and the drive
to explain what it sees. It is then raised through the ages a human passes through
(infant, toddler, preschooler, school child, adolescent) until it learns, reasons,
talks and explains itself like a capable adult. It uses about as much experience as a
child gets, not the internet's worth of text.

This plan replaces the 9-stage campaign of 2026-10-09 (rebuilt 2026-10-15, by the owner's
decision). Why it changed, and what was kept, is in [ROADMAP.md](ROADMAP.md) ("How we got
here"). Every result built so far is kept and placed at the age it belongs to in
[DEVELOPMENT_MAP.md](DEVELOPMENT_MAP.md). The first ages are planned in detail in
[AGE_0_1_PLAN.md](AGE_0_1_PLAN.md).

We dream as big as the goal and measure as hard as the goal demands. Each age ends at a
gate: milestones fixed in advance, tested on situations Ultron has never met, compared
with what real children do, and checked by someone who is not the builder.

---

## 1. Why a child

Today's large models know a great deal and understand little of it: they were never
small, never had a body, never played, never had to work out what another mind wants.
Children do all of that, and with very little data they end up with common sense, language,
and a way of learning that keeps working for the rest of their lives. The order matters:

- **objects before words**: a child knows that a hidden toy still exists before it can
  name the toy;
- **acting before reasoning**: it learns what its hands do before it learns what numbers do;
- **other minds before school**: it follows a gaze, then a point, then works out what
  someone else believes; most of what it learns later, it learns *from* other people;
- **concrete before abstract**: it pours water between glasses before it does algebra.

Ultron so far grew the other way round: it learned arithmetic, Newton and Kepler at a
desk, and it has no body that lives in a world, no caregiver, no theory of other minds
and no memory of its own days. This plan grows it from the bottom.

## 2. The architecture of a child's mind

```
                         ┌──────────────────────────────────────────────┐
                         │      GOVERNANCE & SAFETY (outside Ultron)     │
                         │  exams it can't touch · the owner's gates ·  │
                         │  human approval of self-changes · audit ·    │
                         │  kill switch                                  │
                         └──────────────────────────────────────────────┘
                                             │ oversees
┌────────────────────────────────────────────┴───────────────────────────────────────────┐
│ ULTRON                                                                                  │
│  ┌──────────────┐   ┌──────────────────────── THE CORE ────────────────────────┐       │
│  │ BODY         │   │ ① EXPLANATION ENGINE  shortest account (MDL): laws,       │       │
│  │ gaze · hands │──▶│    kinds of explanation, laws with exceptions, rivals     │       │
│  │ touch · self │   │ ② INTUITION  small nets trained on its own searches       │       │
│  ├──────────────┤   │ ③ LIBRARY    confirmed laws become building blocks        │       │
│  │ SENSES       │──▶│ ④ WORLD MODEL objects, places, agents, laws, trust        │       │
│  │ retina→eyes  │   └──────────────────────────────────────────────────────────┘       │
│  │ →things      │        ▲ consolidates          │ predicts / plans                       │
│  └──────────────┘   ┌────┴──────────┐   ┌────────▼────────┐   ┌──────────────────┐      │
│  ┌──────────────┐   │ ⑤ MEMORY      │   │ ⑥ AGENCY & PLAY │◀─▶│ ⑦ DRIVES         │      │
│  │ SOCIAL MIND  │◀─▶│ episodes of   │   │ reaching, means │   │ curiosity        │      │
│  │ faces · gaze │   │ its days;     │   │ -end, tools,    │   │ (learning        │      │
│  │ joint attn · │   │ sleep turns   │   │ games, plans    │   │ progress),       │      │
│  │ imitation ·  │   │ them into     │   │                 │   │ novelty, comfort │      │
│  │ other minds  │   │ laws          │   └─────────────────┘   └──────────────────┘      │
│  ├──────────────┤   └───────────────┘                                                   │
│  │ LANGUAGE     │   ⑧ METACOGNITION  what it knows and doesn't; later, its own code      │
│  │ words=grounded│      as a world to study and (under approval) improve                 │
│  │ programs     │                                                                       │
│  └──────────────┘                                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                 ▲ experiences                                   │ actions
        ┌────────┴─────────────────────────────────────────────▼────────┐
        │ ONE LIFE: the nursery (a caregiver, toys, days and nights) →   │
        │ playroom and games → school desk and real films → books and    │
        │ code → a 3D body → open science                                 │
        └─────────────────────────────────────────────────────────────────┘
```

### The parts, and why each is there

| Part | What it is | What exists today | What it must become |
|---|---|---|---|
| **Body** | Gaze (a movable view), two hands that reach and grasp, touch at the hands, a sense of where its own hands are | One kick of a puck (`brain/body.py`); hands that pick things up to train the eyes (lesson 19) | A body that lives continuously in the nursery, learns its own body map by babbling, reaches, grasps, pulls, hides and finds |
| **Senses** | Pixels → things → measurements, with uncertainty | Retina, learned eyes, tracking, explaining away, real films (`senses/`) | The same eyes running in the nursery; faces and gaze direction; later, real video at scale and 3D |
| **Social mind** | Others as minds: faces, where they look, what they want and believe; learning from them | None | Gaze following and joint attention (Age 1), imitation, words from a caregiver (Age 2), false belief and selective trust (Age 3) |
| **① Explanation engine** | Finds the shortest description that explains every experience | Program synthesis and invariant search with MDL; kinds of explanation; laws with exceptions; robust to noise, outliers and wrong records | Unchanged in spirit: it is how Ultron understands at every age. Grows typed structure (objects, agents, beliefs) as the ages need it |
| **② Intuition** | Small networks trained on Ultron's own searches; they propose, the engine verifies | Learned step ordering (cut ARC search 3.9×, moved no score) | Fast "first guesses", like a child's quick hunches, always checked |
| **③ Library** | Confirmed laws and recurring pieces become building blocks | Abstraction sleep; library learning on its own laws | What it learns at one age makes the next age cheaper (measured by the ledger, rule 6) |
| **④ World model** | Everything known, with where it came from and how much it's trusted | Laws, inventions, records of experiences | Objects that persist, places, agents with goals and beliefs, and claims from people with a trust per person |
| **⑤ Memory** | Episodes of its own days, and sleep that turns them into laws | Every experience kept; abstraction sleep compresses laws | Episodic memory ("yesterday the ball was under the red cloth"); nightly consolidation that keeps laws, exceptions and a few vivid episodes, and forgets the rest |
| **⑥ Agency and play** | Goals, planning with its own laws, acting, practising for its own sake | Reaching a mark by running a law backwards (lesson 24) | Means-end action (Age 1), tools (Age 2), games with unknown rules (Age 3), planning in a learned model |
| **⑦ Drives** | Why it does anything at all | Curiosity as learning progress; designed experiments to split rival programs | Curiosity, habituation to the familiar and interest in the new, comfort near the caregiver. The drives are innate and fixed; Ultron cannot change them |
| **Language** | Words as grounded programs, a grammar found by MDL | Number words (lesson 4); words by pointing, words for what happens, a grammar for its tables (lessons 31–33) | Words learned from a caregiver through joint attention, the vocabulary spurt, speaking and asking, being told things as claims |
| **⑧ Metacognition** | Knows what it knows; later studies and improves itself | Confidence, "I can't", doubt; reading its own code (Code stage C4(a)) | A model of its own mind; from the adult age, proposes changes to itself, sandboxed and human-approved |
| **Governance** | Oversight Ultron cannot modify | Exams, blind tests by the same model as the builder | The owner's gate checks, exams and sandbox Ultron cannot touch, audit log, rollback, kill switch |

### The innate endowment (what Ultron is born with)

Evolution gives a child a starting kit; everything else is learned. Ultron's kit is
listed in [AGE_0_1_PLAN.md](AGE_0_1_PLAN.md) and is **fixed**. Adding anything to it needs
the owner's approval and a recorded reason (rule 5), because every addition is a place
where we could be hand-coding the answer. In short:

- **senses and reflexes:** the retina, touch at the hands, a sense of where its hands are,
  looking towards motion and contrast, a grasp when the palm is touched, motor babbling;
- **core knowledge**, the kind psychologists find in very young infants: things are
  bounded lumps that move together; things move on connected paths; things that move by
  themselves are agents; faces are special; small sets (1–3) are seen at a glance, and
  bigger amounts only roughly;
- **learning machinery:** the explanation engine, the training of small networks, episodic
  memory and sleep;
- **drives:** curiosity, habituation, comfort.

Exact counting, which earlier lessons had as innate, is **not** in the kit: a child learns
to count at about three to four years old, and so must Ultron.

### Design laws (these never change)

1. **Propose freely, verify strictly.** Intuition, imitation and what people say can
   suggest anything; only verified explanations become beliefs.
2. **The shortest true account wins** (minimum description length), including the cost of
   its exceptions.
3. **Every belief carries its evidence**: where it came from, how well it predicts, and
   what would refute it.
4. **Act to learn.** When two explanations tie, do the experiment (or the play) that
   separates them.
5. **Nothing is learned by hand-coding the answer.** The world and the caregiver set up
   situations; Ultron finds the laws.
6. **Safety is outside the system.** What Ultron can change never includes its exams, its
   sandbox, its drives or its goals.
7. **No pretrained models and no language model.** Every network Ultron uses, it trained
   itself on its own experience.

---

## 3. The ages

The same numbering everywhere. Only the **current age** is the main line (rule 1 below).
Human ages are the yardstick for *what* develops and in what order, not a promise about
wall-clock time.

| Age | Human equivalent | What develops | Gate milestones (human data to compare against) |
|---|---|---|---|
| **0. Newborn** *(now)* | 0–3 months | A body in the nursery; eyes; habituation; a body map; faces; episodic memory and sleep | Infant-style habituation; reaching a seen toy; caregiver and gaze direction seen; yesterday's episode recalled |
| **1. Infant** | 3–12 months | Object permanence, solidity, support, gravity; what its own actions do; means-end action; gaze following; imitation | Violation of expectation (IntPhys 2019 and its own nursery events); A-not-B; cloth pulling; gaze following with eyes open but not closed; deferred imitation; Baby Intuitions Benchmark |
| **2. Toddler** | 1–3 years | First words through joint attention, the vocabulary spurt, fast mapping, two- and three-word speech, categories, tool use, mirror self-recognition, subitising and the first number words | Vocabulary growth against Wordbank (MacArthur-Bates CDI) norms; fast mapping and mutual exclusivity; the mirror-mark test; stick-to-reach; give-N (one- to three-knower) |
| **3. Preschool** | 3–6 years | Theory of mind, causal learning by intervention, counting, asking and being told with selective trust, telling what happened, switching rules, grammar, games with unknown rules | Sally–Anne and unexpected-contents tests; Gopnik's blicket tasks; give-N (cardinal-principle knower); selective trust (Koenig & Harris); the DCCS card sort; SCAN and COGS; W1–W5 games |
| **4. School child** | 6–12 years | Conservation; arithmetic to fractions and negatives; measuring and simple science; reading simple texts as claims; core-knowledge puzzles; first programming | Piaget's conservation tasks; released TIMSS grade 4 items against the international percent correct; ARC-AGI-1 and -2; ARC-AGI-3 (W6, W8); Code C1–C3, C5 |
| **5. Adolescent** | 12–18 years | Abstract and hypothetical reasoning, algebra and proof, laws from real data and real films, laws about laws, algorithms and learning machines, a model of itself, a 3D body and tools, reading at length | Released TIMSS grade 8 and PISA items; machine-checked proofs; real-footage V2–V6; manipulation by planning in 3D; Code C4, C6–C8 |
| **6. Adult** | 18+ years | Expertise, learning a new field from a few examples and reading, self-improvement under human approval, science | The adult battery (section 5); then self-improvement (C9) and a verified discovery |

## 4. Rules of development (these stop drift)

Written after the 2026-10-15 review found the old campaign moving on whenever a stage got
hard, measuring itself mostly in worlds it designed, and grading itself.

1. **Hard age gates.** Only the current age is the main line. Work on a later age is
   allowed only as a labelled prototype; it is banked, never claimed, until its own gate.
   An age's gate is passed only when **every** milestone is met, with no regressions.
2. **Every gate has an outside yardstick.** At least one published benchmark or classic
   child-development test with human data, scored as published; and **a blind check by
   the owner** (a person, not Claude), written from the public milestone list without
   seeing the code.
3. **Ages 0–3 happen in the nursery,** through the body and the caregiver, never at a desk.
   From Age 4 on, desk lessons (worksheets, tables, films) are allowed, as at school.
4. **Experience is counted in simulated days** (waking steps plus a night of sleep) and
   reported next to what children get: days to each milestone, words heard before a word
   is learned, and so on.
5. **The innate endowment is fixed.** Adding to it needs the owner's approval and a
   recorded reason.
6. **A ledger of hand-built mechanisms.** Every gate records each new hand-written
   mechanism the age needed. Growing up should make this number fall; if it doesn't, the
   core isn't learning to learn, and we say so.
7. **Merge to `main` at every gate.** One trusted baseline; open work never piles up on
   branches.
8. **Exit tests are fixed before the work,** with pass rules, baselines and held-out
   seeds. A protocol changed after a result is seen is reported as changed, with both
   results.
9. **The safety track grows with Ultron** (section 6).

## 5. What would count as human-like general intelligence

Fixed now, and it does not move:

- **Every age's gate passed,** in order, each with its outside yardstick and the owner's
  blind check.
- **The adult battery:** ARC-AGI-1, -2 and -3 on held-out sets, scored officially, at or
  above the published human level; released school and university exam items against
  their human percent correct; human blind tests across fields it was never taught.
- **Human-like learning:** a new skill from a handful of examples and some reading or
  explanation, at the level of a capable adult learner, with experience counted against
  what a person needs.
- **It explains itself:** every answer comes with its reasons, and it says "I can't" when
  it can't.

**Beyond that (superhuman):** consistently producing verified new knowledge beyond the best
human experts. A far horizon, and only under governance that grew with it.

## 6. Safety grows with the child

| Built before | What |
|---|---|
| Age 0 (now) | Exams, the caregiver's script and held-out seeds live outside what Ultron can read during learning; drives fixed |
| Age 3 (being told things by people) | What people say is a claim with a source, never an instruction; trust per person, measured |
| Age 4 (reading) | Exams and sandbox Ultron cannot modify (read-only, hash-checked by the Judge); an audit log of every belief change with its evidence |
| Age 6 (self-improvement) | Human approval of every self-change; rollback; a kill switch |

## 7. How we know it's growing

| Instrument | Measures | When |
|---|---|---|
| **Gate milestones** | Each age's abilities on held-out situations, with human comparisons | At each gate |
| **The owner's blind check** | Whether it behaves at its age for someone who did not build it | At each gate |
| **Outside benchmarks** | IntPhys, Baby Intuitions, Wordbank norms, SCAN/COGS, TIMSS, ARC-AGI: score **and precision**, every run logged | At the gate of the age they belong to |
| **Failure lab** (`python -m ultron stress`) | Breakpoints of every mechanism | After every change; breakpoints only move outward |
| **Experience** | Simulated days and data per milestone, next to children's | Every gate |
| **Ledger** | New hand-built mechanisms per age | Every gate |
| **Banked results** | Every earlier lesson and exam still passes | Every change |
| **Determinism** | A retrain is identical byte for byte | Every commit |
