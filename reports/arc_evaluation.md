# Ultron on ARC-AGI

Official scoring (2 attempts per test output). Development uses the training split only; every evaluation run is logged in `reports/arc_runs.log`.

| Set | Split | Tasks | Score | Seconds | Budget (operations per task) |
|---|---|---|---|---|---|
| ARC-AGI-1 | evaluation | 400 | **3.8%** (15.0) | 428.3 | 40000 |
| ARC-AGI-2 | evaluation | 120 | **0.0%** (0.0) | 179.6 | 40000 |

## ARC-AGI-1 evaluation: what it found

15 tasks solved; 1 where a program fitted every example but gave the wrong answer on the test (wrong generalisation); 384 with no program within budget.

| Task | Program Ultron found |
|---|---|
| 0c786b71 | `rot180 ▸ mirror_tile(both)` |
| 0c9aba6e | `combine(('lines', 'or', 8)) ▸ recolour 0→8, 8→0` |
| 31d5ba1a | `combine(('halves_tb', 'xor', 6))` |
| 34b99a2b | `combine(('lines', 'xor', 2))` |
| 506d28a5 | `combine(('lines', 'or', 3))` |
| 60c09cac | `upscale(2)` |
| 66f2d22f | `combine(('halves_lr', 'or', 5)) ▸ recolour 0→5, 5→0` |
| 833dafe3 | `rot180 ▸ mirror_tile(both)` |
| 903d1b4a | `remove_colour(3) ▸ symmetrize(both)` |
| 9a4bb226 | `crop_thing(('most_colours', True))` |
| cd3c21df | `crop_thing(('rarest_colour', False)) ▸ recolour 0→2` |
| d19f7514 | `combine(('halves_tb', 'or', 4))` |
| e133d23d | `combine(('lines', 'or', 2))` |
| e345f17b | `combine(('halves_lr', 'or', 4)) ▸ recolour 0→4, 4→0` |
| f823c43c | `remove_colour(6) ▸ symmetrize(both)` |

## ARC-AGI-2 evaluation: what it found

0 tasks solved; 0 where a program fitted every example but gave the wrong answer on the test (wrong generalisation); 120 with no program within budget.

| Task | Program Ultron found |
|---|---|
