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

The same numbering as [ROADMAP.md](ROADMAP.md). A stage becomes the main line only once
the stage before it has passed every exit test on held-out problems, with no regressions.

| Stage | Conquest | Exit test, fixed in advance |
|---|---|---|
| **1. The scalable, unbreakable core** *(now)* | ①②③ made robust, expressive and fast; ARC-AGI as the battlefield | R1–R6, S1–S2, E1–E2, A2–A3 in [STAGE_1_PLAN.md](STAGE_1_PLAN.md) |
| **2. The real world through its eyes** | Eyes that generalise first; then real videos at scale: falling, swinging, bouncing, colliding, diffusing | Eyes: every failure-lab row ≥ 23/25 with no regressions. Then g, pendulum periods, restitution and diffusion from real footage within measured error; detection on par with lab tools |
| **3. Interactive worlds** *(new)* | ⑤ agency and ⑥ curiosity with a learned ④ world model: grid games with unknown rules and goals (like ARC-AGI-3) | Wins held-out games in close to the fewest actions; laws learned in one game cut the actions needed in later ones |
| **4. The reader** | Learning from the internet as checked evidence | Learns laws from open data it was never taught; catches ≥ 90% of planted false claims; reaches a target accuracy with ≥ 100× fewer bytes read than a fixed, named small language-model baseline on the same questions |
| **5. Language** | Words → sentences → conversation, all grounded | Understands and produces new sentences about its worlds; detects false statements; asks informative questions; human blind evaluation |
| **6. The body in 3D** | 3D simulated bodies, then tools | Solves new manipulation tasks by planning (a tower taller than any it has seen; using an object as a tool) |
| **7. Code, self and Engc** | General programs; its own source as a world; Engc and its twin | Correct programs on unseen specs; predicts its own modules; the Engc twin passes every exam identically |
| **8. Self-improvement** | Proposes changes to its own code and grammar, in a sandbox | Learning efficiency measurably up, zero regressions, every change human-approved; invents a primitive no one gave it |
| **9. The scientist** | New knowledge | A discovery in a field it was never taught, verified independently |
| **AGI** | Stages 1–7 together | The fixed battery: ARC-AGI-1, -2 and -3 on held-out sets; every stage's held-out exams; human blind tests; data efficiency against fixed baselines. Learns new skills from a few examples and some reading, across fields it was never trained on, at the level of a capable human learner |
| **ASI** | Stage 9 at scale | Consistently produces verified knowledge beyond the best human experts, under governance that grew with it |

**The safety track runs alongside the stages.** Governance is built *before* the stage
that needs it:
- **Before stage 4** (the first text written to deceive): exams and sandbox Ultron cannot
  modify, an audit log of belief changes, and the rule that untrusted text is only ever a
  claim, never an instruction.
- **Before stage 8**: human approval of self-changes, rollback and a kill switch.

**Corrections made after building Stage 1:**
- Library learning starts on the brain's own laws (on ARC it had nothing to compress:
  a recorded null result).
- Intuition v2 predicts law families and program pieces (v1 was a recorded null result).
- A per-puzzle MDL network is allowed as a second ARC engine. It is trained only on the
  puzzle and verified, and answers only when no symbolic program fits.
- Eyes moved to stage 2.
- Interactive worlds added as stage 3.
- A measurable reader baseline.
- The safety track moved earlier.

---

## 3. How we know we're winning

| Instrument | Measures | When |
|---|---|---|
| **Failure lab** (`python -m ultron stress`) | Breakpoints of every mechanism | After every change; breakpoints only move outward |
| **Held-out exams** | Understanding vs memorising | Every lesson |
| **Blind tests** | Written by examiners who never saw the code (humans wanted) | Every stage |
| **Public benchmarks** | ARC-AGI-1 and -2 first, ARC-AGI-3 in stage 3; others per stage. Score **and precision** (how many answers were right), on held-out sets, every evaluation run logged | Checkpoints only |
| **Competitions** | Entered only when our logged held-out score beats the best published score for that track (ARC Prize 2026: checked, not entered) | When the rule is met |
| **Efficiency** | Data and search per law, against baselines | Every stage |
| **Determinism** | A retrain is identical byte for byte | Every commit |
