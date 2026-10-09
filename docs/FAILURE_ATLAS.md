# The failure atlas

> Assume Ultron failed to become a general intelligence. Why?

This is a pre-mortem. Every way Ultron could fail is listed here, with how we provoke it
on purpose, what happens today, and how we fix it. The ones we can simulate are measured
by the [failure lab](../reports/failure_lab.md) (`python -m ultron stress`), which turns
one dial at a time until Ultron breaks.

Closing every known failure doesn't prove success: unknown failures remain. But every
failure we find and fix moves the frontier, and the lab keeps running so nothing quietly
breaks again. That is how we build it.

Status: 🔴 breaks today · 🟡 partly handled · 🟢 handled and tested · ⬜ not yet
measurable

## What the lab found (first run)

| Mechanism | Where it breaks today |
|---|---|
| Program search | Laws up to about 7 pieces. (a+1)(b+2)(a+b) is out of reach in budget. a³+b² took 916,000 candidates |
| Wrong records (programs) | Broke at 5% → **fixed**: laws with exceptions (MDL); keeps multiplication with 5 of 40 records corrupted and names exactly those 5 |
| Hidden causes, pure noise | ✅ never claims a false law |
| Few examples | ✅ 2 examples enough for a·b+a |
| Measurement laws, bell-curve noise | Broke at ±0.5% → **fixed**: robust acceptance; F = m·a found at ±20% |
| Measurement laws, outliers | Broke at 0% → **fixed**: F = m·a found with 20% badly wrong readings |
| Irrelevant measurements | Right law, but 6 irrelevant quantities take 312 s |
| Confounders | ❌ a meaningless law chosen, ambiguity not noticed |
| Tiny and huge numbers | ✅ |
| A changing world | ❌ notices, but ends with no law |
| Law shapes | ✅ settling, lines, quadratic (a new kind invented on the spot); ❌ oscillation, logistic, fractional powers |
| Eyes | ❌ over-specialised: 1/25 at double noise, 0/25 bigger things, 2/25 faint, 14/25 crowded |

Every ❌ is a work item in [Stage 1](STAGE_1_PLAN.md).

## 1. Search: the core can't scale

| Failure | How we provoke it | Status | Fix | Stage |
|---|---|---|---|---|
| **Combinatorial explosion.** Search is smallest-first and exhaustive, so cost grows exponentially with the size of a law | Lab: *program size*, with laws from `a+b` to `(a+1)(b+2)(a+b)` | see lab | A **neural guide** trained on its own past searches proposes programs; the checker verifies. **Library learning**: pieces of laws it found become new primitives, so big laws become small | A |
| Search time grows with data | Lab: *compute vs data* | see lab | Check candidates on a small sample first, the rest only for survivors. Hash outputs | A |
| Irrelevant measurements multiply the search | Lab: *irrelevant measurements* | see lab | Relevance screening (does changing it ever change the outcome?) before search. Experiments that vary one thing at a time | A |
| Its search heuristics don't improve with experience | ⬜ | 🔴 | The neural guide above. Measure: search steps per law fall as it learns | A |

## 2. Data that lies

| Failure | How we provoke it | Status | Fix | Stage |
|---|---|---|---|---|
| **Exact program search breaks on a single wrong record** | Lab: *wrong labels* | see lab | Tolerant fitting for programs: the shortest program that fits all but a few experiences wins, if the exceptions cost less to list than to explain (MDL with an exception list). Exceptions get re-checked by re-doing the experiment | B |
| Gross outliers in measurements | Lab: *outliers* | see lab | Robust fitting everywhere (median, trimming, RANSAC-style consensus), not just in the eyes | B |
| Noise beyond what it expects | Lab: *noise* | see lab | It estimates its own noise from repeats (it already does in Phase 3). Extend that to every instrument | B |
| **Internet claims that are false, stale or planted** | ⬜ planted false claims in stage C | 🔴 | Every claim has a source and a trust score per source. Claims are checked against its laws, other sources and experiment. Sources that were wrong lose trust | C |
| Text written to steer the reader (prompt injection) | ⬜ | 🔴 | What it reads is data, never instructions. The reader has no channel to act | C |

## 3. Causes vs coincidences

| Failure | How we provoke it | Status | Fix | Stage |
|---|---|---|---|---|
| **Confounders**: two things always move together, so it picks one arbitrarily | Lab: *confounders* | see lab | Notice ties: when two explanations fit equally, say so, and **design the experiment that separates them** (it already designs experiments for rival programs; extend that to quantities) | A |
| Hidden causes: the outcome depends on something unseen | Lab: *hidden causes and noise* | see lab | Refuse a law, and say "something I can't see matters". Then look for new things to measure | B |
| Correlation taken for causation in passive data (internet tables) | ⬜ | 🔴 | Separate "seen together" from "made to happen" (do-experiments). Laws learned only from passive data are marked as such | C |

## 4. What it can't even express

| Failure | How we provoke it | Status | Fix | Stage |
|---|---|---|---|---|
| **Laws outside its grammar** (oscillations, logistic growth, power laws with fractional exponents, differential equations) | Lab: *kinds of law* | see lab | Grow the grammar: the state of a thing (position *and* speed) as a vector, laws about change (Δ of a state = f(state)), so oscillation is "the change of speed opposes the position". Non-integer exponents through its fractional repeats | A |
| Probabilistic laws (diffusion, radioactive decay, genetics) | Real microscope film: it found Einstein's law, but I chose the statistic (spread) | 🟡 | Distributions as things: it should invent "spread" and "average" as summaries of many unpredictable things | B |
| Structured objects (lists, trees, graphs, recursion) | ⬜ | 🔴 | Types and recursion in the program language (needed for ARC and for code) | A, F |
| Its building blocks are designed by people | — | 🔴 | Library learning first. Then self-proposed primitives, accepted only if they shrink the description of everything it knows | G |

## 5. Senses

| Failure | How we provoke it | Status | Fix | Stage |
|---|---|---|---|---|
| Heavier noise, different sizes, faint or crowded things | Lab: *eyes* | see lab | Train on varied scenes; scale-space (look at several sizes); self-teaching on what lasts (works on the real microscope film: 81% → 86% of the scientists' particles found) | B |
| **Simulator to real world** | Real microscope film | 🟡 one real film | Many real videos (needs network access to video sites). Self-teaching on each | B |
| Clutter, 3D, occlusion, categories ("a cup") | ⬜ | 🔴 | Objects as things that move together (common fate), depth from motion; categories as concepts grounded by use | B, E |

## 6. Memory and compute

| Failure | How we provoke it | Status | Fix | Stage |
|---|---|---|---|---|
| It keeps every experience and re-checks them all | ⬜ grows with lessons | 🟡 | Consolidation: keep the laws plus the exceptions and a sample of experiences; forget the rest | A |
| Forgetting old skills when learning new ones | Real film: eyes kept 40/40 on old trays with replay | 🟢 for eyes | Replay for every learned component; old exams always re-run | all |
| Pure Python is slow | Lab timings | 🟡 | Hot paths in numpy or native code; the Engc twin | F |

## 7. Reasoning and learning dynamics

| Failure | How we provoke it | Status | Fix | Stage |
|---|---|---|---|---|
| The world changes under the same name | Lab: *a changing world* | see lab | Doubt when an established law fails; re-measure; keep the history | B |
| Occam's razor picks a simple wrong law when the truth is complex | ⬜ | 🟡 | More data shifts the balance automatically (MDL); plus held-out checks before trusting | A |
| Curiosity trapped by things it can never learn | Noisy TV and random walks (tested) | 🟢 | Learning progress, not error | — |
| Long chains of reasoning, planning, analogy | ⬜ | 🔴 | Planning with its world model (stage E); analogy as reusing a law's structure in a new field | E, H |
| Too few examples | Lab: *few examples* | see lab | Designing the most informative experiment, rather than waiting for examples | A |

## 8. Language

| Failure | How we provoke it | Status | Fix | Stage |
|---|---|---|---|---|
| ~40 grounded words; no grammar | ⬜ | 🔴 | Words by pointing, then composition (a word's meaning is a program), then reading | D |
| Ambiguity, metaphor, things it can't experience | ⬜ | 🔴 | Meaning grounded where possible, borrowed by analogy where not, and marked as borrowed | D |

## 9. Self-improvement and safety

| Failure | How we provoke it | Status | Fix | Stage |
|---|---|---|---|---|
| **Gaming its own exams** (improving the score, not the skill) | Planned red-team: a self-change that edits an exam must be caught | ⬜ | Exams live outside what it can modify; held-out exams it never sees; human approval of every change | G |
| A change that looks good and breaks something rare | ⬜ | ⬜ | Every exam and every blind test re-run; staged rollout; one-step rollback | G |
| Acting in the world with irreversible effects | ⬜ | ⬜ | Sandboxed bodies first; actions with real effects need human sign-off | E, G |
| Goals drifting as it grows | ⬜ | ⬜ | Goals are written down, versioned and reviewed by humans; it can propose changes to its goals, never make them | G |

## 10. Fooling ourselves

The quietest way to fail: believing we've succeeded.

| Failure | How we provoke it | Status | Fix |
|---|---|---|---|
| **We write the exams we pass** | Blind tests by outside examiners | 🟡 (examiners are the same underlying model) | Human blind tests; public benchmarks (ARC-AGI) with published scores |
| Tolerances tuned until tests pass | Reviews of each threshold change | 🟡 | Thresholds fixed *before* running; first-sight scores always reported |
| Test data leaking into training | ⬜ | 🟡 | Held-out sets are never loaded during training; checked by tests |
| Big claims ahead of evidence | — | — | A claim is made only with the test that backs it. The vision can be as big as we like; the evidence decides what we say happened |

## The order of attack

1. **Robustness of the core** (sections 2 and 3): tolerant program fitting, robust quantity
   fitting, ambiguity detection and separating experiments. These are cheap, measurable in
   the lab today, and every later stage depends on them.
2. **Scale** (section 1): library learning, then the neural guide. Measured on the lab's
   *program size* dial and then on ARC-AGI.
3. **Expressiveness** (section 4): state, change and structured objects.
4. **The real world** (sections 5 and 2): real videos, then reading the internet as claims.

After each fix the lab runs again, and the breakpoint must move.
