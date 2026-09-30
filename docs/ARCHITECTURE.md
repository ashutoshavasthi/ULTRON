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
  decides between them.
- **Inventing concepts** (`invention.py`, line discovery). When two actions
  undo each other and every state lies on one line through the empty state,
  Ultron treats the states past empty as a new kind of number: below zero. It
  also gets a new primitive, `down`, a step with no floor. This is how it
  invents negative numbers from a purse of coins and IOU notes (lesson 8).
  The words '-3' and 'negative three' are taught only afterwards.

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

## Running it

```bash
python -m ultron train            # train from scratch, save brain/ultron_brain.json, write reports/
python -m ultron show             # what Ultron knows
python -m ultron ask "what is 347 plus 1289?"
python -m ultron ask "find a given spring=S2 x=0.3 m=4"
python -m ultron why "3 + 2"      # checked proof
python -m ultron exam             # re-run held-out exams on the saved brain
python -m ultron blind blind/example_not_blind.txt   # score it on someone else's questions
python -m pytest                  # tests
```

## File map

```
ultron/brain/     dsl, synth, invariants, invention, curiosity, memory, perception, units, language, reasoner, brain
ultron/env/       toyworld, physics, dataworld, data/*.csv (real measurements, sources in headers)
ultron/trainer/   lessons (curriculum 0-9: 7 = noisy lab, 8 = owing, 9 = tough final exam), trainer
blind/            write your own blind test; `python -m ultron blind FILE` (mastery gate, naming after understanding)
ultron/judge/     exams (held-out + memoriser baselines), report
ultron/logic/     peano (rules from learned laws + proof checker)
brain/            Ultron's saved brain
reports/          report card, transcript, exam data, judge's verdict
```
