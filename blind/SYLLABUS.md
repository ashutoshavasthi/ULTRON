# What Ultron was taught: the public syllabus for blind examiners

This page is all an examiner needs to write a blind test. It says what Ultron
*experienced* and how to ask it questions. It does not say what Ultron
concluded; finding that out is the point of the test. Don't read the code, the
tests or the trainer's exams: that would make the test not blind.

## What Ultron experienced (in order)

1. **Hidden things.** Objects hidden under a cup and revealed later.
2. **Same number.** Two trays of objects, paired off one to one.
3. **Putting together and taking away.** Merging two trays; taking some away.
4. **Groups of groups.** Several groups of the same size, counted together.
5. **Names.** The marks `0`–`9`, the words `zero`–`ten`, two-mark numerals, and
   the words `plus`, `minus`, `times`, `equals` (and the signs `+ - * × ÷ =`),
   each shown alongside examples. It was never shown division.
6. **Pushing, stretching, colliding.** Balls pushed with a steady force;
   springs `S1`–`S5` stretched; balls colliding (sticky "clay" and bouncy "steel").
7. **Real measurements.** Planets' orbit sizes and periods (NASA fact sheets),
   and Boyle's 1662 air-pressure measurements. The data is in
   `ultron/env/data/*.csv`, which you may read.
8. **A noisy lab.** The same experiments with instruments off by up to ±1%.
9. **Owing.** A purse of coins and IOU notes: getting paid, paying.
10. **Sharing cakes.** A knife that cuts cakes into equal pieces, and a balance.
    It was shown the word `/` and the word `divided` by example.
11. **The wheel.** A wheel with **6** slots, numbered 0–5 from the top mark, and a
    pointer that ticks round. The word `after` names ticking on.
12. **Hills and valleys.** Balls rolling on a frictionless track.
13. **Growing.** Cells that split; the word `power` names repeated splitting.
14. **Hills and a spring.** The same track with a spring bumper at the bottom.
15. **A tile's diagonal.** Rulers with different numbers of marks.
16. **Coiled springs.** Springs wound from the same wire with different numbers
    of coils: stretching one shows its pull, looking at it shows its coils.

## How to ask

### Arithmetic

Numbers may be marks (`23`, `-5`), words (`seven`), `negative 4`, or fractions
(`7/2`, `-1/3`). Operations: `plus`, `minus`, `times`, `divided`, `power`, and
`after` (the 6-slot wheel). Examples of the forms it accepts:

```
23 plus 19
what is 5 minus 8
what times 6 equals 54          (one unknown, written "what")
2 power what equals 1024
3 plus 4 times 2                (worked left to right: (3 + 4) × 2)
100 after 3                     (tick 100 times from slot 3)
```

Answers are whole numbers or fractions in lowest terms (`7/2`, `-1/3`). When no
fraction is exactly right (e.g. `what power 2 equals 2`), Ultron gives a range
`between A and B`; write the expected answer as `~1.41421`.

### Physics

`find <quantity> given name=value ...`. SI units: kg, m, s, N.

| Situation | Quantities |
|---|---|
| pushing a ball | `F` (N), `m` (kg), `a` (m/s²) |
| stretching a spring you name | `spring=S1`…`S5`, `x` (m), `F` (N) |
| a ball on a stretched spring | `spring=…`, `x`, `m`, `a` |
| coiled springs | `coils`, `x` (m), `F` (N); no spring name needed |
| a collision | `m1 v1 m2 v2 v1_after v2_after` (kg, m/s; head-on, signed) |
| a run on the track | now: `y` (height, m), `v` (speed, m/s); at the start: `y0`, `v0` |
| the track with the spring bumper | also `c` (how far the bumper is squashed, m) and `c0` |
| orbits | `r` (m), `T` (s), `system=Sun` |
| Boyle's air | `P`, `V` in the data's own units |

### What the world really is (Ultron was never told this)

Use these to work out the true answers.
- Gravity on the track is g = 9.81 m/s². The track is frictionless.
- The bumper spring has stiffness 400 N/m and the ball on that track is 2 kg.
- Coiled springs: stiffness = 600 N/m ÷ coils.
- Collisions: momentum is always conserved; steel balls also keep their kinetic energy.
- The stiffness of S1–S5 is hidden and random, so don't ask for exact values about
  them. You can ask questions whose answers cancel it out, or check that it
  refuses springs it has never met.

## Scoring format

One question per line: `question | expected`. `refuse` means the only right answer
is "I can't". `~x` means the true value is x and Ultron must pin it in a range
containing x. Arithmetic is compared exactly; physics numbers within 2%.
