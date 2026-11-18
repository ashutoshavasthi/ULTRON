# The scoreboard

One row per run of `python -m ultron score` (see [docs/PLAN.md](../docs/PLAN.md)). Each run is one more round of the learning loop.
**Held out**: tasks it never learns from, without and with the words it has grown; right (wrong) answers. **Gain**: held-out net (right - wrong) with what it grew minus without (and the change in net from the last round). **ARC-1 training**: the main solver, official scoring, with precision (right / answered). **Lessons**: exams of lessons 0-33 the saved brain still passes. **Learned words**: the last run of `python -m ultron words g0` ([docs/MECHANISM.md](../docs/MECHANISM.md)); a new primitive is a learned word that no program of hand-written words imitates.

| When | Commit | Run | Round | Held out: without | with its words | Gain | Words | ARC-1 training | Lessons | Learned words |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-14 15:25 | `43dc24d` | quick (60 held out) | 1 | 7 (0) | 7 (0) | +0 (+0) | 0 | 50.0% of 40 (20/22 right) | skipped | G0: 3 of 5 hidden families relearned, 3 new primitives (single words exact 88%) |
| 2026-11-18 05:43 | `e3f9d74` | quick (60 held out) | 2 | 7 (0) | 6 (0) | -1 (-1) | 0 | 50.0% of 40 (20/22 right) | skipped | G0: 3 of 5 hidden families relearned, 3 new primitives (single words exact 88%) |
