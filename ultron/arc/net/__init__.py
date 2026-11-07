"""Engine 2: Ultron's own network (docs/PLAN.md, M2).

A small recursive network, in the spirit of TRM (arXiv 2510.04871), that Ultron trains
itself, from scratch, and that answers a puzzle directly instead of writing a program
for it. Nothing is pretrained. It learns from the examples given in puzzles (never the
answers of the puzzles it is tested on), from augmented copies of them, and from the
puzzles it dreams up in its own language (arc/dreams.py).

    data.py    puzzles as token grids, augmentations, the training set (with its guard)
    model.py   the recursive network
    train.py   training, checkpoints, answering with votes across augmentations
"""
