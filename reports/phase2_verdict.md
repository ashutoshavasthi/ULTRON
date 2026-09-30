# Judge's verdict: Phase 2 (inventing concepts, more generally)

*Written by Claude, as Ultron's trainer and judge, after running lessons 0–14,
every exam, and the experiments in `python -m ultron experiment`. Metrics are in
[`report_card.md`](report_card.md).*

## Verdict

**Phase 2 passes, but it isn't perfect.** Ultron now invents concepts with
mechanisms that are *general*: each one produced at least one concept it was
never built for. Every Phase 2 lesson and the Phase 2 final exam passed on the
first attempt. Where it falls short of "one mechanism for everything" is listed
below, as plainly as the successes.

## What Phase 2 demonstrated

| Mechanism | What it invented | Evidence it's general |
|---|---|---|
| **Shape discovery** (`invention.py`): walk an action from the empty state with its own laws and look at the shape it traces | **Clock numbers** (lesson 11): "the 6th tick brings me back to the start... numbers go round" | The *same code* found negative numbers as a line in Phase 1. Nothing in it mentions clocks or wheels. |
| **Hidden quantities** (`invariants.py`): when no product stays constant, try A + λ·B with λ fitted | **Energy** (lesson 12): y + 0.0509684·v² per run (= height + v²/2g), found in 7 experiences, mass correctly left out | It noticed that its coefficient's units are those of its own accelerometer readings. It then answered never-trained questions about balls thrown *upwards*. |
| **Compression** (`compression.py`): find the pattern "this law is that law, repeated" in its own library | **Powers**, predicted in *lesson 3*, ten lessons before meeting anything that grows | The growing world confirmed the prediction. Ultron searched 0 programs, against 110,210 without compression. It then declined to predict the next rung and explained why (powers aren't symmetric). |
| **Laws on amounts** (`amounts.py`): run any of its programs on fractions; "undo" steps below zero | **Square roots, cube roots, logarithms, negative and fractional powers**, none of them taught | "what power 2 equals 81" = 9, "2 power what equals 1024" = 10, "3 power -2" = 1/9. It correctly refuses "what power 2 equals 2": no fraction answers it. |

**Imperfections from Phase 1, fixed in Phase 2:**
- **Designing experiments now pays off.** It used to pick the first situation
  that split its ideas, which was always the tiniest, like "0 groups of 1". Such
  cases fit almost any rule. It now prefers the richest such situation.
  Experiences needed to find every law:

  | Teacher | Designing | Watching | Saving |
  |---|---|---|---|
  | Helpful | 27 | 34 | 21% |
  | Random, wider range | 23 | 38 | 39% |

  With a biased teacher it is still the only way to learn what nobody shows it.
- **Speed.** Ultron checks which of its laws are symmetric and then "counts on
  from the bigger number". Full training went from 50 seconds to 9 seconds,
  with identical answers.

## Imperfections, stated plainly

1. **Fractions still use their own mechanism.** Shape discovery unified
   negatives and clock numbers; fractions still come from `amounts.py`, which
   was built for them. One mechanism for all three is not done.
2. **The mechanisms are still categories I designed:** shapes of an action's
   walk, two-term sums, the REPEAT pattern. They're far more general than
   Phase 1's one-concept detectors, but Ultron can't invent a new *kind* of
   hypothesis.
3. **REPEAT was generalised from one example.** Ultron says so ("I have seen
   this shape 1 time"), treats the result as a prediction, and lets the world
   decide. It also tries its prediction on every new two-number experience.
   That's harmless and quickly refuted, but naive.
4. **Energy has exactly two terms.** A world where height, speed and a spring
   all share energy would need three terms, which the search does not try.
5. **Its wheel law is odd.** It wrote `earn_coins(slot, groups(6,
   take_away(slot, 4)))` instead of "if slot is 5 then 0 else slot + 1". Both
   are correct and equally short; Occam's razor cannot tell them apart.
6. **Irrational numbers are a genuine next invention.** Ultron is right that
   no fraction squared makes 2. Inventing numbers that fill those gaps is where
   its current mechanisms stop.
7. **I wrote every exam.** A blind test from someone else is still the
   strongest evidence missing.

## Grade

Phase 2 is **passed**. The inventions are real and each one is checked on
problems never seen: clock numbers, energy, predicted powers, and roots and
logarithms never taught. "One mechanism for every concept" is still an
honest *not yet*.
