# Ultron roadmap: toward general intelligence

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
| 3+. The real world (in progress) | A real microscope film from the internet: Einstein's law of diffusion measured from raw pixels, matching the scientists' own tool (1.63 vs 1.65 µm²/s) | Scripts work; lesson 26 not yet in the curriculum |

Blind tests by examiners who never saw the code scored 55/60, 54/60 and 45/50 on first
sight. The examiners were the same underlying model as the trainer, so a human's blind
test still counts for more.

## The road ahead

Each stage targets one of the honest gaps between today's Ultron and general intelligence.
The order puts the biggest risk first: if the core can't scale, nothing else matters.

| Stage | The gap it closes | What gets built | Exit test (could fail) |
|---|---|---|---|
| **A. A mind that scales** | Search is exponential: Ultron finds small laws, not big programs | A neural network trained on Ultron's *own* past searches proposes programs, and Ultron's checker verifies them. Successful pieces become reusable library parts (library learning) | Solves law-discovery problems **10× larger** than today with less search. On **ARC-AGI** (public abstract-reasoning puzzles built to measure few-shot generalisation), a public score compared fairly with published systems |
| **B. The real world through its eyes** | It has seen one real film | Finish lesson 26 (the microscope film). Then many real videos: falling objects, pendulums, bouncing balls, rolling balls | Rediscovers g, pendulum periods and bounce losses from **real footage**, matching measured values within stated error |
| **C. Reading the internet like a scientist** | It knows only what it experienced | A reader that takes in open data and text as **claims with sources**: tables first (open scientific datasets), then plain text. Each claim is checked against its laws, other sources and experiment. Reading is driven by curiosity: it reads what it most needs to learn | From open sources, it extracts laws it was never taught and **predicts held-out data**. It catches planted false claims. It reaches a target accuracy with **far less reading** than a language-model baseline, and we measure how much less |
| **D. Language** | It knows about 40 grounded words | Words by pointing, then grammar, then conversation, all grounded in concepts it already has. Reading from stage C grows its vocabulary | Understands new sentences about its world, answers questions, detects false statements, asks good questions |
| **E. A body and goals** | One action (a kick), in 2D | A 3D physics simulator (MuJoCo or PyBullet), goals, planning with its own world model, causal experiments | Solves new tasks by planning: a taller tower than it has ever seen, using an object as a tool |
| **F. Code, itself, and Engc** | It can't write real programs | Its program language grows into a general one. It studies its own Python source as a world. It learns [Engc-V1](https://github.com/ashutoshavasthi/Engc-V1) the way it learned arithmetic, and writes its twin in Engc | Correct programs for unseen specs, checked by running them. It predicts its own modules' behaviour. Its Engc twin passes every exam with identical answers |
| **G. Self-improvement, safely** | Its building blocks are still designed by people | Ultron proposes changes to its own code and its own grammar of explanations. Each runs in a sandbox, is kept only if every exam still passes and learning gets measurably better, can always be rolled back, and **needs a human to approve it** | Measurably better at *learning* (less data and less search per law) with zero regressions. It invents a building block that wasn't given to it, and uses it |
| **H. A scientist** | Everything it knows, someone knew before | Cross-domain analogy, its own experiment design, reading real literature as claims, deep mastery of one field (for example, mathematics with machine-checked proofs) | **Discovers something new** in a field it was not taught, verified independently |

## What would count as AGI, and ASI

Claims like these have to be testable, so we fix the bar in advance.

- **AGI (our working definition):** across fields it was never trained on, Ultron learns a
  new skill from a handful of examples and some reading, at the level of a capable human
  learner. It does this on public benchmarks and blind tests written by people who never saw
  its code, and it explains its answers. Stages A–F are the parts of that.
- **ASI:** consistently beyond the best human experts at producing *verified* new knowledge
  (stage H at scale). This is a far horizon. It also needs a level of safety and oversight
  that has to be built before the capability, not after.

## Honest difficulty

- **Stages A–C** are where the bet gets tested. Each is hard but concrete, and each could
  fail in a way we would learn from.
- **Stages D–F** are open research problems. The pieces exist but have never been combined
  well.
- **Stages G–H** are unsolved in general. Nobody, including us, can promise them.

## Next steps

1. **Finish lesson 26** (the real microscope film): run it, test it, add it to the
   curriculum, write the verdict.
2. **Start stage A with ARC-AGI.** Load the public tasks, run Ultron's synthesis core on them
   unchanged to get a baseline, then build the neural guide that proposes programs and the
   checker that verifies them.
3. **Start stage C with open data.** Teach Ultron to read open scientific data tables as
   claims with sources, and measure how much it learns per byte it reads.

Network note: this environment can reach GitHub and the Python Package Index. Wikimedia,
YouTube and archive.org are blocked. They can be allowed under the cloud environment's
**Edit → Network access** settings, and stages B and C will need them.
