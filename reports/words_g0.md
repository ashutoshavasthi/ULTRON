# Learned words, gate G0 (small pictures, CPU)

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

Target: a free word matches the hidden word on at least 95% of kept-aside pictures for at least 3 of the 5 families. **Met for 3 of 5 (3 run so far).**

| Hidden family | Puzzles (explained by hand-written words alone) | Explained by learned words | Words kept | Match on kept-aside pictures | Match on colours never trained | Held-out puzzles right: without -> with learned words | One vector per puzzle: test right | New primitive? |
|---|---|---|---|---|---|---|---|---|
| flip_h | 120 (0) | 120/120 | new0 | 95% | - | 1/80 -> 77/80 | 15/40 | new0: new |
| recolour_all | 120 (0) | 117/120 | new1 (takes a colour), new2 (takes a colour) | 96% | 90% | 0/80 -> 70/80 | 8/40 | new1: new |
| outline | 120 (0) | 120/120 | new1 (takes a colour) | 99% | 78% | 0/80 -> 76/80 | 1/40 | new1: new |

Held-out puzzles are made from kept-aside pictures: half use the hidden word alone, half put a hand-written word before or after it. "New" means no program of up to three hand-written words imitates the learned word.

The families were run one process each, with the same code as `words g0`, so that a machine restart would lose at most one family. Their results are in `reports/words_runs/run2/`.

**This is the second run.** The first (kept in `reports/words_runs/`) met the target for `flip_h` only. `recolour_all` and `outline` were learned but matched 81% and 88%. It was stopped during `fill_enclosed`, whose words explained 5 and 4 of 120 puzzles, once it could no longer reach 3 of 5. One round of fixes followed, as the kill rule allows: puzzles of words already kept are rehearsed while later words train, and a word keeps growing past 60 members.

**Verdict: G0-b is met.** 3 of 5 families reach a 95% match, where 3 were needed. The margin is thin: each hidden word is checked on 20 kept-aside pictures, so `flip_h` at 19 of 20 sits exactly on the line (it was 20 of 20 in the first run).

Not in the table: gravity, fill_enclosed. These were still running when this report was written; their words had explained only a few puzzles each (see the diagnosis below).

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
