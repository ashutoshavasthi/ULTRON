# Learned words, gate G0 (small pictures)

Produced by `python -m ultron words g0`. The gate and its targets were fixed in advance in [docs/MECHANISM.md](../docs/MECHANISM.md).

Setting: pictures up to 8 x 8, taken only from the practice half; an interpreter of width 96 (303,648 numbers), taught for 30,000 steps.

## G0-a: carrying out hand-written words

- Single words exact on kept-aside pictures: **87.7%** (target 99%).
- Programs of six words exact from start to end: **99/200 = 49.5%** (target 90%).
- **Not met.**

| Family | Exact |
|---|---|
| antitranspose | 20/20 |
| connect | 40/80 |
| crop_content | 15/20 |
| frame_things | 157/180 |
| hollow_things | 7/20 |
| keep_colour | 198/200 |
| remove_colour | 199/200 |
| remove_specks | 35/40 |
| rot180 | 20/20 |
| slide_things | 54/80 |
| symmetrize | 77/80 |
| transpose | 20/20 |

The training run was interrupted at step 20,000 by a machine restart and continued from the saved interpreter for 10,000 more steps at a lower learning rate. Single-word exactness did not improve over that continuation (89% on a smaller sample before it).

By the kill rule (more training once, then stop and report), G0-a stands as **not met** at this size on a CPU. Words that re-map cells or colours are carried out almost perfectly. Words about whole things (sliding, connecting, hollowing) are not. The next test is a wider interpreter trained longer on a GPU.


## G0-b: rediscovering words it was never shown

Target: a free word matches the hidden word on at least 95% of kept-aside pictures for at least 3 of the 5 families. **Met for 3 of 5.**

| Hidden family | Puzzles (explained by hand-written words alone) | Explained by learned words | Words kept | Match on kept-aside pictures | Match on colours never trained | Held-out puzzles right: without -> with learned words | One vector per puzzle: test right | New primitive? |
|---|---|---|---|---|---|---|---|---|
| flip_h | 120 (0) | 120/120 | new0 | 95% | - | 1/80 -> 77/80 | 15/40 | new0: new |
| recolour_all | 120 (0) | 117/120 | new1 (takes a colour), new2 (takes a colour) | 96% | 90% | 0/80 -> 70/80 | 8/40 | new1: new |
| gravity | 240 (5) | 54/235 | new0, new1, new2, new4 (takes a colour), new3, new6 (takes a colour), new5 | 25% | - | 8/80 -> 8/80 | 4/40 | new4: new; new6: new; new5: new |
| fill_enclosed | 120 (0) | 62/120 | new1 (takes a colour), new2 (takes a colour), new3 (takes a colour), new4 (takes a colour), new5 (takes a colour), new6 (takes a colour), new7 (takes a colour) | 26% | 30% | 0/80 -> 7/80 | 4/40 | new4: new |
| outline | 120 (0) | 120/120 | new1 (takes a colour) | 99% | 78% | 0/80 -> 76/80 | 1/40 | new1: new |

Held-out puzzles are made from kept-aside pictures: half use the hidden word alone, half put a hand-written word before or after it. "New" means no program of up to three hand-written words imitates the learned word. In a family that was not relearned, such a word is new but does not do the hidden word's job, so it is not counted as a new primitive on the scoreboard.

The families were run one process each, with the same code as `words g0`, so that a machine restart would lose at most one family. Their results are in `reports/words_runs/run2/`.

**This is the second run.** The first (kept in `reports/words_runs/`) met the target for `flip_h` only. `recolour_all` and `outline` were learned but matched 81% and 88%. It was stopped during `fill_enclosed`, whose words explained 5 and 4 of 120 puzzles, once it could no longer reach 3 of 5. One round of fixes followed, as the kill rule allows: puzzles of words already kept are rehearsed while later words train, and a word keeps growing past 60 members.

**Verdict: G0-b is met.** 3 of 5 families reach a 95% match, where 3 were needed. The margin is thin: each hidden word is checked on 20 kept-aside pictures, so `flip_h` at 19 of 20 sits exactly on the line (it was 20 of 20 in the first run).

**gravity and fill_enclosed were not relearned.** Each split into seven small words, which together explained 54 of 235 and 62 of 120 of their puzzles, but none matched its hidden word on more than about a quarter of kept-aside pictures. For gravity the cause was measured (below). For fill_enclosed it was not; the interpreter's weakness on words about whole things is the likely cause.

Other things this run shows. Learning a new word costs a little of the old ones: single hand-written words were exact on 87.7% of pictures before, and 80% to 84% after a family was learned. On the two colours never used in training, the colour-taking words match 78% to 90%, below their match on trained colours. `recolour_all` ended up split between two learned words (103 and 14 puzzles) where one would do.

## Why gravity is hard: a diagnosis

Measured on the interpreter as saved at step 20,000 (`python -m ultron words diagnose --family gravity`).

A new word trains on one puzzle alone. Of the 8 other puzzles it then fits best, how many have the same hidden word?

| Starting puzzle | Same word among the best 8 | Expected by chance |
|---|---|---|
| gravity(down) | 8 | 1.9 |
| gravity(up) | 8 | 1.9 |
| gravity(left) | 6 | 1.9 |
| gravity(right) | 8 | 1.9 |

A new word is handed a clean group of puzzles of one hidden word.

| Hidden word | Puzzles given | Pass their check | Match on kept-aside pictures |
|---|---|---|---|
| gravity(down) | 4 | 0 | 15% |
| gravity(down) | 8 | 0 | 15% |
| gravity(down) | 16 | 4 | 10% |

## G0-a, second form: taught words practised by family and toward mistakes

Declared before it ran, with the condition for running G0-b again ([docs/MECHANISM.md](../docs/MECHANISM.md), commit e3f9d74). The first form drew the 48 taught words evenly, so a family of one word got 2% of practice and a family of ten 21%. The second form draws a family first, weighted toward the families still got wrong on learning pictures, then a word of it. Same width (96), seed and 30,000 steps.

The first form's run was interrupted at step 20,000; its curve stops there. Each check uses 10 pictures per word, so differences of a few points are noise. Logs: `reports/words_runs/teach_first_form.log`, `teach_second_form.log`.

Training curve, single words exact on kept-aside pictures (10 per word), same seed and size; only the way words are drawn differs.

| Steps | First form (words drawn evenly) | Second form |
|---|---|---|
| 2,500 | 43.5% | 43.3% |
| 5,000 | 61.7% | 66.9% |
| 7,500 | 75.0% | 79.6% |
| 10,000 | 79.0% | 82.1% |
| 12,500 | 83.3% | 85.2% |
| 15,000 | 85.0% | 85.6% |
| 17,500 | 87.5% | 86.9% |
| 20,000 | 89.4% | 88.7% |
| 22,500 | - | 89.4% |
| 25,000 | - | 89.6% |
| 27,500 | - | 89.2% |
| 30,000 | - | 89.6% |

- Single words exact: **88.3%** (first form 87.7%; target 99%).
- Six-word programs exact: **88/200 = 44.0%** (first form 49.5%; target 90%).
- **Not met.**

| Family | First form | Second form |
|---|---|---|
| antitranspose | 20/20 = 100% | 20/20 = 100% |
| connect | 40/80 = 50% | 51/80 = 64% |
| crop_content | 15/20 = 75% | 20/20 = 100% |
| frame_things | 157/180 = 87% | 135/180 = 75% |
| hollow_things | 7/20 = 35% | 17/20 = 85% |
| keep_colour | 198/200 = 99% | 197/200 = 98% |
| remove_colour | 199/200 = 100% | 198/200 = 99% |
| remove_specks | 35/40 = 88% | 37/40 = 92% |
| rot180 | 20/20 = 100% | 20/20 = 100% |
| slide_things | 54/80 = 68% | 55/80 = 69% |
| symmetrize | 77/80 = 96% | 78/80 = 98% |
| transpose | 20/20 = 100% | 20/20 = 100% |

**Verdict: not met, and no overall gain.** Single words are exact on 88.3% against 87.7%, within noise. The curves ran ahead by about 5 points early on (66.9% against 61.7% at 5,000 steps) and were level from 15,000 steps.

**Practice moved accuracy between families rather than adding to it.** hollow_things rose from 35% to 85% and crop_content from 75% to 100%; frame_things fell from 87% to 75%, as its share of practice fell from 19% (9 of the 48 words) to between 10% and 16%. Six-word programs fell from 99 to 88 of 200.

**G0-b was not run again.** The condition fixed in advance was single words up by 3 points, or the three weakest families up by 10 points each. Single words rose 0.6 points; of the three weakest, hollow_things and connect rose 50 and 14 points but slide_things only 1.

**What it suggests.** At width 96 the interpreter behaves as if it is full: giving one family more practice costs another. That points to its size rather than its diet, which is what the GPU run tests (`--size gpu`: twice as wide, one more pass, 100,000 steps). The second form's way of drawing words stays the default, so that run gives the one-word families their share from the start. The first form can still be reproduced with `python -m ultron words teach --even`.
