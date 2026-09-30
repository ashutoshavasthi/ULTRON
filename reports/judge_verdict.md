# Judge's verdict: Phase 1 (Baby Ultron), final

*Written by Claude, acting as Ultron's trainer and judge, after running all ten
lessons and every exam in this repository and questioning Ultron directly.
The metrics are in [`report_card.md`](report_card.md); the full conversation is
in [`transcript.md`](transcript.md).*

## Verdict

**Phase 1 is complete.** Ultron is the kind of learner this project set out to
build. It is grounded, it learns rules rather than answers, its knowledge
compounds, and it **invented a concept nobody gave it**. It is still an infant,
and I built its innate abilities. The one test that could prove me wrong has
not been run yet: a blind test written by someone else (see "What is still
open").

## What Ultron demonstrated

| Claim | Evidence |
|---|---|
| **Rules, not answers** | 100% on held-out sizes far outside training in every numeric exam. A lookup memoriser trained on the same experiences scored 0%. |
| **Knowledge compounds** | Multiplication was found only because addition was in its library. A blank brain scored 0/40. Place value was built from both. |
| **It invents concepts** | **Negative numbers** (lesson 8). It lived with a purse of coins and IOU notes, never hearing of numbers below zero. On reflection it noticed its purse states form one line that continues past empty. It decided those were places *below zero*, invented a step with no floor, and learned to pay and be paid there. It was told the words "-3" and "negative three" only afterwards. It also invented spring stiffness, and a per-star property that matches the Sun/Jupiter mass ratio. |
| **It transfers** | It predicted Jupiter's moons from one sighting of Io, and unseen Ceres and Halley's Comet from real data. |
| **It composes and reasons backwards** | It answers a never-trained spring-launch problem by chaining two laws, and runs laws backwards. Division, never taught, comes from running multiplication in reverse. |
| **It copes with noise** | With ±1% instruments it uses error propagation and predicts the *true* values. |
| **It knows what it doesn't know** | It refuses situations new *in kind*: a planet system it never saw, an unmeasured spring, a negative wage, a word never taught. It gives the reason each time. Tough final exam: 109/109. |
| **It isn't overconfident** | Laws are *tentative* until confirmed 3 times. Its early "momentum after one collision" claim is now marked tentative until the evidence arrives. |
| **It is checkable** | Every answer comes with its reasons. Peano proofs are derived from its own laws and checked independently. Training is deterministic, byte for byte. |

## What did not work, honestly

- **Designing experiments made no measurable difference.** Ultron now sets up
  the situation where its rival explanations disagree, or else a kind of
  situation it has never tried. Summed over all laws, it needed 35 experiences
  to find its final laws; watching random scenes needed 34. It helped on the
  harder purse laws (12 vs 19) and hurt on simple ones. In worlds this small,
  every law appears within a few experiences anyway. I tried two other
  strategies (more rivals; novelty first); neither helped. The mechanism
  stays, and its value is unproven.
- **The lesson 0 exam is weak.** A nearest-example memoriser also scores 100%.
- **Some refusals are a judgement call.** Ultron refuses "5 plus -3" because it
  was never paid a negative wage. That is consistent with its principle, but a
  person would simply answer 2.
- **Training slowed from ~5 s to ~1 min.** The purse lesson's searches reach
  70,000 candidate programs.

## What I built, not Ultron

- The innate primitives (counting, `succ`, `pred`, `eq`, "repeat n times").
- The power-product form for measurements.
- The *ability* to notice a line of states.
- The curiosity and confirmation rules.
- The reading and solving procedures.

What Ultron discovers with these is its own. Nothing in the code states a law,
a formula or an answer. But the space it searches is small and was designed by
me. Phase 2's job is to let it grow that space itself.

## What is still open

1. **The blind test.** Write questions in `blind/` (format in
   `blind/README.md`) and run `python -m ultron blind yourfile.txt`. I wrote,
   ran and then improved against every other test, so only a test written by
   someone else proves the claims above. If it fails fairly, Phase 1 isn't
   done, and I'll say so.
2. **Invention beyond one mechanism.** Line discovery produced negative
   numbers. Phase 2 needs a general way to invent, by compressing recurring
   pieces of its own programs into new primitives.

*Grade: Phase 1 passed. It is the right kind of mind, a very young one, with
one genuine invention of its own.*
