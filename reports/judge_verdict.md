# Judge's verdict: Baby Ultron v0

*Written by Claude, acting as Ultron's trainer and judge, after running every
lesson and exam in this repository and questioning Ultron directly. Metrics are
in [`report_card.md`](report_card.md); the full conversation is in
[`transcript.md`](transcript.md).*

## Verdict

**Phase 1 is passed as a proof of mechanism. It is not yet intelligence.**

Ultron learns the way the design intends, and the results cannot be explained
by memorisation. It is still a small learner in a small world that I designed
to be learnable. Both statements are true, and the second one matters as much as
the first.

## What Ultron genuinely demonstrated

1. **Rules, not answers.** On every numeric exam with sizes outside its
   training range, Ultron scored 100%. A lookup memoriser trained on exactly the
   same experiences scored 0%, and a nearest-example memoriser scored 0–40%.
   The one exception is lesson 0 (see weaknesses).
2. **Knowledge compounds.** Multiplication was found *only* because addition was
   already in its library. A blank brain given the identical lesson found
   nothing (0/40). Place value was then found using both addition and
   multiplication.
3. **It invents concepts.** Nobody mentioned stiffness. Ultron noticed that
   `F / x` is constant for each spring but different between springs, and
   concluded that every spring carries a hidden property. It did the same with
   the planets: the Kepler constant became a property of the central body, and
   Ultron's ratio for Jupiter vs the Sun (≈1049) is the real mass ratio (≈1047).
4. **It transfers.** It predicted three of Jupiter's moons from a single
   observation of Io, using the form of a law it had learned from planets. A
   blank brain could predict nothing from one moon.
5. **It composes.** It had never seen a ball launched by a spring. It answered
   by chaining the spring law and Newton's law through the shared quantity F.
   The trace is in the report card.
6. **It knows what it doesn't know.** It says "I don't know what 'divided'
   means" and "I don't know the word 'twelve'" instead of guessing.
7. **Its curiosity isn't fooled by noise.** It gave the random lamp panel the
   minimum look (16 tries) and never came back.
8. **Its reasoning is checkable.** Its Peano rules are derived from its own
   programs, and an independent checker verifies every proof step.

## The tougher test (lessons 7 and 8)

Lessons 0–6 were too easy for the verdict to mean much, so I added two harder
lessons.

- **Lesson 7, the noisy lab.** Every reading is off by up to ±1%.
- **Lesson 8, the final exam.** There is no teaching at all, and every question
  is of a kind never practised:
  - division, which was never taught;
  - inverse questions and three-step chains;
  - physics solved for a different unknown, and chained backwards;
  - unseen real bodies (Ceres and Halley's Comet);
  - impossible questions, where the only correct answer is "I can't".

**What happened the first time, before any changes:**
- In the noisy lab Ultron found **no laws at all**. It demanded exact
  constancy, and noisy data is never exact.
- It answered "5 minus 8 = 0".
- It confidently gave Titan (orbiting Saturn) a period using the Sun's
  constant, and got it wrong.
- In the noisy lab, its estimate of F/(m·a) stayed at 0.991. It was computed
  from the first few noisy readings and never updated.

**What I changed in the brain.** Each change is a general principle, not an
answer:
1. **Error propagation.** Instruments state their precision, and Ultron
   works out how much error a formula can accumulate (sum of |powers| ×
   precision). Small misses within that are no longer surprises.
2. **Outside experience.** Rules generalise across *magnitude*, but a
   situation that is new *in kind* is not predicted. Examples: taking away more
   than there is, which never happened in any experience; a planetary system it
   has never observed; a spring it has never measured. Ultron now says so and
   gives the reason.
3. **Reasoning backwards.** For "what times 4 equals 20", Ultron tries 0, 1,
   2, ... with its own law. Division was never taught, so this is how it
   divides. It also refuses when no number works.
4. **Refining estimates.** Constants are re-averaged over all evidence, not
   frozen at discovery.
5. **Trusting precise evidence.** When two laws relate the same quantities
   (from the clean sandbox and from the noisy lab), the reasoner uses the more
   precise one.

**Result after the changes:** lesson 7 60/60, lesson 8 109/109. All previous
exams still pass.

**Honest caveat:** I designed this test, saw the failures, then improved the
brain. The changes are principled and the exam items are random draws, so this
is not memorising answers. But it is no longer a *blind* test. The real proof
is a test written by someone else. **Ask Ultron your own questions** with
`python -m ultron ask`.

## Weaknesses, stated plainly

1. **I designed the building blocks.** Ultron combines primitives such as
   `succ`, `pred`, `eq`, repetition and the power-product form. It did not
   invent them. Its search space is small, and the answers are guaranteed to be
   in it. This is the biggest limitation and the main Phase 2 target.
2. **The exams share the lessons' structure.** Held-out values are far outside
   the training range, but they are the same kind of problem. The lesson 0
   exam is weak: the nearest-example memoriser also scored 100%.
3. **The physics is clean and the real data is tiny.** The sandbox has no
   noise. The real-data lesson has 12 orbits and 25 Boyle rows. Finding these
   laws this way was already done by the BACON program in the 1970s, so this is
   a sound foundation, not new science.
4. **Overconfidence.** It declared momentum conserved after one collision.
   Reflection later refined this correctly, but there is no uncertainty or
   confidence tracking on laws yet.
5. **Its world stops at zero.** It now correctly *refuses* "5 minus 8"
   instead of saying 0. But it still has no negative numbers or fractions, and
   it divides only by trial, not with a division concept of its own.
6. **Its language is tiny.** It knows 30 grounded tokens and one sentence
   pattern ("x op y"). This is grounded, but it is nowhere near English.
7. **Some strategies are built in.** Reading numerals left to right, and solving
   a collision for one unknown, are hand-written procedures. The laws they use
   are learned; the procedures are not.
8. **Curiosity chooses what, not how.** Ultron picks which experiment to run,
   but not its parameters. It doesn't yet design experiments to settle
   questions.

## What I would teach next (Phase 2)

- **Library learning:** let Ultron compress recurring pieces of its programs
  into new primitives it names itself (DreamCoder-style). The first target is
  to invent "negative" or "division" when the world demands it (debts, sharing).
- **Confidence per law:** how many independent confirmations a law has, and
  demotion when a law fails.
- **Active experiments:** choose parameters that best split the surviving
  hypotheses.
- **A noisy sandbox**, so uncertainty handling is forced early.
- **Blind exams** written by someone other than its trainer.

*Grade: A for the mechanism, and honestly an early infant for intelligence.
It is the right kind of learner. It is still very early in its life.*
