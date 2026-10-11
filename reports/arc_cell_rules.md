# ARC: cell rules (work in progress, paused 2026-10-11)

**What it is.** `ultron/arc/rules.py`: a new law learned per task from the task's own
examples. Ultron describes each cell by generic things it sees (its colour and its
neighbours', the first colour in each of 8 directions, the mirrored cell, the thing it
belongs to and its size, whether it is shut in, its row and column) and finds the
shortest list of "if one or two facts hold, then a colour / the colour of something it
sees, otherwise a default" that gives every cell of every example. A list is believed
only if, learned without each example in turn, it predicts that example (leave-one-out).

**Measured on the training split (development only; the evaluation split was not opened):**

| | ARC-AGI-1 training | Answers right of given |
|---|---|---|
| Before | 35.38% (141.5 of 400) | 142 of 155 |
| With cell rules | **37.12%** (148.5 of 400) | 149 of 163 |

On its own (same-shape tasks only) the rule learner answers 45 training tasks, 41 right
and 4 wrong; 7 of the right ones were unsolved before.

**What limits it (where it stopped).** Of 262 same-shape training tasks, 167 have no rule
list within 8 rules of one or two facts (the facts are not enough), and 46 fit every
example but fail leave-one-out (they memorise), for example colour swaps where each
example shows different colours.

**Not yet done:** the evaluation split score, the ARC-AGI-2 held-out training check, and
richer facts (colour ranked by how common it is, inside a thing's box, periodic
position). Paused by the owner while the coding work runs.

Checks run: full pytest suite 111 passed. The ARC solver is not part of the curriculum or
the brain's retrain, so lessons and retrain are unaffected by this change.
