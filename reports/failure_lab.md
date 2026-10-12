# The failure lab

Every experiment turns one dial until Ultron breaks. ✅ = still right, ❌ = broken. Regenerate with `python -m ultron stress`.

## program size

_How big a law can it find by search?_ Breaks at: **(a+1)(b+2)(a+b)**

| the law's size | what it did | |
|---|---|---|
| a+b | `merge(a, b)` | ✅ |
| a·b | `groups(a, b)` | ✅ |
| a·b+a | `groups(a, succ(b))` | ✅ |
| a·b+a+b | `pred(groups(succ(a), succ(b)))` | ✅ |
| a²+b | `merge(b, square(a))` | ✅ |
| (a+b)² | `square(merge(a, b))` | ✅ |
| a·b²+a | `groups(a, succ(square(b)))` | ✅ |
| a³+b² | `merge(square(b), groups(a, square(a)))` | ✅ |
| (a+1)(b+2)(a+b) | `nothing found` | ❌ |

Search is size-ordered and exhaustive: cost grows exponentially with the size of the law.

## library learning

_After sleeping on laws that share a piece nobody taught it, does it find laws bigger than its search can reach?_ Breaks at: **did not break**

| held-out law | what it did | |
|---|---|---|
| practice: 5 of 5 laws found; sleep | `piece1 = groups(succ(x1), succ(x2)) (saves 5); piece2 = piece1(x1, succ(x2)) (saves 1)` | ✅ |
| S(S(a,b),a)+S(a,b) | `piece1(a, piece2(b, a)) — 10 pieces written out` | ✅ |
| S(S(a,b),S(a,a)) | `piece1(square(succ(a)), piece1(a, b)) — 11 pieces written out` | ✅ |
| S(S(a,b),S(b,b)) | `piece1(square(succ(b)), piece1(a, b)) — 11 pieces written out` | ✅ |
| S(S(a,b),S(a,b))+a | `merge(a, square(succ(piece1(a, b)))) — 9 pieces written out` | ✅ |
| S(T(a,b),T(b,a)) | `piece1(piece2(a, b), piece2(b, a)) — 15 pieces written out` | ✅ |
| T(T(a,b),T(b,a)) | `piece2(piece2(a, b), piece2(b, a)) — 16 pieces written out` | ✅ |

Its search alone stops at 7 pieces. The held-out laws are compositions of the family's pieces (S = (x+1)(y+1), T = (x+1)(y+2)); S1 asks for laws of 12 pieces written out, within 60 s.

## intuition

_Does measuring description length against what its intuition expects cut search (S2, intuition alone)?_ Breaks at: **38 held-out laws (lab laws and unseen dreams)**

| held-out set | what it did | |
|---|---|---|
| 38 held-out laws (lab laws and unseen dreams) | `search 0.7x less with the prior; 1 lost, 4 longer` | ❌ |

Kept out of the brain until it pays: a wrong guess pushes a needed law to a dearer level, and search grows exponentially per level.

## wrong labels (programs)

_If some experiences are recorded wrongly, does it still find multiplication?_ Breaks at: **did not break**

| share of wrong records | what it did | |
|---|---|---|
| 0% wrong | `groups(a, b)` | ✅ |
| 5% wrong | `groups(a, b)` | ✅ |
| 10% wrong | `groups(a, b)` | ✅ |
| 20% wrong | `groups(a, b)` | ✅ |

## hidden causes and noise

_When the outcome depends on something unseen, or on nothing, does it refuse to claim a law?_ Breaks at: **did not break**

| case | what it did | |
|---|---|---|
| hidden cause | `no law (right)` | ✅ |
| pure noise | `no law (right)` | ✅ |

## few examples

_How few examples does it need to find a·b+a?_ Breaks at: **1 examples**

| examples | what it did | |
|---|---|---|
| 1 examples | `pred(square(b))` | ❌ |
| 2 examples | `groups(a, succ(b))` | ✅ |
| 3 examples | `groups(a, succ(b))` | ✅ |
| 4 examples | `groups(a, succ(b))` | ✅ |
| 6 examples | `groups(a, succ(b))` | ✅ |
| 8 examples | `groups(a, succ(b))` | ✅ |

Failing with very few examples is expected: many laws fit. The point is how fast it converges.

## compute vs data

_How does search time grow with more examples?_ Breaks at: **did not break**

| examples | what it did | |
|---|---|---|
| 20 examples | `3.8 s` | ✅ |
| 100 examples | `1.4 s` | ✅ |
| 400 examples | `1.0 s` | ✅ |

## noise

_How noisy can measurements be before F = m·a is lost?_ Breaks at: **did not break**

| noise per reading (known to it) | what it did | |
|---|---|---|
| ±0.5% | `F / (a·m)` | ✅ |
| ±1.0% | `F / (a·m)` | ✅ |
| ±2.0% | `F / (a·m)` | ✅ |
| ±5.0% | `F / (a·m)` | ✅ |
| ±10.0% | `F / (a·m)` | ✅ |
| ±20.0% | `F / (a·m)` | ✅ |

## noise unknown

_Not told how noisy its readings are, does it work the noise out and still find F = m·a?_ Breaks at: **±5%, no repeats**

| noise per reading (unknown to it) | what it did | |
|---|---|---|
| ±1%, repeated trials | `F / (a·m) (noise measured ±1.3%)` | ✅ |
| ±2%, repeated trials | `F / (a·m) (noise measured ±2.3%)` | ✅ |
| ±5%, repeated trials | `F / (a·m) (noise measured ±4.2%)` | ✅ |
| ±10%, repeated trials | `F / (a·m) (noise measured ±12.5%)` | ✅ |
| ±20%, repeated trials | `F / (a·m) (noise measured ±31.0%)` | ✅ |
| ±1%, no repeats | `F / (a·m)` | ✅ |
| ±2%, no repeats | `F / (a·m)` | ✅ |
| ±5%, no repeats | `nothing` | ❌ |
| ±10%, no repeats | `nothing` | ❌ |

## outliers

_If some readings are badly wrong (a slipped ruler), is F = m·a still found?_ Breaks at: **did not break**

| share of bad readings | what it did | |
|---|---|---|
| 0.0% bad readings | `F / (a·m)` | ✅ |
| 2.5% bad readings | `F / (a·m)` | ✅ |
| 5.0% bad readings | `F / (a·m)` | ✅ |
| 10.0% bad readings | `F / (a·m)` | ✅ |
| 20.0% bad readings | `F / (a·m)` | ✅ |

## irrelevant measurements

_If it also measures things that don't matter (colour, time of day...), does it still find F = m·a?_ Breaks at: **did not break**

| irrelevant quantities | what it did | |
|---|---|---|
| 0 irrelevant | `F / (a·m)` | ✅ |
| 2 irrelevant | `F / (a·m)` | ✅ |
| 4 irrelevant | `F / (a·m)` | ✅ |
| 6 irrelevant | `F / (a·m)` | ✅ |
| 10 irrelevant | `F / (a·m)` | ✅ |

## confounders

_When two things always move together, does it notice it can't tell which one matters (and design an experiment)?_ Breaks at: **did not break**

| case | what it did | |
|---|---|---|
| mass and a label always equal | `picked F / (a·c); ambiguity noticed: True` | ✅ |
| …and it may choose its experiments | `F / (a·c) → F / (a·m); 1 designed` | ✅ |

## magnitudes

_Does it work with tiny and huge numbers?_ Breaks at: **did not break**

| scale | what it did | |
|---|---|---|
| ×1e-12 | `F / (a·m)` | ✅ |
| ×1e-06 | `F / (a·m)` | ✅ |
| ×1 | `F / (a·m)` | ✅ |
| ×1e+06 | `F / (a·m)` | ✅ |
| ×1e+12 | `F / (a·m)` | ✅ |

## a changing world

_When the world changes under the same name, does it notice and update?_ Breaks at: **did not break**

| case | what it did | |
|---|---|---|
| stiffness 50 → 80 | `believes 80` | ✅ |

## kinds of law

_Which shapes of law can it explain, and then predict for a new object?_ Breaks at: **did not break**

| law | what it did | |
|---|---|---|
| settling (known kind) | `ρ(Δ(y))` | ✅ |
| straight line (known kind) | `ρ(Δ(y))` | ✅ |
| quadratic | `Δ(Δ(y))` | ✅ |
| oscillation | `y[n] = a1·y[n-1] + a2·y[n-2]` | ✅ |
| damped oscillation | `y[n] = a1·y[n-1] + a2·y[n-2]` | ✅ |
| logistic growth | `ρ(Δ(y^-1))` | ✅ |
| power law t^1.5 | `Δ(y^2/3)` | ✅ |

Its grammar: Δ, ρ, composed; applied to a power of the reading; and recurrences (the next reading a fixed mix of the last few).

## eyes

_How robust is its learned vision?_ Breaks at: **did not break**

| condition | what it did | |
|---|---|---|
| normal (8% noise) | `25/25 trays counted right` | ✅ |
| 16% noise | `25/25 trays counted right` | ✅ |
| 32% noise | `24/25 trays counted right` | ✅ |
| big things (r 4-6) | `25/25 trays counted right` | ✅ |
| faint things (30% brightness) | `25/25 trays counted right` | ✅ |
| touching (gap = diameter) | `25/25 trays counted right` | ✅ |
| overlapping (gap < diameter) | `20/25 trays counted right (merged blobs: a physical limit, reported only)` | ✅ |

## false laws

_On data with nothing to find, does it ever claim a law?_ Breaks at: **did not break**

| audit | what it did | |
|---|---|---|
| 50 program datasets with nothing to find | `0 false laws` | ✅ |
| 25 sequence worlds with nothing to find | `0 false laws` | ✅ |
| 50 measurement datasets with nothing to find | `0 false laws` | ✅ |
| 25 datasets of pure noise, noise not told | `0 false laws` | ✅ |
| 25 hidden causes (±5%) with repeated trials, noise not told | `0 false laws` | ✅ |

## words by pointing

_Does it still learn what words mean when the Trainer sometimes says the wrong word, or says less?_ Breaks at: **20% of sentences name the wrong thing**

| wrong words; sentences heard | what it did | |
|---|---|---|
| 0% of sentences name the wrong thing | `60/60 right (60/60 of its answers)` | ✅ |
| 5% of sentences name the wrong thing | `60/60 right (60/60 of its answers)` | ✅ |
| 10% of sentences name the wrong thing | `60/60 right (60/60 of its answers)` | ✅ |
| 20% of sentences name the wrong thing | `37/60 right (37/37 of its answers)` | ❌ |
| 30% of sentences name the wrong thing | `60/60 right (60/60 of its answers)` | ✅ |
| 120 sentences heard | `60/60 right (60/60 of its answers)` | ✅ |
| 60 sentences heard | `40/60 right (40/40 of its answers)` | ❌ |
| 40 sentences heard | `40/60 right (40/40 of its answers)` | ❌ |
| 20 sentences heard | `0/60 right (0/0 of its answers)` | ❌ |
| 10 sentences heard | `0/60 right (0/0 of its answers)` | ❌ |

A row passes at 57/60 (95%). The two dials are separate: the first breakpoint is the first row that fails.

## words for what happens

_Does it still learn words for events and for comparing when the Trainer sometimes says the wrong word, says less, or the camera is noisier?_ Breaks at: **20% of event sentences say the wrong word**

| wrong words; sentences heard; camera noise | what it did | |
|---|---|---|
| 0% of event sentences say the wrong word | `60/60 right (60/60 of its answers)` | ✅ |
| 10% of event sentences say the wrong word | `60/60 right (60/60 of its answers)` | ✅ |
| 20% of event sentences say the wrong word | `0/60 right (0/0 of its answers)` | ❌ |
| 30% of event sentences say the wrong word | `0/60 right (0/0 of its answers)` | ❌ |
| 50 event sentences heard | `60/60 right (60/60 of its answers)` | ✅ |
| 25 event sentences heard | `60/60 right (60/60 of its answers)` | ✅ |
| 12 event sentences heard | `33/60 right (33/33 of its answers)` | ❌ |
| camera 2 times as noisy | `50/60 right (50/50 of its answers)` | ❌ |
| camera 3 times as noisy | `33/60 right (33/33 of its answers)` | ❌ |
| 0% of comparing sentences say the wrong word | `60/60 right (60/60 of its answers)` | ✅ |
| 10% of comparing sentences say the wrong word | `60/60 right (60/60 of its answers)` | ✅ |
| 20% of comparing sentences say the wrong word | `15/60 right (15/15 of its answers)` | ❌ |

A row passes at 54/60 (90%). Event words were taught with 100 sentences and comparing words with 120 in the first rows.

## how words combine

_Does it still find how words combine when it mishears words, when the Trainer talks about another table, when a word has two meanings, or when it hears less?_ Breaks at: **20% of sentences have a word misheard**

| misheard words; wrong tables; two meanings; sentences heard | what it did | |
|---|---|---|
| 0% of sentences have a word misheard | `60/60 right (60/60 of its answers)` | ✅ |
| 20% of sentences have a word misheard | `34/60 right (34/34 of its answers)` | ❌ |
| 40% of sentences have a word misheard | `19/60 right (19/19 of its answers)` | ❌ |
| 20% of sentences are about another table | `60/60 right (60/60 of its answers)` | ✅ |
| 40% of sentences are about another table | `0/60 right (0/0 of its answers)` | ❌ |
| 'left' has two meanings (also 'above', half the time) | `35/60 right (35/35 of its answers)` | ❌ |
| 75 sentences heard | `25/60 right (25/25 of its answers)` | ❌ |
| 30 sentences heard | `0/60 right (0/0 of its answers)` | ❌ |

A row passes at 57/60 (95%). The grammar was found from 300 sentences in the first rows.

