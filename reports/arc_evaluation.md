# Ultron on ARC-AGI

Official scoring (2 attempts per test output). Development uses the training split only; every evaluation run is logged in `reports/arc_runs.log`.

| Set | Split | Tasks | Score | Seconds | Budget (operations per task) |
|---|---|---|---|---|---|
| ARC-AGI-1 | evaluation | 400 | **7.8%** (31.0) | 244.5 | 40000 |
| ARC-AGI-2 | evaluation | 120 | **0.0%** (0.0) | 115.0 | 40000 |

## ARC-AGI-1 evaluation: what it found

31 tasks solved; 2 where a program fitted every example but gave the wrong answer on the test (wrong generalisation); 367 with no program within budget.

| Task | Program Ultron found |
|---|---|
| 00dbd492 | `fill_enclosed(3) ▸ local law on (colour, size): 2 situations change colour` |
| 0c786b71 | `rot180 ▸ mirror_tile(both)` |
| 0c9aba6e | `combine(('lines', 'nor', 8))` |
| 195ba7dc | `combine(('lines', 'or', 1))` |
| 1d0a4b61 | `complete_pattern(0)` |
| 2072aba6 | `upscale(2) ▸ local law on (colour, parity): 4 situations change colour` |
| 21f83797 | `lines_through((2, 'both')) ▸ fill_enclosed(1)` |
| 31d5ba1a | `combine(('halves_tb', 'xor', 6))` |
| 332efdb3 | `local law on (colour, parity): 3 situations change colour` |
| 34b99a2b | `combine(('lines', 'xor', 2))` |
| 506d28a5 | `combine(('lines', 'or', 3))` |
| 5b6cbef5 | `fractal` |
| 5d2a5c43 | `combine(('lines', 'or', 8))` |
| 60c09cac | `upscale(2)` |
| 66f2d22f | `combine(('halves_lr', 'nor', 5))` |
| 7039b2d7 | `count_parts` |
| 833dafe3 | `rot180 ▸ mirror_tile(both)` |
| 84f2aca1 | `fill_enclosed(5) ▸ local law on (colour, size): 1 situations change colour` |
| 903d1b4a | `remove_colour(3) ▸ symmetrize(both)` |
| 9a4bb226 | `crop_thing(('most_colours', True))` |
| ae58858e | `recolour_all(6) ▸ local law on (colour, size): 3 situations change colour` |
| be03b35f | `rot270 ▸ continue_pattern(((2, 5), (2, 5)))` |
| c663677b | `complete_pattern(0)` |
| ca8f78db | `complete_pattern(0)` |
| cd3c21df | `crop_thing(('rarest_colour', True))` |
| d19f7514 | `combine(('halves_tb', 'or', 4))` |
| d282b262 | `slide_things(left)` |
| e133d23d | `combine(('lines', 'or', 2))` |
| e345f17b | `combine(('halves_lr', 'nor', 4))` |
| e95e3d8e | `complete_pattern(0)` |
| f823c43c | `complete_pattern(6)` |

## ARC-AGI-2 evaluation: what it found

0 tasks solved; 0 where a program fitted every example but gave the wrong answer on the test (wrong generalisation); 120 with no program within budget.

| Task | Program Ultron found |
|---|---|
