# Ultron on ARC-AGI

Official scoring (2 attempts per test output). Development uses the training split only; every evaluation run is logged in `reports/arc_runs.log`.

| Set | Split | Tasks | Score | Seconds | Budget (operations per task) |
|---|---|---|---|---|---|
| ARC-AGI-1 | training | 400 | **11.0%** (44.0) | 278.8 | 40000 |

## ARC-AGI-1 training: what it found

44 tasks solved; 3 where a program fitted every example but gave the wrong answer on the test (wrong generalisation); 353 with no program within budget.

| Task | Program Ultron found |
|---|---|
| 00d62c1b | `fill_enclosed(4)` |
| 0d3d703e | `recolour 1→5, 2→6, 3→4, 4→3, 5→1, 6→2, 8→9, 9→8` |
| 1cf80156 | `crop_content` |
| 1e0a9b12 | `gravity(down)` |
| 1f85a75f | `crop_thing(('largest', False))` |
| 23b5c85d | `crop_thing(('smallest', False))` |
| 2dc579da | `pick_part(odd_one)` |
| 3906de3d | `gravity(up)` |
| 3af2c5a8 | `mirror_tile(both)` |
| 3c9b0459 | `rot180` |
| 42a50994 | `remove_specks(1)` |
| 496994bd | `symmetrize(v)` |
| 4c4377d9 | `flip_v ▸ mirror_tile(v)` |
| 6150a2bd | `rot180` |
| 62c24649 | `mirror_tile(both)` |
| 67a3c6ac | `flip_h` |
| 67e8384a | `mirror_tile(both)` |
| 68b16354 | `flip_v` |
| 6d0aefbc | `mirror_tile(h)` |
| 6f8cd79b | `outline(8)` |
| 6fa7a44f | `mirror_tile(v)` |
| 7468f01a | `flip_h ▸ crop_content` |
| 74dd1130 | `transpose` |
| 7b6016b9 | `fill_enclosed(2) ▸ recolour 0→3` |
| 88a62173 | `pick_part(odd_one)` |
| 8be77c9e | `mirror_tile(v)` |
| 9172f3a0 | `upscale(3)` |
| 9565186b | `recolour_all(5)` |
| 9dfd6313 | `transpose` |
| a416b8f3 | `tile((1, 2))` |
| a5313dff | `fill_enclosed(1)` |
| a740d043 | `crop_content ▸ recolour 1→0` |
| ae4f1146 | `keep_colour(1) ▸ crop_thing(('largest', True)) ▸ recolour 0→8` |
| b1948b0a | `recolour 6→2` |
| be94b721 | `crop_thing(('largest', False))` |
| c59eb873 | `upscale(2)` |
| c8f0f002 | `recolour 7→5` |
| c9e6f938 | `mirror_tile(h)` |
| d511f180 | `recolour 5→8, 8→5` |
| d5d6de2d | `fill_enclosed(3) ▸ recolour 2→0` |
| dae9d2b5 | `combine(('halves_lr', 'or', 6))` |
| ed36ccf7 | `rot90` |
| f25fbde4 | `crop_content ▸ upscale(2)` |
| f25ffba3 | `symmetrize(v)` |
