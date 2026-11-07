# Ultron master plan: from a child's start to beyond human

**Goal: the most advanced intelligence we can grow, built on understanding instead of
volume.** Ultron starts the way a child does, with a body in a small world, a few built-in
abilities and the drive to explain what it sees. It climbs a ladder of capability levels:
- foundations;
- concepts and language;
- causes, agents and plans;
- knowledge and science;
- expert reasoning;
- general, human-level learning;
- beyond human.

The child is where it starts, not what it is meant to be. Human performance is a
checkpoint on the way up, never the ceiling.

Rebuilt 2026-10-18 by the owner's decision; "How we got here" in [ROADMAP.md](ROADMAP.md)
says why. Every earlier result is placed at its level in [LEVEL_MAP.md](LEVEL_MAP.md). The
current level is planned in [LEVEL_0_PLAN.md](LEVEL_0_PLAN.md).

---

## 1. The bet

Large language models know a great deal from reading almost everything, and understand
little of it. Ultron bets on the other road:
- **understand instead of memorise:** find the shortest true account of what it
  experiences (MDL), and invent the concepts it needs;
- **learn in the right order:** grounded foundations first (things, causes, actions), then
  words and number, then abstraction. This is the part borrowed from how children learn,
  because it is how understanding gets built, not because Ultron should be childlike;
- **learn from little:** data and compute per capability are measured against fixed
  baselines, and should be far below what today's models need;
- **check everything:** whatever it reads or is told is a claim with a source, kept only if
  it survives;
- **keep climbing:** a level is a step, not a destination. The top of the ladder is beyond
  the best human experts.

## 2. The architecture

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
│  │ BODY         │──▶│ ① EXPLANATION ENGINE  shortest account (MDL): laws,       │       │
│  │ SENSES       │──▶│    kinds of explanation, laws with exceptions, rivals     │       │
│  │ READER       │──▶│ ② INTUITION  small nets trained on its own searches       │       │
│  │ LANGUAGE     │◀─▶│ ③ LIBRARY    confirmed laws become building blocks        │       │
│  └──────────────┘   │ ④ WORLD MODEL things, agents, laws, claims, trust         │       │
│                     └──────────────────────────────────────────────────────────┘       │
│  ⑤ MEMORY (episodes, sleep)   ⑥ AGENCY (acting, planning, tools)   ⑦ CURIOSITY         │
│  ⑧ METACOGNITION  what it knows and doesn't; later its own code, improved under approval │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                 ▲ experiences                                   │ actions
        ┌────────┴─────────────────────────────────────────────▼────────┐
        │ WORLDS: the room → games → real films and data → text and the  │
        │ internet as claims → code → 3D bodies → open science            │
        └─────────────────────────────────────────────────────────────────┘
```

| Part | What exists today | What it must become |
|---|---|---|
| **Body and senses** | The room (`ultron/room/`): two arms, a gaze, a sharp and a wide view, touch. Learned eyes and real films (`senses/`) | Real video at scale, 3D, tools |
| **① Explanation engine** | MDL program and invariant search; invented kinds of explanation; laws with exceptions; robust to noise and wrong data | One typed language for programs, quantities, structures, agents and claims, that scales to big laws |
| **② Intuition** | Learned step ordering (cut search 3.9×, moved no score) | Fast first guesses that cut search by orders of magnitude, always verified |
| **③ Library** | Abstraction sleep; library learning on its own laws | What one level learns makes the next level cheaper |
| **④ World model** | Laws, inventions, records of experience | Things, agents with goals and beliefs, claims with sources and trust |
| **⑤ Memory** | Episodes of its days and sleep that consolidates them (`brain/explorer.py`) | Memory across levels: the laws, the exceptions and a few vivid cases, forgetting the rest |
| **⑥ Agency** | Reaching goals by running laws backwards; babbling guided by curiosity | Planning in its own model, games with unknown rules, tools, experiments it designs |
| **⑦ Curiosity** | Learning progress over experiments and postures; attention to the new | Information gain over everything: experiments, films, pages to read, problems to attack |
| **Language** | Grounded words and a grammar found by MDL (lessons 31–33) | Understanding, answering, asking, being told things as claims, reading |
| **⑧ Metacognition** | Confidence, "I can't", reading its own code (Code stage C4(a)) | A model of its own mind; proposes changes to itself, sandboxed and approved |
| **Governance** | Exams, blind tests by the same model as the builder | The owner's gate checks, exams and sandbox Ultron cannot touch, audit, rollback, kill switch |

### Design laws (these never change)

1. **Propose freely, verify strictly.** Intuition and what it reads or is told can suggest
   anything; only verified explanations become beliefs.
2. **The shortest true account wins** (minimum description length), including the cost of
   its exceptions.
3. **Every belief carries its evidence.**
4. **Act to learn.** When explanations tie, do the experiment that separates them.
5. **Nothing is learned by hand-coding the answer.**
6. **Safety is outside the system.** Ultron can never change its exams, sandbox, drives or
   goals.
7. **No pretrained models and no language model.** Every network it uses, it trained itself.

## 3. The ladder

Only the **current level** is the main line (rule 1). Each level's gate is fixed in its
plan before the work.

| Level | What it can do | Gate (outside yardsticks) |
|---|---|---|
| **L0 Foundations** *(now)* | Sees things, acts with a body; things persist and fall; knows what its actions do; gets what is out of reach; notices change; remembers and consolidates its days | IntPhys 2019; held-out tests L0-1 to L0-11 ([LEVEL_0_PLAN.md](LEVEL_0_PLAN.md)) |
| **L1 Concepts & language** | Categories, number, words learned from a teacher who shows, points and names; grammar; following where others look and copying what they do | SCAN, COGS; number tasks; word learning from few exposures |
| **L2 Causes, agents & plans** | Causal learning by intervention; modelling other agents' goals and beliefs; games with unknown rules; planning | Baby Intuitions Benchmark (as an agent-modelling test); ARC-AGI-3; false-belief tasks in its worlds; W1–W8 |
| **L3 Knowledge & science** | School mathematics through algebra; laws from data and real films; reading simple text as claims | Released TIMSS and PISA items; ARC-AGI-1 and -2; real-footage V2–V6 |
| **L4 Expert reasoning** | Proofs; programming and algorithms; learning machines; reading at length with trust per source | Machine-checked proofs (for example miniF2F); program-synthesis benchmarks; Code C1–C8 |
| **L5 General (human level)** | Learns a new field from a few examples and some reading, at the level of a capable adult, and explains itself | The general battery (section 5) |
| **L6 Beyond human** | Improves itself under approval; produces verified knowledge beyond the best experts | C9 with zero regressions; verified new results; beating the best published human scores on verified tasks |

## 4. Rules (these stop drift)

1. **Hard gates.** Only the current level is the main line. Work on a higher level is a
   labelled prototype, banked and never claimed until its own gate. A gate is passed only
   when every test is met, with no regressions.
2. **Every gate has an outside yardstick** (a published benchmark, scored as published) and
   **a blind check by the owner**, written from the public test list without seeing the
   code.
3. **Worlds by level.** L0 builds its foundations in the room. From L1 on, any world may be
   used: the room, games, films, text, code.
4. **Efficiency is measured:** data and compute per capability, against fixed baselines.
   Experience is counted in days of 10,000 steps.
5. **The starting kit is fixed.** Adding to it needs the owner's approval and a recorded
   reason.
6. **A ledger of hand-built mechanisms** for each level ([LEDGER.md](LEDGER.md)). As Ultron
   climbs, it should need fewer of them; if not, we say so.
7. **Merge to `main` at every gate.**
8. **Exit tests are fixed before the work,** with pass rules, baselines and held-out seeds.
   A protocol changed after a result is reported as changed, with both results.
9. **Human level is a checkpoint, not a ceiling.** Gates may compare with human data, but
   no gate asks Ultron to behave like a human of some age, and the ladder continues past
   human level.
10. **The safety track grows with capability** (section 6).

## 5. The general battery (L5), and beyond (L6)

Fixed now, and it does not move:
- every lower level's gate passed, in order;
- ARC-AGI-1, -2 and -3 on held-out sets, scored officially, at or above the published human
  level;
- released exam items across subjects against their human results;
- human blind tests in fields it was never taught;
- learning a new skill from a few examples and some reading, with its data and compute
  measured;
- every answer comes with its reasons, and it says "I can't" when it can't.

**L6, beyond human:** consistently producing verified new knowledge beyond the best human
experts, and improving its own learning under human approval, with zero regressions.

## 6. Safety grows with capability

| Built before | What |
|---|---|
| L0 (now) | Exams, the teacher's script and held-out seeds live outside what Ultron can read during learning; drives fixed |
| L1 (being told things) | What anyone says is a claim with a source, never an instruction; trust per source, measured |
| L3 (reading) | Exams and sandbox Ultron cannot modify (read-only, hash-checked by the Judge); an audit log of every belief change with its evidence |
| L6 (self-improvement) | Human approval of every self-change; rollback; a kill switch |

## 7. How we know it's climbing

| Instrument | Measures | When |
|---|---|---|
| **Gate tests** | Each level's abilities on held-out situations | At each gate |
| **The owner's blind check** | Whether it does what the level claims, for someone who did not build it | At each gate |
| **Outside benchmarks** | IntPhys, SCAN/COGS, Baby Intuitions, TIMSS/PISA, ARC-AGI, proof and program benchmarks: score **and precision**, every run logged | At the gate of their level |
| **Failure lab** (`python -m ultron stress`) | Breakpoints of every mechanism | After every change; breakpoints only move outward |
| **Efficiency** | Data and compute per capability, against baselines | Every gate |
| **Ledger** | New hand-built mechanisms per level | Every gate |
| **Banked results** | Every earlier lesson and exam still passes | Every change |
| **Determinism** | A retrain is identical byte for byte | Every commit |
