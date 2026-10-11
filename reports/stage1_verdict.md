# Stage 1 verdict: the scalable core

*Written 2026-10-11. Criteria were fixed before the work started (`docs/STAGE_1_PLAN.md`).*

| Criterion | Result | Verdict |
|---|---|---|
| R1 wrong records (20%) | right law found | ✅ |
| R2 noise up to ±10%, estimated by itself | measures its own noise from repeated trials; holds to ±20% | ✅ |
| R3 outliers (20%) | right law found | ✅ |
| R4 10 irrelevant quantities, < 10 s | 0.04 s | ✅ |
| R5 every tie reported; separating experiment designed | yes; one designed experiment gave F = m·a from a wrong start | ✅ |
| R6 zero false laws on 100 datasets of noise or hidden causes | 0 false laws in every audit | ✅ |
| S1 laws of size 12 within 60 s | laws of 15–16 pieces in about 10 s, via abstraction sleep | ✅ |
| S2 search per law falls ≥ 10× after library learning and intuition | combined > 1,400×; intuition alone 1.0× / 0.7× (brain), 3.9× (ARC) | 🟡 combined only |
| E1 oscillation, quadratic motion, fractional powers | explained and predicted for new objects (lesson 27) | ✅ |
| E2 lists | folds with its own addition; 120/120 on 3× longer rows (lesson 28) | ✅ |
| A0 ARC harness and baseline | done | ✅ |
| A1 ≥ 10% ARC-AGI-1 evaluation | **12.75%** (logged, C4; 51 of 63 answers right) | ✅ |
| A2 ≥ 25% | not reached | ❌ |
| A3 ≥ 40% | not reached | ❌ |

## What the ARC work established (and why it stops here)

Measured, in order:
- **Hand-written law families** raised evaluation from 3.75% to 12.75%, then hit
  diminishing returns.
- **A learned intuition** ranked the right step first and cut search 3.9×, but did not
  raise the score: what limits Ultron is what it can express, not search order.
- **Library learning on the 38 big operations** grew 2 blocks and gained nothing on
  unseen tasks.
- **A language of 40 small composable steps** solves 67 training tasks on its own. A
  leave-one-out check took the fallback's wrong answers to zero. Ultron's own steps,
  grown from that language, reach 2–6 new unseen tasks per half with no wrong answers,
  but did not meet the adoption bar.

The training score went from 30.8% to 35.4% (141 solved, 13 wrong) over this phase.
Gains reached the evaluation split at about one third, and the last several mechanisms
added little or nothing to the default solver.

## Decision

A2 and A3 are **not met**. The roadmap's rule is that a stage becomes the main line only
once the stage before it has passed every exit test. On 2026-10-11 the project owner
decided to **move to Stage 2 now** because further ARC work is not paying off. That
decision is recorded here and in the roadmap as a correction.

ARC returns in two places:
- **Stage 3 (interactive worlds),** with ARC-AGI-3-style games;
- **the AGI battery,** where ARC-AGI-1, -2 and -3 remain fixed tests.

Everything built stays in the repository, and every measurement stays recorded:
`docs/ARC_REPORT.md`, `docs/STAGE_1_PLAN.md`, `reports/arc_*.json`.
