# Ultron on ARC-AGI

Official scoring (2 attempts per test output). Development uses the training split only; every evaluation run is logged in `reports/arc_runs.log`.

| Set | Split | Tasks | Score | Seconds | Budget (operations per task) |
|---|---|---|---|---|---|
| ARC-AGI-1 | training | 400 | **25.5%** (102.0) | 214.7 | 40000 |

## ARC-AGI-1 training: what it found

102 tasks solved; 11 where a program fitted every example but gave the wrong answer on the test (wrong generalisation); 287 with no program within budget.

| Task | Program Ultron found |
|---|---|
| 007bbfb7 | `fractal` |
| 00d62c1b | `fill_enclosed(4)` |
| 017c7c7b | `continue_pattern(((3, 2), (1, 1))) ▸ recolour 1→2` |
| 0520fde7 | `combine(('lines', 'and', 2))` |
| 05269061 | `complete_diagonal(0)` |
| 08ed6ac7 | `local law on (colour, order): 4 situations change colour` |
| 0ca9ddb6 | `marks around things by (colour): 2 kinds leave marks` |
| 0d3d703e | `recolour 1→5, 2→6, 3→4, 4→3, 5→1, 6→2, 8→9, 9→8` |
| 0dfd9992 | `complete_pattern(0)` |
| 1190e5a7 | `count_parts` |
| 178fcbfb | `lines_through((2, 'v')) ▸ local law on (colour, row): 4 situations change colour` |
| 1b2d62fb | `combine(('lines', 'nor', 8))` |
| 1cf80156 | `crop_content` |
| 1e0a9b12 | `gravity(down)` |
| 1f85a75f | `crop_thing(('largest', False))` |
| 1f876c06 | `connect(diagonals)` |
| 22168020 | `connect(rows)` |
| 23b5c85d | `crop_thing(('smallest', False))` |
| 253bf280 | `local law on (colour, line): 2 situations change colour` |
| 29ec7d0e | `complete_pattern(0)` |
| 2dc579da | `pick_part(odd_one)` |
| 2dee498d | `continue_pattern(((1, 1), (1, 3)))` |
| 3428a4f5 | `combine(('lines', 'xor', 3))` |
| 3618c87e | `keep_thing(('largest', False)) ▸ local law on (colour, n4): 2 situations change colour` |
| 3906de3d | `gravity(up)` |
| 3af2c5a8 | `mirror_tile(both)` |
| 3c9b0459 | `rot180` |
| 4258a5f9 | `frame_things(1)` |
| 42a50994 | `remove_specks(1)` |
| 4347f46a | `hollow_things` |
| 445eab21 | `gravity(right) ▸ continue_pattern(((1, 5), (1, 5))) ▸ recolour 6→7, 7→8` |
| 484b58aa | `complete_pattern(0)` |
| 496994bd | `symmetrize(v)` |
| 4c4377d9 | `flip_v ▸ mirror_tile(v)` |
| 50cb2852 | `hollow_things ▸ fill_enclosed(8)` |
| 543a7ed5 | `fill_enclosed(4) ▸ frame_things(3)` |
| 6150a2bd | `rot180` |
| 62c24649 | `mirror_tile(both)` |
| 6430c8c4 | `combine(('lines', 'nor', 3))` |
| 67385a82 | `thing law on (size): 8 except 1 kind` |
| 67a3c6ac | `flip_h` |
| 67e8384a | `mirror_tile(both)` |
| 68b16354 | `flip_v` |
| 694f12f3 | `local law on (colour, count8, rank): 2 situations change colour` |
| 6c434453 | `local law on (colour, count8, rank): 4 situations change colour` |
| 6d0aefbc | `mirror_tile(h)` |
| 6d75e8bb | `frame_things(2) ▸ local law on (colour, line): 4 situations change colour` |
| 6e82a1ae | `thing law on (size): 3 kinds of thing` |
| 6f8cd79b | `outline(8)` |
| 6fa7a44f | `mirror_tile(v)` |
| 7468f01a | `flip_h ▸ crop_content` |
| 74dd1130 | `transpose` |
| 7b6016b9 | `fill_enclosed(2) ▸ recolour 0→3` |
| 810b9b61 | `thing law on (holes): 3 except 1 kind` |
| 868de0fa | `fill_enclosed(2) ▸ thing law on (size): keep except 3 kinds` |
| 8be77c9e | `mirror_tile(v)` |
| 8f2ea7aa | `crop_content ▸ fractal` |
| 913fb3ed | `marks around things by (colour): 3 kinds leave marks` |
| 9172f3a0 | `upscale(3)` |
| 94f9d214 | `combine(('halves_tb', 'nor', 2))` |
| 95990924 | `marks around things by (colour): 1 kinds leave marks` |
| 963e52fc | `continue_pattern(((1, 1), (2, 1)))` |
| 99b1bc43 | `combine(('lines', 'xor', 3))` |
| 9dfd6313 | `transpose` |
| a416b8f3 | `tile((1, 2))` |
| a5313dff | `fill_enclosed(1)` |
| a61f2674 | `thing law on (size_rank): 3 kinds of thing` |
| a699fb00 | `local law on (colour, line): 2 situations change colour` |
| a740d043 | `crop_content ▸ recolour 1→0` |
| ae3edfdc | `frame_things(7) ▸ local law on (colour, line, orth_set): 16 situations change colour` |
| ae4f1146 | `keep_colour(1) ▸ crop_thing(('largest', True)) ▸ recolour 0→8` |
| aedd82e4 | `thing law on (size): keep except 1 kind` |
| b1948b0a | `recolour 6→2` |
| b230c067 | `thing law on (shape_count): 2 kinds of thing` |
| b2862040 | `thing law on (holes): 8 except 1 kind` |
| b6afb2da | `local law on (colour, count8): 3 situations change colour` |
| bb43febb | `local law on (colour, count8): 1 situations change colour` |
| bdad9b1f | `lines_through((2, 'h')) ▸ local law on (colour, col): 2 situations change colour` |
| be94b721 | `crop_thing(('largest', False))` |
| c0f76784 | `fill_enclosed(6) ▸ thing law on (size): keep except 2 kinds` |
| c3f564a4 | `complete_pattern(0)` |
| c59eb873 | `upscale(2)` |
| c8f0f002 | `recolour 7→5` |
| c9e6f938 | `mirror_tile(h)` |
| ce22a75a | `frame_things(1) ▸ recolour 5→1` |
| ce4f8723 | `combine(('lines', 'or', 3))` |
| d2abd087 | `thing law on (size): 1 except 1 kind` |
| d364b489 | `marks around things by (colour): 1 kinds leave marks` |
| d511f180 | `recolour 5→8, 8→5` |
| d5d6de2d | `fill_enclosed(3) ▸ recolour 2→0` |
| d90796e8 | `local law on (colour, orth_set): 2 situations change colour` |
| dae9d2b5 | `combine(('halves_lr', 'or', 6))` |
| ded97339 | `local law on (colour, line): 2 situations change colour` |
| e3497940 | `symmetrize(h) ▸ pick_part(first)` |
| e8593010 | `thing law on (size): 3 kinds of thing` |
| e98196ab | `overlay_parts` |
| ea32f347 | `thing law on (size_rank): 3 kinds of thing` |
| ed36ccf7 | `rot90` |
| f25fbde4 | `crop_content ▸ upscale(2)` |
| f25ffba3 | `symmetrize(v)` |
| f2829549 | `combine(('lines', 'nor', 3))` |
| fafffa47 | `combine(('halves_tb', 'nor', 2))` |
