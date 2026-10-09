# ARC primitives: what Ultron can see and do with a grid

Every primitive is **generic**: it means the same thing in every task and would make
sense to a child looking at any picture. None was written for a particular task.
Parameters (colours, sizes) come from the task's own examples, never from known answers.

This list is counted, so a solver made of special cases would show here.

> **Frozen at 38 hand-written operations** (`ops.FROZEN`, enforced by
> `tests/test_arc.py::test_hand_written_operations_are_frozen`). From here on, new
> abilities come only from Ultron itself: library learning (`library.py`) turns pieces
> that recur in its own solved programs into new building blocks, kept only when they
> shorten the total description of what it has solved. Learned blocks live in
> `brain/arc_library.json`, each with the tasks it came from.

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

## Added after the freeze: perception of things, and laws learned per task

The 38 operations stay frozen. What was added is **perception**: the quantities Ultron
measures on a thing, listed and counted here. It is also **learning**: laws found from
each task's own examples by the same rule Ultron uses everywhere, the shortest
description that agrees with every example.

### Quantities of a thing (`objects.describe_things`): 13, plus "most / least"

| Quantity | Why it's generic |
|---|---|
| colour, size, height, width | Basic properties of any object |
| shape (the exact pattern), number of colours | What it looks like |
| holes (enclosed background) | Inside vs outside, again |
| touches the border | Where it is |
| symmetric, filled (a solid rectangle) | Regularity |
| how many things share its shape / its colour | Same and different |
| size rank, and "most / middle / least" for every count above | Comparison: the biggest, the most common |

### Laws learned from a task's own examples (`objects.py`)

| Law | What it says | Guard against fooling itself |
|---|---|---|
| thing law | A thing's new colour (or "stays") depends on its quantities | A default with exceptions is allowed only if it is really the rule; when two laws explain the examples equally well, both are kept as the two attempts |
| marks | What each kind of thing paints around itself: fixed marks, and rays to the edge or to the next thing | A kind seen once gives no evidence; a mark must be shown by two things; the law must compress the painted cells at least two to one |
| pick | Which thing is the answer, as a value of its quantities | Every thing with that value must give the same answer |
| moves | How each kind of thing moves: toward what stays put, slide, by its own size, or a step | Ranked by what each takes to say; a kind seen moving once gives no evidence |

| symmetry (`symmetry.py`) | The picture's own symmetry (a mirror, two mirrors, quarter turns, a diagonal) about its own centre, found where the cells it can see agree with their images, fills what is missing: blank, or hidden under a colour; optionally the answer is the repaired patch | The centre must be backed by at least half the visible cells; images that disagree, or a hidden cell with no visible image, give no answer; rival laws are the two attempts |
| where a colour is (`objects.py`) | The answer is the box around a colour (or what it holds inside), the colour named outright or chosen by a trait: drawn as a rectangle outline, a solid block, the most or least common | Exactly one colour may have the trait, else no answer |

| copies (`objects.py`) | Copies of one thing (the template, chosen by a value of its quantities) replace every other thing (the markers), centred on them or matching colours with them, optionally in the marker's colour | Exactly one thing may be the template; no markers, or an ambiguous anchor, gives no answer |
| lines between things (`objects.py`) | What fills a gap between two coloured cells on a row or column (a colour, the ends' own colour, or nothing) is a law of the two ends | The smallest key that explains every gap wins; a kind of gap never seen gives no answer |

| summary (`summary.py`) | The answer is about the picture: a colour (that of the thing a law singles out, or a class of the picture by one trait: symmetry, how many things, colours, its one shape), a row, column, diagonal or square as long as a count (things, coloured cells, cells of a colour), or one cell per uniform block | A class table must be shorter than its examples; an unseen kind of picture gives no answer |

Perception added for summaries (counted): a picture's symmetry, number of things and colours, its one shape; uniform blocks (runs of identical rows and columns).

Traits of a colour (perception, counted): drawn as an outline, drawn as a solid block, how common it is compared with the others.

In every case, a kind of thing never seen in the examples gets **no answer**, not a guess.
