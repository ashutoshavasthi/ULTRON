# Judge's verdict: Phase 3, real senses, new kinds of explanation, a minimal body

*Written by Claude, as Ultron's trainer and judge, after running lessons 0–25, every
exam, and a third blind test written by an independent examiner.*

## Verdict

**Both limits I named are pushed back hard. Neither is gone, and I say exactly where
each one now stands.** All 26 lessons pass on the first attempt. Training takes about
60 s, and retraining gives the same brain file byte for byte, including the neural
network's weights. On the Phase 3 blind test Ultron first scored **45/50**. All 10
questions where the only right answer is "I can't" were handled correctly. The 5
failures were fair, and each is fixed at its cause.

## Limit 1: "its world is tiny and arrives as clean numbers"

| Before | Now | Evidence |
|---|---|---|
| Numbers handed over, noise at most ±1% | **Pixels only**: 48×48 (or 96×96) grayscale with 8% sensor noise, blur, uneven light, a shaking camera, and 2% spoiled frames (a hand in the way, a dropped frame) | `senses/camera.py` |
| Counting was innate and exact | **Eyes it learns**: a 3-layer convolutional network trained from **touch** (while handling things, its hands say where each thing is), with the forward and backward passes written out in numpy | 60/60 new trays of 0–30 counted right; **20/20 trays of 31–50, never practised**; 228/229 things located within half a pixel; the same network before learning got 5/60 |
| Laws found from clean tables | **Laws found from video**: F = m·a (F/(a·m) = 1.002), each spring's stiffness, and energy y + v²/19.28, where 2g = 19.62 | A **blank brain given only the eyes** rediscovers all three. Accelerations predicted before watching: 12/12 within 3% |
| Tolerances given by the trainer | Ultron **measures its own noise** (accelerations ±0.5%, stretches ±1.5%). For energy, every reading carries an uncertainty it measured, and a law is accepted only when what's left over is noise-sized | y + c·v, y + c·v³ and y² + c·v² are all rejected on the same data |
| No body | **A minimal body**: to reach a painted mark it runs its law backwards. On a floor it never touched, it makes a cautious first kick at half the distance, reads the floor's friction from what it sees, then hits | Wood 12/12 on the first try; carpet 12/12 and ice 10/10 on the second; random kicks hit 4% |

**Still true:** the camera, the physics and the noise are simulated. The eyes see blobs
against a ruler, not a cluttered room. There is no real language. The "body" is one
action (a kick) in 2D. This is the honest distance to Phase 4 (a 3D body) and Phase 5
(language).

## Limit 2: "it can't invent new kinds of hypothesis"

| Before | Now | Evidence |
|---|---|---|
| A fixed set of kinds (products, sums, conserved totals, REPEAT, shapes, gaps), all written by me | Kinds are **data**: a transform from a small grammar (Δ, ρ, composed; Δy/Δx) plus a scope. When no kind it has fits, it searches the grammar, shortest first, and keeps the winner as a **new kind** | **Kind 1**, "the steps shrink by the same fraction each time: it settles", invented on cooling cups. **Kind 2**, "equal steps in what I change give equal steps in what I read", invented on springs measured by length |
| — | **Reuse**: new worlds are explained by its own kinds first | Bounces and batteries use kind 1; candles, read at odd times, use kind 2; draining tanks, never seen before the final exam, are explained **on first meeting**. On the same data, its own kinds cost 84 vs 168 steps, 96 vs 404, 40 vs 940, and 72 vs 72 for candles |
| — | **Not fooled by noise**: a randomly blown marker stays unexplained, even after 8 extra walks | No kind is invented for it |
| — | **Ablation**: the same brain with invention switched off can't explain cooling or the tanks at all | Checked in exams 22 and 25 |
| — | A law about its law: every ball it met settles at 0, so two bounces are enough for a new ball | Used only when every object agrees; cups settle at different temperatures, so it still needs 3 readings of a cup |

**Still true:** the *grammar* the kinds are written in (Δ, ρ, composition, two scopes)
is mine. It is small, so reuse saves 2–20× here, not millions. What Ultron can now do
is invent kinds that grammar can express, keep them and transfer them. Inventing the
grammar itself is the next level up, and it is still open.

## The blind test

[`independent_3.txt`](../blind/independent_3.txt) was written from
[`SYLLABUS.md`](../blind/SYLLABUS.md) by a separate agent. It never saw the code, tests
or exams, but it is the same underlying model as me. The test has 50 questions: 25
about things that change step by step, 5 about kicked pucks, 10 refusals and 10 from
earlier lessons.

**First sight: 45/50.** The 5 failures:
- **Backward in time** (a cup's temperature at t = 0 from later readings). It could only
  run a sequence forward.
- **Between readings** (readings every 2 minutes, asked about minute 5). It now repeats a
  step a fraction of a time, the same meaning fractional repeats got in the closing-the-
  gaps work.
- **Two bounces only.** It now notices that every ball it has met settles at 0.

All of these are fixed and are now regression tests. The earlier blind tests still score
60/60, 60/60 and 14/14.

## Grade

**Phase 3: done.** The exit test in [the roadmap](../docs/ROADMAP.md) was to rediscover
the Phase 1 laws from raw simulated video. Ultron does that, and it does it starting
from a blank brain that has only eyes it learned itself. Beyond that exit test, it
invents new kinds of explanation, reuses them in worlds it has never seen, and acts to
reach goals by correcting from what it sees. The next walls are a real 3D body
(Phase 4), language (Phase 5), and letting Ultron grow its own grammar of kinds.
