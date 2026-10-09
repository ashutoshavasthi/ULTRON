# Ultron on ARC-AGI

Official scoring (2 attempts per test output). Development uses the training split only; every evaluation run is logged in `reports/arc_runs.log`.

| Set | Split | Tasks | Score | Seconds | Budget (operations per task) |
|---|---|---|---|---|---|
| ARC-AGI-1 | evaluation | 400 | **11.8%** (47.0) | 650.0 | 40000 |
| ARC-AGI-2 | evaluation | 120 | **0.8%** (1.0) | 454.6 | 40000 |

## ARC-AGI-1 evaluation: what it found

47 tasks solved; 12 where a program fitted every example but gave the wrong answer on the test (wrong generalisation); 341 with no program within budget.

| Task | Program Ultron found |
|---|---|
| 00dbd492 | `fill_enclosed(3) ▸ thing law on (shape): keep except 2 kinds` |
| 0c786b71 | `rot180 ▸ mirror_tile(both)` |
| 0c9aba6e | `combine(('lines', 'nor', 8))` |
| 12eac192 | `thing law on (size): keep except 2 kinds` |
| 195ba7dc | `combine(('lines', 'or', 1))` |
| 1d0a4b61 | `complete_pattern(0)` |
| 2072aba6 | `upscale(2) ▸ local law on (colour, parity): 4 situations change colour` |
| 21f83797 | `lines_through((2, 'both')) ▸ fill_enclosed(1)` |
| 31d5ba1a | `combine(('halves_tb', 'xor', 6))` |
| 332efdb3 | `local law on (colour, parity): 3 situations change colour` |
| 34b99a2b | `combine(('lines', 'xor', 2))` |
| 47996f11 | `symmetry (quarter turns) about its own centre fills what colour 6 hides` |
| 506d28a5 | `combine(('lines', 'or', 3))` |
| 5b6cbef5 | `fractal` |
| 5d2a5c43 | `combine(('lines', 'or', 8))` |
| 60c09cac | `upscale(2)` |
| 66f2d22f | `combine(('halves_lr', 'nor', 5))` |
| 67b4a34d | `symmetry (v) about its own centre fills what colour 3 hides, answer is the repaired patch` |
| 7039b2d7 | `count_parts` |
| 72a961c9 | `marks around things by (colour): 3 kinds leave marks` |
| 73ccf9c2 | `the thing with symmetric=False` |
| 833dafe3 | `rot180 ▸ mirror_tile(both)` |
| 84db8fc4 | `thing law on (colour, border): 4 kinds of thing` |
| 84f2aca1 | `marks around things by (size): 2 kinds leave marks` |
| 903d1b4a | `remove_colour(3) ▸ symmetrize(both)` |
| 929ab4e9 | `remove_colour(2) ▸ symmetrize(both)` |
| 981571dc | `symmetry (h+v) about its own centre fills what colour 0 hides` |
| 9a4bb226 | `crop_thing(('most_colours', True))` |
| ae58858e | `thing law on (size): 6 except 3 kinds` |
| af22c60d | `symmetry (h+v) about its own centre fills what colour 0 hides` |
| be03b35f | `rot270 ▸ continue_pattern(((2, 5), (2, 5)))` |
| c663677b | `complete_pattern(0)` |
| ca8f78db | `complete_pattern(0)` |
| cd3c21df | `crop_thing(('rarest_colour', True))` |
| d19f7514 | `combine(('halves_tb', 'or', 4))` |
| d282b262 | `slide_things(left)` |
| d56f2372 | `the thing with symmetric=True` |
| e0fb7511 | `thing law on (size): 8 except 1 kind` |
| e133d23d | `combine(('lines', 'or', 2))` |
| e345f17b | `combine(('halves_lr', 'nor', 4))` |
| e66aafb8 | `symmetry (v) about its own centre fills what colour 0 hides, answer is the repaired patch` |
| e95e3d8e | `complete_pattern(0)` |
| f0afb749 | `upscale(2) ▸ marks around things by (): 1 kinds leave marks` |
| f4081712 | `symmetry (v) about its own centre fills what colour 3 hides, answer is the repaired patch` |
| f45f5ca7 | `things move by (colour): 4 kinds (steps)` |
| f5aa3634 | `the thing with shape_count=2` |
| f823c43c | `complete_pattern(6)` |

## ARC-AGI-2 evaluation: what it found

1 tasks solved; 4 where a program fitted every example but gave the wrong answer on the test (wrong generalisation); 115 with no program within budget.

| Task | Program Ultron found |
|---|---|
| 981571dc | `symmetry (h+v) about its own centre fills what colour 0 hides` |
