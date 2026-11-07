# The learning curve

One row per round of `python -m ultron learn` (docs/PLAN.md). Practice: tasks explained so far (new this round). Held out: tasks it never learns from, right (wrong), with its words; without any words it gets the number in the 'without' column. Learning compounds when the gain grows from round to round.

| Round | When | Run | Practice explained (new) | Words | Held out: without | with its words | Gain | Change from last round |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-20 09:15 | full (316 held out) | 35 (+35) | 5 | 37 (4) | 39 (6) | +2 | +2 |
| 2 | 2026-10-20 09:35 | full (316 held out) | 45 (+10) | 8 | 37 (4) | 40 (11) | +3 | +1 |
| 3 | 2026-10-20 09:55 | full (316 held out) | 46 (+1) | 9 | 37 (4) | 42 (9) | +5 | +2 |

## From here on: held-out answers must earn their place

Rows above answered whenever any program fit the examples, and their wrong answers rose with the right ones. From here on a held-out answer is given only when its explanation also holds with any one example left out (as the main solver does), and Ultron tries first the steps it uses most (its intuition). **Net** = right - wrong; **precision** = right / answered. Learning compounds when net and right rise while wrong stays low.

| Round | When | Run | Practice explained (new) | Words | Held out without: right (wrong) | with its words and intuition | Net (without -> with) | Precision | Change in net from last round |
|---|---|---|---|---|---|---|---|---|---|
| 3b | 2026-11-07 03:51 | full (316 held out) | 46 (+0) | 9 | 30 (1) | 34 (0) | 29 -> 34 | 100% | - |
| 4 | 2026-11-07 04:10 | full (316 held out) | 47 (+1) | 9 | 30 (1) | 32 (0) | 29 -> 32 | 100% | - |
| 5 | 2026-11-07 04:32 | full (316 held out) | 47 (+0) | 9 | 30 (1) | 32 (0) | 29 -> 32 | 100% | +0 |
| 6 | 2026-11-07 04:51 | full (316 held out) | 47 (+0) | 9 | 30 (1) | 32 (0) | 29 -> 32 | 100% | +0 |

## From here on: dreams and a learned guide (M1 in docs/PLAN.md)

Each night Ultron makes puzzles from its own language (dreams) and learns from them and from its real solutions which steps a puzzle needs (its guide). **Interval**: 95% bootstrap interval of the gain in net over knowing nothing; the gain is real when it excludes 0. **Missed**: held-out tasks with no answer; of a sample of them re-searched with 4x the budget, how many were then found (search limits it) or not (its language or eyes limit it). M1's target: practice explained >= 80 and net gain >= +15 at >= 95% precision within 3 rounds; if the gain is < +10 after 3 rounds, program search stops being the main line.

| Round | When | Run | Practice explained (new) | Words | Dreams | Held out: right (wrong) | Net (without -> with) | Interval of the gain | Precision | Missed: found with 4x budget / not found (of sample) |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 | 2026-11-07 05:15 | full (316 held out) | 47 (+0) | 9 | 3000 | 32 (0) | 29 -> 32 | +0 to +7 | 100% | 284: 0 / 40 (of 40) |
| 8 | 2026-11-07 05:36 | full (316 held out) | 48 (+1) | 9 | 3000 | 32 (0) | 29 -> 32 | +0 to +7 | 100% | 284: 0 / 40 (of 40) |
| 9 | 2026-11-07 05:57 | full (316 held out) | 48 (+0) | 9 | 3000 | 32 (0) | 29 -> 32 | +0 to +7 | 100% | 284: 0 / 40 (of 40) |
