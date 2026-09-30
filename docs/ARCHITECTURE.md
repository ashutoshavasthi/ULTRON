# How Baby Ultron works

Ultron is a **Brain** living in an **Environment**, taught by a **Trainer** and
examined by a **Judge**. There is no neural network and no large dataset. It
learns from a few dozen experiences per lesson by searching for the *simplest
law that explains all of them*.

```
 TRAINER  sets up scenes · names things (only after understanding) · gates on exams
    │ scenes / words                                  ▲ answers + reasons
    ▼                                                 │
 ENVIRONMENT  ── observations ──►  BRAIN
  ToyWorld      ◄── choices ──      perception → memory → hypothesis engines → library
  PhysicsSandbox                    curiosity (learning progress) · language · reasoner
  DataWorld (real data)
                                  JUDGE  held-out exams · memoriser baselines · report card
```

## The learning loop (`ultron/brain/brain.py`)

For every experience:
1. **Predict** the outcome with the current best law.
2. **Observe** what the world actually does.
3. **Compare.** If the prediction was wrong, that's a surprise.
4. **Revise.** On a surprise, search all memories for a new simplest law.
5. **Store** the experience. After 8 correct predictions in a row, a
   discrete law is *confirmed* and added to the library as a new building
   block.

## Two hypothesis engines

| Engine | Used for | How it works |
|---|---|---|
| Program synthesis (`synth.py`) | counting, adding, multiplying, place value | Writes every program of size 1, then 2, and so on. Programs that behave identically on everything seen count as one. The first program that explains all memories is a shortest one. Confirmed laws cost size 1, which is why learning compounds. |
| Invariant search (`invariants.py`) | physics, real data | Tries products of powers of measured quantities, simplest first, looking for one that stays constant. If it's constant within each object but differs between objects, a new hidden property is invented. Minimum description length decides between the two options. Conservation laws: a per-object quantity whose total is unchanged by an event. |

Both engines are deterministic: the same experiences always give the same law.

Four more principles govern how laws are used and refined:
- **Noisy instruments.** Each instrument states its precision. A candidate
  law may vary by up to 2 × (sum of |powers|) × precision, which is error
  propagation.
- **Refinement.** Constants are re-averaged over all evidence as it
  accumulates.
- **Outside experience.** A law generalises across magnitude, but not to a
  situation that is new in kind: an input relation never once observed (taking
  away more than there is), or a system or object never observed (Saturn, a new
  spring). In those cases Ultron declines and explains why.
- **Reasoning backwards.** An inverse question ("what times 4 equals 20") is
  answered by trying candidates with the law itself.

## Trust, experiments and invention

- **Trust.** A measured law stays *tentative* until it has predicted 3 new
  experiences, then becomes *established*. If an established law fails,
  Ultron notes its doubt and searches again. Discrete laws are confirmed
  after 8 correct predictions in a row. Conservation laws are tentative until
  they have held for 3 events.
- **Designing experiments** (`Brain.propose`). The search also returns
  *rival* programs that explain the same experiences. When they disagree
  about some situation Ultron could set up, it sets that one up, so the world
  decides between them. When they all agree, it tries a *kind* of situation it
  has never met. This is how it learns what a biased teacher never shows it.
- **Amounts between numbers** (`amounts.py`). From two bakery laws
  ("k pieces of an n-cut balance w cakes when k = w groups of n"; "re-cutting
  an n-cut into m gives an n·m-cut"), Ultron notices amounts that balance no
  whole number of cakes, and invents fractions. Sameness, plus, minus and times
  on amounts are all worked out with its own laws, by re-cutting to a common
  kind of piece. Division is its times law run backwards: it brackets the
  answer, then halves the range.
- **Doubt.** A confirmed law that fails is doubted. Ultron keeps playing
  (instead of getting bored) until a replacement is confirmed.
- **Undoing** (`find_inverses`, `dsl.iterate`). Once numbers below zero
  exist, Ultron imagines with its laws to find which steps undo which ("pay
  undoes merge"). Repeating a step a below-zero number of times then means
  undoing it that many times. This gives, for example, (-2) × (-3) = 6.
- **Inventing concepts** (`invention.py`, line discovery). When two actions
  undo each other and every state lies on one line through the empty state,
  Ultron treats the states past empty as a new kind of number: below zero. It
  also gets a new primitive, `down`, a step with no floor. This is how it
  invents negative numbers from a purse of coins and IOU notes (lesson 8).
  The words '-3' and 'negative three' are taught only afterwards.

## Phase 2: general invention

| Mechanism | File | What it does | Inventions |
|---|---|---|---|
| Shape discovery | `invention.py` | Walks the world's states with its own laws: a cycle, a line through zero, a half-line, or a *finer* line (roles of its law's inputs found by testing) | negative numbers (line), clock numbers (cycle), fractions (finer line) |
| Numbers in the gaps | `gaps.py` | An inverse question no pile of pieces answers, yet always squeezed between two piles: a number in a gap, pinned as tightly as its counting allows (effort budget in counting steps) | irrational numbers (√2 = a tile's diagonal) |
| Hidden quantities | `invariants.py` (`search_sum_invariant`) | When no product stays constant, tries sums of 2, then 3 terms with least-squares coefficients, constant within each run | energy (and spring energy) |
| Compression | `compression.py` | Finds "this law is that law, repeated" (REPEAT) in its library; predicts the next law; stops where the pattern becomes ambiguous | powers (predicted 10 lessons early) |
| Laws on amounts | `amounts.py` (`evaluate_amount`) | Runs any of its programs on fractions; a below-zero number of repeats means undoing | roots, logarithms, negative and fractional powers |

Also in Phase 2:
- Experiment design prefers *rich* situations (not "0 groups of 1").
- Symmetric laws "count on from the bigger number".
- Among equally short explanations, prefer the one borrowing fewer library laws.
- Predictions are candidate explanations: tested first, trusted only after 3 fits.
- The program language gained "if ... then ... else" and one-input laws.

## Closing Phase 2's gaps

| Gap | File | Fix |
|---|---|---|
| Counting is slow and imprecise | `columns.py` | From its place-value law it checks four identities (columns add, ten carries, times spreads, a 0 is times ten) and builds column methods from its own single-digit facts, known by heart once counted. A column method is used for a law only after it agrees with the law on 60 examples. Its laws of repeating also let it square: a^(2k) = (a^k)². 20-digit products are exact; training takes 29 s instead of 90 s. |
| "Repeat 1.58 times" meant nothing | `compression.py` (`look_for_exponent_laws`) | It checks, with its own laws, that repeating p times then q more is repeating p+q times, and that repeating p times, done q times, is repeating p·q times. The only meaning of "repeat 1/2 time" that keeps those laws true is "whatever, repeated twice, is repeating once", so fractional powers and logarithms become questions about whole repeats. |
| No new kind of hypothesis | `metalaws.py` | Its own invented properties (each spring's stiffness) become data, and it runs its hypothesis engine one level up: stiffness × coils = 600. That is a law about a law, and it predicts springs it has never stretched. It is still composition of the kinds it has, not a new kind. |
| No blind test | `blind/SYLLABUS.md` | A public syllabus (what it experienced, how to ask) that independent examiners write tests from without seeing code, tests or exams. |

The reasoner also answers questions about two moments: energy along a run
(start values written `y0`, `v0`, `c0`) and momentum across a collision, solving
for any one unknown.

## Phase 3: senses, new kinds of explanation, a minimal body

| Part | File | What it does |
|---|---|---|
| Camera | `senses/camera.py`, `senses/world.py` | The world as grayscale pixels only: sensor noise (8%), blur, uneven light, a camera that shakes a pixel, spoiled frames (2%). Trays, a push table, a spring stand, a valley (a finer 96-pixel camera), floors to kick pucks on. The true state stays with the simulator. |
| Eyes | `senses/eyes.py` | A 3-layer convolutional network (3×3 filters, 1→8→8→1), forward and backward passes written in numpy, trained with Adam from **touch**: while handling things, its hands say where each thing is (lesson 19). Local peaks of its map are things; the threshold is the one that best matched touch. It looks again when two glances disagree. |
| Measuring | `senses/measure.py` | Positions are read against a ruler in the same picture (a line through all its marks), so shaking doesn't matter. Robust fits drop bad frames. Each reading carries the uncertainty Ultron measured itself. |
| Noise-aware laws | `invariants.py` (`_noise_check`) | With self-measured uncertainties, a sum of terms is accepted only when its leftovers are noise-sized (median z ≤ 1.5, ≤ 10% beyond 4σ). Wrong forms (y + c·v, y + c·v³) are rejected. |
| Kinds of explanation | `kinds.py` | Kinds are data: a transform from a small grammar (Δ, ρ, composed; Δy/Δx) and a scope (global, per object). When no innate kind fits, it searches the grammar shortest first and keeps the winner as a new kind, which it tries first next time. `brain.inventing = False` is the ablation. |
| Body | `body.py` | To reach a goal it runs its law backwards. On a floor it never touched, it makes a cautious first try (aimed at half the distance), treats what it sees as a measurement of that floor's constant, and plans again. |

Lessons: 19 handling things, 20 seeing numbers, 21 watching motion, 22 cooling cups,
23 bouncing/charging/hanging/burning/wandering, 24 using what it knows, 25 exam.
Everything is deterministic (numpy on one thread; the eyes' weights live in the
brain file).

What stays hand-made in Phase 3: the grammar of kinds (Δ, ρ, composition, two
scopes), the network's shape, the camera simulator, and the idea of looking for
peaks. The kinds themselves, the eyes' weights and threshold, the laws, and each
floor's friction are learned.

## Curiosity (`curiosity.py`)

For each kind of experiment, Ultron tracks how fast its prediction error is
falling:
- **Falling:** keep going.
- **Zero:** mastered, move on.
- **Flat and high:** unlearnable noise, give up.

This is why it ignores the random lamp panel.

## Language (`language.py`, `reasoner.py`)

Words are attached only to things Ultron already has:
- **Quantities** it can count ("seven", "7").
- **Its own laws** ("plus" is whichever law reproduces the Trainer's
  demonstrations, including argument order).
- **Innate relations** ("equals").

Answers carry the chain of laws used. `why` produces Peano proofs whose rules
are derived from Ultron's own programs and checked independently
(`ultron/logic/peano.py`).

## What is hand-designed (innate) vs learned

| Innate (designed by me) | Learned by Ultron |
|---|---|
| counting by tally, `succ`, `pred`, `eq`, `lt`, `not`, `and`, "repeat n times" | object permanence, same-number, addition, subtraction, multiplication, place value |
| power-product form for measurements; instruments and their units | F = m·a, spring stiffness (invented property), momentum and energy conservation, Kepler's 3rd law, Boyle's law |
| curiosity rule, confirmation rule, reading marks left-to-right | which word means which law; every constant and every property value |
| line discovery (the *ability* to notice a line of states) | negative numbers, the `down` step, paying and being paid below zero |
| noticing amounts that balance no whole number | fractions, their sameness and arithmetic, 'divided' |

## Running it

```bash
python -m ultron train            # train from scratch (~60 s; numpy needed from lesson 19), save brain/ultron_brain.json, write reports/
python -m ultron show             # what Ultron knows
python -m ultron ask "what is 347 plus 1289?"
python -m ultron ask "find a given spring=S2 x=0.3 m=4"
python -m ultron why "3 + 2"      # checked proof
python -m ultron exam             # re-run held-out exams on the saved brain
python -m ultron blind blind/example_not_blind.txt   # score it on someone else's questions
python -m ultron look pic.npy     # what its eyes see in a picture
python -m ultron ask "find rest given T@0=80 T@1=70 T@2=62"
python -m pytest                  # tests
```

## File map

```
ultron/brain/     dsl, synth, invariants, invention, amounts, gaps, compression, columns, metalaws, kinds, body, curiosity, memory, perception, units, language, reasoner, brain
ultron/env/       toyworld, physics, dataworld, data/*.csv (real measurements, sources in headers)
ultron/trainer/   lessons: Phase 1 = 0-10 (7 noisy lab, 8 owing, 9 sharing cakes, 10 final exam);
                  Phase 2 = 11 wheel, 12 hills and valleys, 13 growing, 14 hills and a spring,
                  15 the diagonal of a tile, 16 Phase 2 final exam;
                  closing the gaps = 17 coiled springs, 18 exam (columns, fractional repeats);
                  Phase 3 = 19-21 senses, 22-23 new kinds, 24 acting, 25 exam (senses_lessons.py)
ultron/senses/    camera, eyes (learned CNN), world (visual worlds), measure
blind/            SYLLABUS.md (public), independent examiners' tests; write your own; `python -m ultron blind FILE` (mastery gate, naming after understanding)
ultron/judge/     exams (held-out + memoriser baselines), report
ultron/logic/     peano (rules from learned laws + proof checker)
brain/            Ultron's saved brain
reports/          report card, transcript, exam data, judge's verdict
```
