# The failure lab

Every experiment turns one dial until Ultron breaks. ✅ = still right, ❌ = broken. Regenerate with `python -m ultron stress`.

## program size

_How big a law can it find by search?_ Breaks at: **(a+1)(b+2)(a+b)**

| the law's size | what it did | |
|---|---|---|
| a+b | `get_paid(a, b)` | ✅ |
| a·b | `groups(a, b)` | ✅ |
| a·b+a | `groups(a, succ(b))` | ✅ |
| a·b+a+b | `pred(groups(succ(a), succ(b)))` | ✅ |
| a²+b | `get_paid(b, square(a))` | ✅ |
| (a+b)² | `square(get_paid(a, b))` | ✅ |
| a·b²+a | `groups(a, succ(square(b)))` | ✅ |
| a³+b² | `get_paid(square(b), groups(a, square(a)))` | ✅ |
| (a+1)(b+2)(a+b) | `nothing found` | ❌ |

Search is size-ordered and exhaustive: cost grows exponentially with the size of the law.

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
| 20 examples | `6.3 s` | ✅ |
| 100 examples | `7.9 s` | ✅ |
| 400 examples | `20.1 s` | ✅ |

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

_How robust is its learned vision?_ Breaks at: **16% noise**

| condition | what it did | |
|---|---|---|
| normal (8% noise) | `25/25 trays counted right` | ✅ |
| 16% noise | `1/25 trays counted right` | ❌ |
| 32% noise | `0/25 trays counted right` | ❌ |
| big things (r 4-6) | `0/25 trays counted right` | ❌ |
| faint things (30% brightness) | `2/25 trays counted right` | ❌ |
| touching (gap = diameter) | `19/25 trays counted right` | ❌ |
| overlapping (gap < diameter) | `14/25 trays counted right (merged blobs: a physical limit, reported only)` | ✅ |

## false laws

_On data with nothing to find, does it ever claim a law?_ Breaks at: **did not break**

| audit | what it did | |
|---|---|---|
| 50 program datasets with nothing to find | `0 false laws` | ✅ |
| 25 sequence worlds with nothing to find | `0 false laws` | ✅ |
| 50 measurement datasets with nothing to find | `0 false laws` | ✅ |
| 25 datasets of pure noise, noise not told | `0 false laws` | ✅ |
| 25 hidden causes (±5%) with repeated trials, noise not told | `0 false laws` | ✅ |

