# Ultron master plan: the architecture of a general intelligence

**Goal: the first general intelligence built on understanding instead of volume, and then
superintelligence.** Ultron learns the way scientists and children do. It explains what
it sees with the shortest true account, invents the concepts it needs, tests everything
against the world, and reads the internet as evidence to be checked, not text to be copied.
So it needs a tiny fraction of the data today's models consume.

We dream as big as the goal and measure as hard as the goal demands. Every stage has exit
tests fixed in advance, run on problems Ultron has never seen, and the
[failure lab](FAILURE_ATLAS.md) attacks every mechanism until it breaks. The vision is
unlimited. The claims follow the evidence.

---

## 1. The architecture

```
                         ┌──────────────────────────────────────────────┐
                         │      GOVERNANCE & SAFETY (outside Ultron)     │
                         │  exams it can't touch · human approval of     │
                         │  self-changes · audit log · kill switch       │
                         └──────────────────────────────────────────────┘
                                             │ oversees
┌────────────────────────────────────────────┴───────────────────────────────────────────┐
│ ULTRON                                                                                  │
│                                                                                         │
│  ┌─────────────┐   ┌──────────────────────── THE CORE ─────────────────────────┐       │
│  │ SENSES      │   │                                                            │       │
│  │ retina →    │   │  ① EXPLANATION ENGINE   find the shortest account (MDL)   │       │
│  │ learned     │──▶│     typed program language · kinds of explanation ·       │       │
│  │ eyes →      │   │     laws with exceptions · uncertainty · rivals           │       │
│  │ objects,    │   │                    ▲ proposes        │ verifies            │       │
│  │ tracks,     │   │  ② INTUITION        neural guide trained on its own       │       │
│  │ measurements│   │     searches: proposes likely programs, never decides     │       │
│  └─────────────┘   │                    ▲                 │                     │       │
│  ┌─────────────┐   │  ③ LIBRARY          every confirmed law and reusable      │       │
│  │ READER      │   │     piece becomes a building block (library learning)     │       │
│  │ sources →   │──▶│                                                            │       │
│  │ claims →    │   │  ④ WORLD MODEL      concepts, laws, objects, provenance,  │       │
│  │ checked     │   │     trust, what is known and what isn't                   │       │
│  │ knowledge   │   └────────────────────────────────────────────────────────────┘      │
│  └─────────────┘            │ predicts / plans                ▲ learns                 │
│  ┌─────────────┐   ┌────────▼─────────────┐   ┌───────────────┴──────────────┐         │
│  │ LANGUAGE    │◀─▶│ ⑤ AGENCY              │──▶│ ⑥ CURIOSITY                   │         │
│  │ word = a    │   │ goals · planning with │   │ learning progress · the most │         │
│  │ grounded    │   │ its own laws · acting │   │ informative experiment ·     │         │
│  │ program     │   │ · correcting          │   │ what to read next            │         │
│  └─────────────┘   └──────────────────────┘   └──────────────────────────────┘         │
│                                                                                         │
│  ⑦ METACOGNITION  a model of itself: confidence per belief, its own failure lab,        │
│     its own code as a world to study; proposes improvements to itself (sandboxed)       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                 ▲ experiences                                   │ actions
        ┌────────┴─────────────────────────────────────────────▼────────┐
        │ WORLDS: simulators → real videos → the internet → 3D bodies →   │
        │ code (its own, Engc) → open science                             │
        └─────────────────────────────────────────────────────────────────┘
```

### The parts, and why each is there

| Part | What it is | What exists today | What it must become |
|---|---|---|---|
| **① Explanation engine** | Finds the shortest description that explains every experience: a program, a law, a kind | Program synthesis and invariant search with MDL; kinds of explanation; laws with exceptions (new) | One typed language for programs, quantities, sequences, grids and structures. Robust to noise and wrong data. Reports ties and uncertainty |
| **② Intuition** | A neural network that learns, from Ultron's own searches, which programs are likely. It proposes; the engine verifies | None | Cuts search by orders of magnitude. Never trusted without verification, so it can't hallucinate |
| **③ Library** | Confirmed laws become building blocks; recurring pieces of laws become new primitives | Confirmed laws are reused | Library learning: compressing what it knows into new primitives, so big laws become small |
| **④ World model** | Everything known, with where it came from and how much it's trusted | Laws, inventions, episodic memory | A concept graph with provenance, trust, exceptions and open questions; consolidation instead of storing everything |
| **⑤ Agency** | Goals, planning with its own laws, acting, correcting from what it sees | Reaching marks by running laws backwards | Multi-step planning, tools, 3D bodies, safe actions |
| **⑥ Curiosity** | Chooses what to learn next | Learning progress; designs separating experiments for programs | Information gain over everything: experiments, videos, pages to read |
| **⑦ Metacognition** | Knows what it knows; studies and improves itself | Confidence, doubt, the failure lab (run by us) | Runs its own failure lab; proposes changes to itself in a sandbox |
| **Senses** | Pixels → objects → measurements with uncertainty | Retina, learned CNN eyes, tracking, self-teaching; one real film | Real video at scale, 3D, categories |
| **Reader** | The internet as claims with sources, checked before believed | None | Tables, then text; trust per source; detects falsehoods and manipulation |
| **Language** | Words as grounded programs | About 40 grounded words | Grammar, reading, conversation |
| **Governance** | Oversight that Ultron cannot modify | Exams, blind tests | Sandbox, human approval, audit, rollback, kill switch |

### Design laws (these never change)

1. **Propose freely, verify strictly.** Intuition and reading can suggest anything; only
   verified explanations become beliefs.
2. **The shortest true account wins** (minimum description length), including the cost of
   its exceptions.
3. **Every belief carries its evidence**: where it came from, how well it predicts, and
   what would refute it.
4. **Act to learn.** When two explanations tie, design the experiment that separates them.
5. **Nothing is learned by hand-coding the answer.** The Trainer sets up worlds; Ultron
   finds the laws.
6. **Safety is outside the system.** What Ultron can change never includes its exams, its
   sandbox or its goals.

---

## 2. The campaign

| Stage | Conquest | Exit test, fixed in advance |
|---|---|---|
| **1. The scalable, unbreakable core** | ①②③ made robust and fast; ARC-AGI as the battlefield | See [STAGE_1_PLAN.md](STAGE_1_PLAN.md) |
| **2. The real world through its eyes** | Real videos at scale: falling, swinging, bouncing, colliding, diffusing | Recovers g, pendulum periods, restitution and diffusion from real footage within measured error; detection on par with lab tools |
| **3. The reader** | Learning from the internet as checked evidence | Learns laws from open data it was never taught; catches ≥ 90% of planted false claims; reaches a target accuracy with ≥ 100× less reading than a language-model baseline on the same questions |
| **4. Language** | Words → sentences → conversation, all grounded | Understands and produces new sentences about its worlds; detects false statements; asks informative questions; human blind evaluation |
| **5. The body** | 3D simulated bodies, then tools | Solves new manipulation tasks by planning (a tower taller than any it has seen; using an object as a tool) |
| **6. Code, self and Engc** | General programs; its own source as a world; Engc and its twin | Correct programs on unseen specs; predicts its own modules; the Engc twin passes every exam identically |
| **7. Self-improvement** | Proposes changes to its own code and grammar, in a sandbox | Learning efficiency measurably up, zero regressions, every change human-approved; invents a primitive no one gave it |
| **8. The scientist** | New knowledge | A discovery in a field it was never taught, verified independently |
| **AGI** | Stages 1–6 together | Learns new skills from a few examples and some reading, across fields it was never trained on, at the level of a capable human learner; public benchmarks plus human blind tests |
| **ASI** | Stage 8 at scale | Consistently produces verified knowledge beyond the best human experts, under governance that grew with it |

Stages overlap. Stage 2 can start while stage 1 runs, but stage 1 comes first because
everything rests on the core.

---

## 3. How we know we're winning

| Instrument | Measures | When |
|---|---|---|
| **Failure lab** (`python -m ultron stress`) | Breakpoints of every mechanism | After every change; breakpoints only move outward |
| **Held-out exams** | Understanding vs memorising | Every lesson |
| **Blind tests** | Written by examiners who never saw the code (humans wanted) | Every stage |
| **Public benchmarks** | ARC-AGI first; others per stage | Published scores |
| **Efficiency** | Data and search per law, against baselines | Every stage |
| **Determinism** | A retrain is identical byte for byte | Every commit |
