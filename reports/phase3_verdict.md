# Judge's verdict: closing Phase 2's gaps, and the first blind tests

*Written by Claude, as Ultron's trainer and judge, after running lessons 0–18,
every exam, and two blind tests written by independent examiners.*

## Verdict

**Three of the four gaps named at the end of Phase 2 are closed. The fourth is
narrowed, not closed.** All 19 lessons pass on the first attempt. Training takes
23 s instead of 90 s, and retraining gives the same brain file byte for byte.
On the two independent blind tests Ultron first scored **55/60** and **54/60**
(and one run crashed). Every failure was fair. Each is now fixed at its cause,
and both tests now score 60/60. Those 60/60 scores are *after* fixing, so the
honest blind numbers are the first ones.

## The four gaps

| Gap (from the Phase 2 verdict) | What Ultron does now | Evidence |
|---|---|---|
| **Counting arithmetic is slow and imprecise** | It invents **column arithmetic**. From its place-value law it checks four identities on 40 examples each: columns add, ten in a column carries, times spreads over columns, and a 0 on the end is times ten. It then builds column methods from its own single-digit facts, known by heart once counted. A column method is used for a law only after it agrees with the law on 60 examples. Its laws of repeating also let it **square** (a^(2k) = (a^k)²). Inverse questions with big numbers step out 1, 2, 4, … and halve. | 20-digit products exact; `3 power 40`, `5 power 30` exact; `what plus 314159265358979 equals 271828182845904` answered instantly. Log and root pins went from 2–15 s to about 0.2 s, and 5^(2/3) is now pinned to a thousandth. |
| **"Repeat 1.58 times" means nothing** | It checks its **laws of repeating** with its own laws: repeating p times then q more is repeating p+q times; repeating p times, done q times, is repeating p·q times. The only meaning of "repeat 1/2 time" that keeps those laws true is "whatever, repeated twice, is repeating once". Fractional powers and logarithms become questions about whole repeats. | `8 power 2/3` = 4, `27/8 power -2/3` = 4/9, `2 power what equals 3` between 79/50 and 159/100, `10 power 1/3` pinned. `0 power -1` is refused, with the reason that nothing undoes "times 0". |
| **It can't invent new kinds of hypothesis** | Narrowed. It finds **laws about its own laws**. Its invented property (each spring's stiffness) becomes data, and it runs its hypothesis engine one level up: stiffness × coils = 600 for every spring. | It predicts the pull of springs it has **never stretched** from counting their coils (15/15). It works backwards, "how many coils?" (10/10), and chains through the new law in both directions. |
| **No blind test** | A public [syllabus](../blind/SYLLABUS.md) (what it experienced, how to ask, the world's true settings for grading) and two tests written from it by examiners who never saw the code, tests or exams. | 55/60, then 54/60 on first sight. See below. |

The third gap is only narrowed. A law about a law *composes* the kinds of
hypothesis Ultron already has, one level up. That is how a lot of real science
proceeds, but it is not a new kind. Inventing new kinds of hypothesis is still
the research frontier.

## The blind tests

Two examiners each wrote 60 questions: 20 arithmetic, 25 physics and 15 where
the only right answer is "I can't". They read only `blind/SYLLABUS.md`,
`blind/README.md` and the public data files. They were separate agents running
**the same underlying model as me**, the trainer. They didn't see my code,
tests or exams, but they are not independent people. A test written by a human
still counts for more.

**Test 1 ([`independent_1.txt`](../blind/independent_1.txt)), 55/60 on first sight.** All
15 refusals were right. Five failures:
- It couldn't solve for a *start* value (`find v0 …`, `find y0 …`), because it only
  reasoned forward along a run.
- It couldn't take a spring bumper as unsquashed when the question didn't mention
  it. Now a quantity mentioned at only one moment is taken as 0, and the answer
  says so.

**Test 2 ([`independent_2.txt`](../blind/independent_2.txt)), 54/60 on first sight,
and the first full run crashed.**
- **Big inverse questions ran out of memory.** `what plus 314159265358979 equals …`
  listed candidates one by one. It now steps out and halves.
- **`27/8 power -2/3`.** Undoing a fractional step twice needs fine pieces (729ths).
  It now guesses the kind of piece from the question's own numbers and checks the
  guess exactly. Simplifying uses only the kinds of piece that fit evenly, found in
  pairs.
- **`5/6 divided what equals -10/3`.** Inverse questions about `divided` weren't
  understood. They are now read through what `divided` means.
- **`0 divided 0` answered 0.** Every amount works, so there is no one answer, and it
  now says so.
- **`find a given spring=S2 x=0 m=5`, `find x given spring=S4 F=0`.** Its laws refused
  any zero. Now a zero makes the answer zero when it multiplies, and "no number" when
  it divides (so `find a given F=10 m=0` is still refused).

Both tests are now regression tests (`tests/test_phase3.py`).

## Honest limits

1. **These blind tests are not truly independent.** The examiners were the same model
   as the trainer. The next proof must come from a person.
2. **The kinds of hypothesis are still hand-given.** Laws about laws reuse them one
   level up.
3. **Precision is budgeted.** Logarithms are pinned to hundredths; roots often to
   thousandths. Any finer costs more counting than the budget allows, and it says so
   by giving a range, never a false exact answer.
4. **Filling unstated quantities with 0 is a convention.** It is announced in the
   answer's reasons, but it is a convention and not something Ultron learned.

## Grade

**Phase 2's gaps: three closed, one narrowed.** Ultron invented column arithmetic,
gave fractional repeats their only consistent meaning, and found a law about its own
law that predicts experiments it never did. It also met its first examiners. Where it
failed them, the failures were real, and the fixes are general mechanisms, not
answers.
