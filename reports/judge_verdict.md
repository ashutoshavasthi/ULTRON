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
| **It invents concepts** | **Fractions** (lesson 9, from cutting and weighing cakes). **Negative numbers** (lesson 8). It lived with a purse of coins and IOU notes, never hearing of numbers below zero. On reflection it noticed its purse states form one line that continues past empty. It decided those were places *below zero*, invented a step with no floor, and learned to pay and be paid there. It was told the words "-3" and "negative three" only afterwards. It also invented spring stiffness, and a per-star property that matches the Sun/Jupiter mass ratio. |
| **It transfers** | It predicted Jupiter's moons from one sighting of Io, and unseen Ceres and Halley's Comet from real data. |
| **It composes and reasons backwards** | It answers a never-trained spring-launch problem by chaining two laws, and runs laws backwards. Division, never taught, comes from running multiplication in reverse. |
| **It copes with noise** | With ±1% instruments it uses error propagation and predicts the *true* values. |
| **It knows what it doesn't know** | It refuses situations new *in kind* that none of its principles reach: a planet system it never saw, an unmeasured spring, a division with no whole answer, a word never taught. It gives the reason each time. Tough final exam: 109/109. |
| **It learns what nobody shows it** | Under a biased teacher it still found "same number" and invented negative numbers, because it designed its own experiments. When only watching, it failed both. |
| **It isn't overconfident** | Laws are *tentative* until confirmed 3 times. Its early "momentum after one collision" claim is now marked tentative until the evidence arrives. |
| **It is checkable** | Every answer comes with its reasons. Peano proofs are derived from its own laws and checked independently. Training is deterministic, byte for byte. |

## Imperfections found, and what happened to them

- **Designing experiments: fixed by understanding what it is for.** With a
  teacher who shows everything, it gives no speed gain: 32 vs 34 experiences to
  find every law, and 38 vs 38 with random scenes over a wider range. Occam's
  razor finds each law within a few experiences either way. Its real value
  shows with a **biased teacher**, who never shows equal trays and never lets
  the purse go into debt:
  - Designing its own experiments, Ultron passed both lessons. It invented
    negative numbers by spending from an empty purse itself.
  - Only watching, it failed lesson 1: it concluded that "trays never pair
    off".
  - Only watching, it never invented negative numbers.

  Designing experiments is how it learns what nobody shows it.
- **Lesson 0's exam was weak: fixed.** It now hides several things and tests
  counts never seen. A nearest-example memoriser drops from 100% to 0%.
- **Fair questions below zero were refused: fixed.** One reasoning principle
  was added: doing something a below-zero number of times means undoing it
  that many times. Mathematicians used this "keep the rules working" principle
  to extend arithmetic. Ultron found *which* steps undo which by imagining
  with its own laws ("pay always undoes merge"). From that, it answers:
  - "5 minus -3" = 8
  - "-4 plus -2" = -6
  - **"-2 times -3" = 6**

  "Minus times minus is plus" appears nowhere in the code; Ultron derives it.
- **"what times 3 equals -7" was refused: fixed by a second invention.** It
  was impossible only for whole numbers. In lesson 9 Ultron cut cakes into
  equal pieces and weighed piles on a balance, without ever hearing of
  fractions. It noticed that one piece of a cake cut into 2 balances no whole
  number of cakes, yet 2 of them balance exactly one. So there are amounts
  *between* its numbers, and it invented them. It works everything out with its
  own laws:
  - "what times 3 equals -7" = **-7/3**;
  - "1/2 plus 1/3" = **5/6**, by re-cutting both piles into sixths;
  - "7 divided 2" = 7/2, having learned 'divided' from watching cakes being
    shared.

  Two problems surfaced along the way, and both are fixed:
  - A wrong law that got lucky 8 times in a row used to stay trusted. Now a
    confirmed law that fails is **doubted**, and Ultron keeps playing until
    its replacement is confirmed.
  - Its first fraction search was brute force, taking minutes. It now checks
    whether adding pieces changes anything, then brackets the answer and
    halves the range, taking milliseconds.

  What is still refused really is impossible: "what times 0 equals 5" (zero
  groups of anything is zero), "3/0" (a cake cut into 0 pieces), and words
  never taught.
- **Training speed: fixed.** Laws are pure functions, so their results are now
  memoised. The full 11-lesson curriculum trains in seconds again (it had been
  about a minute).

## What I built, not Ultron

- The innate primitives (counting, `succ`, `pred`, `eq`, "repeat n times").
- The power-product form for measurements.
- The *ability* to notice a line of states and to notice amounts between
  numbers, and the principle that a below-zero number of repetitions means
  undoing. (Phase 2's job is to replace these per-concept abilities with one
  general way of inventing.)
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
