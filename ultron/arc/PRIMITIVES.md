# ARC primitives: what Ultron can see and do with a grid

Every primitive is **generic**: it means the same thing in every task and would make
sense to a child looking at any picture. None was written for a particular task.
Parameters (colours, sizes) come from the task's own examples, never from known answers.

This list is counted, so a solver made of special cases would show here.

## Perception (`grid.py`): 5

| Primitive | Why it's generic |
|---|---|
| background (the commonest colour) | Every picture has a ground |
| things: connected pieces, single- or multi-colour, 4- or 8-connected | Objects as cohesive pieces (the Spelke principle that infants use) |
| a thing's box, size, colour and number of colours | Basic properties of any object |
| separator lines (a colour found only on full rows or columns) | Pictures divided into panels |
| halves | Left/right and top/bottom |

## Operations (`ops.py`): 25

| Operation | Why it's generic |
|---|---|
| rot90, rot180, rot270, flip_v, flip_h, transpose, antitranspose | The symmetries of a square |
| crop_content | "Just the part that has something in it" |
| crop_thing / keep_thing (by: largest, smallest, rarest colour, commonest colour, top, bottom, left, right, most colours, biggest box) | Attending to the one thing that stands out, by a property every object has |
| remove_specks | Ignoring noise |
| upscale, downscale | Size |
| tile, mirror_tile | Repetition and reflection |
| recolour_all, keep_colour, remove_colour | Colour as a property you can change or attend to |
| fill_enclosed | Inside vs outside |
| gravity | Things fall |
| outline | Edges and borders |
| symmetrize | Completing a symmetric picture |
| combine (and, or, xor, only-left, neither) | Comparing two panels cell by cell |
| pick_part (first, last, odd one out, most or least filled) | Choosing among panels |
| overlay_parts | Stacking panels |

## Learned per task: 1

| | |
|---|---|
| colour mapping | One consistent recolouring that the task's own examples determine |

## Search (`solve.py`)

Programs are chains of operations, tried shortest first. A program is kept only if it
maps **every** training input to its output exactly. Programs that do the same thing to
every example are kept once. The budget is in operations, not time, so results are
identical on any machine.

## Added in step 1e (from training-split failures)

| Operation | Why it's generic |
|---|---|
| complete_pattern | A picture made of a repeating tile with some cells covered: find the repeat and uncover them |
| extend_rays | Lines continue until they meet something |
| local laws (`cells.py`) | A cell's new colour depends on what it sees around it; the smallest set of features that makes one consistent table wins |
| background is a property of the task (its commonest colour across all examples) | One ground for a whole set of pictures |
| fractal | A picture made of copies of itself |
| connect | Same-coloured cells on one line are joined |
| lines_through | A mark draws a line across the whole picture |
| complete_diagonal | Repetition along diagonals |
| continue_pattern | A repeating picture continued to a new size |
| count_parts, count_things | Counting panels and things |
| cell features: neighbour colour sets (orthogonal, diagonal), uniform row or column, size order of the thing | What a cell can see around it |
| each_thing (flip, rotate or transpose every thing in place) | "Each one does the same" |
| slide_things | Things move as wholes until they bump into something |
| frame_things, hollow_things | Borders around things; things as outlines |
