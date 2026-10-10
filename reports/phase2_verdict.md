# Judge's verdict: Phase 2 (inventing concepts, generally)

*Written by Claude, as Ultron's trainer and judge, after running lessons 0–16,
every exam, and `python -m ultron experiment`. Metrics are in
[`report_card.md`](report_card.md).*

## Verdict

**Phase 2 is complete. Every imperfection I found that can be fixed within this
phase has been fixed.** All 17 lessons pass their held-out exams on the first
attempt. What remains open is either not mine to supply (a blind test) or the
research frontier (letting Ultron invent new *kinds* of hypothesis). Both are
named at the end, because "perfect" would be a false claim.

## What Ultron invents, and with how few mechanisms

| Mechanism | Inventions | Proof it is general |
|---|---|---|
| **Shape discovery** (`invention.py`): walk the world's states with its own laws and look at the shape | **negative numbers** (a line through zero), **clock numbers** (a cycle), **fractions** (a finer line) | One module, three kinds of number, no concept-specific code. For fractions it even works out *by testing* which input of its law is the count, the kind of piece and the wholes. |
| **Numbers in the gaps** (`gaps.py`) | **irrational numbers**: "what power 2 equals 2" is always squeezed between two piles, never on one | Invented by reasoning in lesson 13. Confirmed by the world in lesson 15: the tile's diagonal predicts every ruler reading, at 1,000 marks too, without ever being measured there. |
| **Hidden quantities** (`invariants.py`): sums of any number of terms, coefficients fitted | **energy**: y + v²/2g, then y + v²/2g + (k/2mg)·c² with a spring | The spring coefficient matched the hidden true value exactly. It answers never-trained questions: balls thrown up, how far a spring squashes, how high a spring launches. |
| **Compression** (`compression.py`): "this law is that law, repeated" | **powers**, predicted in lesson 3 and confirmed in lesson 13 | 0 programs searched against 130,758 without compression. It declines to predict the next rung, because powers aren't symmetric. |
| **Laws run on amounts** (`amounts.py`) | **roots, logarithms, negative and fractional powers**, never taught | "what power 2 equals 81" = 9, "2 power what equals 1024" = 10, "3 power -2" = 1/9, √2 between 141/100 and 71/50 |

## Imperfections found in Phase 2, and what happened to them

| Imperfection | Fix |
|---|---|
| Fractions had their own mechanism | Fractions are now a shape (a *finer line*) found by the same shape discovery as negatives and clock numbers, with no hard-coded law names |
| Energy could only have two parts | Hidden quantities have any number of parts; spring energy was found exactly |
| Irrational numbers didn't exist for Ultron | Invented by reasoning (numbers in the gaps), then confirmed by measuring a tile's diagonal |
| Its wheel law was odd (it reused the purse law) | Among equally short explanations, it prefers the one that borrows fewer laws from its library (borrowing costs more description). The law is now "if slot is 5 then 0 else slot + 1" |
| REPEAT was trusted after one example, and assumed everywhere | Predictions are candidate explanations kept in mind and *tested first*. It calls a fit on 1–2 experiences "only a suspicion", and it counts its evidence honestly |
| Designing experiments sometimes hurt | It prefers rich situations over degenerate ones like "0 groups of 1". It needs 29 vs 34 experiences (helpful teacher) and 31 vs 37 (random teacher) compared with watching, and only it can learn what a biased teacher never shows |
| Slow answers | It counts on from the bigger number for laws it checked are symmetric, reuses coarse pins, and only tries piece sizes that fit evenly |

## What remains, honestly

1. **Counting arithmetic caps precision.** Ultron multiplies by counting, so it
   pins √2 to hundredths quickly, but cube roots take a second or two. That is a
   genuine limit of a mind that only counts. It is also the natural next
   invention: place-value ("column") arithmetic, which would make its own
   numerals do the work.
2. **Repeating a fractional number of times.** "2 power what equals 3" is
   refused. The answer is between 1 and 2, and Ultron has no idea what doing
   something "1.58 times" means. That's a real concept, not a bug.
3. **The kinds of hypothesis are still mine.** Shapes, sums of terms, REPEAT,
   gaps: Ultron invents *concepts* with them, but it can't invent a new *kind of
   hypothesis*. That is the open research frontier, not something one more
   patch fixes.
4. **The blind test.** I wrote every exam. Only questions written by someone
   else can prove all of this.

## Grade

**Phase 2: complete.** Ultron invented negative numbers, clock numbers,
fractions, irrational numbers, energy with any number of parts, and powers
before meeting them. It uses a handful of general mechanisms, and every
invention is tested on problems it has never seen. The four items above are
where Phase 3 begins.
