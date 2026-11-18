# Research: what is known, and the ground nobody holds

*Written 2026-11-13 for the `ultron-final` branch. It replaces the reading behind the old plan
(now [history/PLAN_M1_M2.md](history/PLAN_M1_M2.md)). Each source below says how it was read:
**full** (the paper's text), **part** (the first part of the text plus a machine summary of the
rest), or **abstract**. Numbers are quoted as the source gives them.*

## The short version

1. **The old checkpoint is taken.** Pretrained commercial models are at about 95% on ARC-AGI-2
   and 81% on ARC-AGI-3 on the official leaderboard. A coding-agent harness on such a model
   reports 100% on the 25 public ARC-AGI-3 games. "Human level on ARC" is no longer a first.
2. **From scratch, nothing is close.** With no pretrained model the best results are about 45% on
   ARC-AGI-1 and about 8% on ARC-AGI-2. Ultron is at 12.75% and 0.83%.
3. **Every from-scratch success fits each puzzle separately, by gradient descent, at test time.**
   What is fitted is a vector per puzzle (TRM, HRM, Latent Program Network) or a whole small
   network per puzzle (CompressARC). None of them comes away with a reusable, named concept.
4. **Symbolic library learning only abbreviates.** DreamCoder, Stitch and Ultron's own word
   learning compress programs they could already write. None tests whether a learned word does
   something the base language could not.
5. **One recent line learns a vocabulary of operations from scratch** (Neurally Interpreted
   Languages, ICLR 2026): discrete words whose meaning a small network carries out. It works on
   synthetic list tasks. It has no ARC result, its words take no arguments, and it has no link to
   symbolic programs.
6. **So the open ground is specific:** a learner whose vocabulary of operations grows from
   puzzles, in which learned words and hand-written words work in one program, learned words take
   arguments, and each new word is tested for being more than an abbreviation. That is what
   [MECHANISM.md](MECHANISM.md) builds and what its first gate measures.

## 1. Where the field stands

| System | Pretrained? | ARC-AGI-1 | ARC-AGI-2 | Source (how read) |
|---|---|---|---|---|
| GPT-6 Astra | yes | | 95.0% | [leaderboard](https://arcprize.org/leaderboard) (full) |
| Claude Fable 5.2 | yes | | 93.8% (ARC-AGI-3: 81.2%) | [leaderboard](https://arcprize.org/leaderboard) (full) |
| NVARC, Kaggle winner 2025 | | | 24.03% | [ARC Prize 2025 report](https://arxiv.org/abs/2601.10904) (part) |
| TRM (7M numbers) | no | 44.6% (verified 40.0%) | 7.8% (verified 6.3%) | [paper](https://arxiv.org/abs/2510.04871) (part), leaderboard |
| HRM (27M) | no | 40.3% (verified 32%) | 5.0% (verified 2%) | [ARC Prize analysis](https://arcprize.org/blog/hrm-analysis) (full) |
| CompressARC (76K) | no | 20% (34.75% on training) | about 4% | [paper](https://arxiv.org/abs/2512.06104) (part) |
| Vector-symbolic solver | no | 3.0% | 0.0% | [paper](https://arxiv.org/abs/2511.08747) (part) |
| **Ultron, engine 1** | no | 12.75% | 0.83% | `reports/arc_runs.log` |

The rows are not measured on identical sets, so read them as rough positions.

ARC Prize 2026 has closed; results are due on 4 December 2026. Its papers are not out yet, so
this review cannot see them.

## 2. The from-scratch line, and what it really learns

**HRM, analysed by ARC Prize** ([analysis](https://arcprize.org/blog/hrm-analysis), full).
- The hierarchy the paper is named for has "minimal performance impact". A plain transformer of
  the same size is within about 5 points.
- The outer refinement loop is what matters: going from 1 to 2 loops is +13 points.
- The network is given only the input grid and a puzzle identity. It never reads the examples.
  So the puzzles it is tested on must already be in its training set.
- Trained only on the 400 evaluation puzzles' examples it still gets 31% (41% with everything).
  The analysts call this "zero-pretraining test-time training".

**TRM** ([paper](https://arxiv.org/abs/2510.04871), part).
- One two-layer network used recursively, 7M numbers, a learned vector per puzzle and per
  augmentation, 1000 augmentations, answers chosen by vote.
- Training for ARC took "around 3 days with 4 H100".
- Its ablations were run on Sudoku, not on ARC.

**What TRM depends on** ([analysis paper](https://arxiv.org/abs/2512.11847), full; one public
checkpoint, ARC-AGI-1).
- With the right puzzle identity: 40.00%. With a blank or random identity: **0.00%**. The paper
  calls the model "functionally dependent on the presence of the correct puzzle identifier".
- Voting over 1000 augmentations adds 10.75 points (29.25% without).
- Recursion is "effectively shallow": 38.25% after the first step, 40.5% after the fourth.

**Adapting TRM under a compute limit** ([paper](https://arxiv.org/abs/2511.02886), full).
- Pre-training a replication took "roughly 48 hours on 4xH100".
- Fine-tuned on hidden puzzles within the Kaggle budget it scored 6.67% on ARC-AGI-2, and
  between 3.33% and 6.67% on resubmission of the same model.

**Sampling from TRM** ([Probabilistic TRM](https://arxiv.org/abs/2605.19943), part): noise at
inference and several rollouts move ARC-AGI-2 pass@1 from 7.36% to 8.47%. The authors say the ARC
gain is small.

**CompressARC** ([paper](https://arxiv.org/abs/2512.06104), part).
- No training set at all. A 76K-number network is trained on one puzzle's examples to minimise
  description length: Ultron's own principle, in a continuous medium.
- "About 20 minutes per puzzle" on an RTX 4070.
- The authors list what it cannot do: swapping two colours, repeating an operation many times,
  counting, rotation and reflection, connectivity, long-range pattern extension.

**Latent Program Network** ([paper](https://arxiv.org/abs/2411.08706), part).
- Learns a continuous space of programs and searches it by gradient at test time. 178M numbers,
  about 2 days on a TPU v4-32, trained on re-arc (generators hand-written for the training tasks).
- Out of distribution it reaches 15.5%; test-time search roughly doubles that score.
- Stated limits: compositional generalisation is not robust.

**What this adds up to.** These systems do not learn concepts that carry to a new puzzle. They
learn a trunk that makes per-puzzle fitting work. The fitted thing (a vector, or weights) is
opaque and belongs to one puzzle. This is also true of Ultron's own engine 2, which can only
answer puzzles it trained on. And the cost is far beyond a single 8 GB GPU.

## 3. Learning a vocabulary of operations

**Neurally Interpreted Languages** ([paper](https://arxiv.org/abs/2604.18907), part; ICLR 2026).
- A program is a short sequence of discrete tokens from a learned codebook of 512. A recurrent
  network carries the program out one token at a time. Everything is trained from scratch from
  input-output pairs, with the Gumbel-Softmax trick; at test time the program is refined by
  gradient search.
- The tokens come to mean reusable operations. Trained on shifts of up to some length, it solves
  longer ones by repeating its "shift by one" token.
- Out-of-distribution accuracy 0.99, 1.00 and 0.91 on its three benchmarks, where an in-context
  model, test-time training and the Latent Program Network score between 0.00 and 0.29.
- Removing discreteness or recurrent execution drops out-of-distribution accuracy to near zero.
- A small model: width 128, 2 layers.
- Stated limits: test-time search cost; "parameterised primitives are not supported"; execution
  is strictly sequential with no branching. No ARC result is reported.

**Neural Programmer-Interpreters** ([paper](https://arxiv.org/abs/1511.06279), part; 2016).
- One shared core; each program is a learned vector. A new program is added by learning only its
  vector: "all the learning for a new task occurs in program embedding space".
- It needs full execution traces as supervision.

**Latent Programmer** ([paper](https://arxiv.org/abs/2012.00377), part; 2021): discrete codes
that organise the search over programs in an existing language. It adds no operations.

**What Ultron takes from these.** A word is a learned vector that a shared network carries out
(as in NPI). Its meaning is learned from input-output pairs alone (as in NLI). Three things are
added that none of them has: the state between words is a real, exact grid; hand-written and
learned words run in the same program; and a learned word can take an argument, such as a colour.

## 4. Library learning

**DreamCoder** ([paper](https://arxiv.org/abs/2006.08381), part).
- Wake: search for programs with a neural guide. Sleep: compress solutions into a library, and
  train the guide on dreams. Text editing goes from 3.7% to 79.6% solved.
- "We typically train DreamCoder on 100-200 tasks." Typical runs take about a day on 20 to 100
  CPUs; one domain took about a year of CPU time.
- Its evidence for learning is compression: a sort written with 5 library calls where the base
  language needs 32. No test separates a new concept from an abbreviation.

**Stitch** ([paper](https://arxiv.org/abs/2211.16605), part): the same compression three to four
orders of magnitude faster. It produces first-order abbreviations of what the language already has.

**LILO** ([paper](https://arxiv.org/abs/2310.19791), part): Stitch plus a language model that
solves tasks and names the abstractions. Unnamed abstractions made the language model worse. It
depends on a pretrained model, so it is outside Ultron's rules.

**For Ultron.** `ultron/arc/library.py` and `compose.learn_library` are this family. Their null
results (9 words, no held-out gain) are what this family predicts when solved tasks are few and
shallow. Compression is cheap now, and it is not the bottleneck.

## 5. Discovery systems

**AM and Eurisko** ([abstract](https://aaai.org/papers/00236-aaai83-059-why-am-and-eurisko-appear-to-work/),
abstract only; the paper's text could not be read). The authors' own summary: "AM's ultimate
limitation apparently was due to its inability to discover new, powerful, domain-specific
heuristics", and learning heuristics by discovery "turned out to be much more difficult than was
realized initially". They credit its early success to a representation in which syntax mirrors
meaning.

**BACON** (from memory, and credited in `ultron/brain/invariants.py`): finds laws as constant
products of measured quantities. Finding a law among given quantities is solved. Choosing the
quantities is not.

**For Ultron.** The lessons brain invents concepts inside kinds a person wrote, and kinds inside
a grammar a person wrote (`ultron/brain/kinds.py` says so). The same question applies to every
part of Ultron: how much of a discovery was already in the representation?

## 6. Programs and direct answers are complementary

**Induction and transduction** ([paper](https://arxiv.org/abs/2411.02272), part). Two models with
the same training data: one writes programs, one answers directly. Programs do better on "precise
computations" and on "composing multiple concepts"; direct answers do better on "fuzzier
perceptual concepts". Together 56.75% where each alone is 38% and 43%. Their 400,000 training
problems were written by a language model, so the result is not from scratch.

**For Ultron.** This supports having both kinds of step. It also suggests where learned words
should pay first: on perceptual steps that are hard to write as code.

## 7. Other from-scratch attempts

**Vector-symbolic solver** ([paper](https://arxiv.org/abs/2511.08747), part): objects, a
hand-designed language of five operations, small predictors. 3.0% on ARC-AGI-1 evaluation, 0% on
ARC-AGI-2. It "cannot generate new hypotheses on the fly".

**Slot Attention** ([abstract](https://arxiv.org/abs/2006.15055)): a network can learn to split a
scene into objects without labels. Relevant later, when Ultron's fixed way of seeing things
becomes the limit.

## 8. ARC-AGI-3

- An agent sees a 64 x 64 coloured grid, chooses an action and gets the next grid, with no rules
  given in words. The score is action efficiency against human players
  ([Tycho](https://arxiv.org/abs/2607.28287), part).
- 25 games are public. The competition track runs offline, with open code.
- The published high scores all put a pretrained model in charge. One harness writes a Python
  model of each game and plans through it: 7 of 25 games solved, mean score 32.58%
  ([paper](https://arxiv.org/abs/2605.05138), full). A later one reports 100% on all 25 public
  games ([Tycho](https://arxiv.org/abs/2607.28287)); its authors note the public games were not
  checked for contamination.
- No leading entry is described as free of pretrained models.

**For Ultron.** The format suits its lessons brain (acting, experimenting, learning laws from few
trials). No from-scratch result was found to compare against, so this stays a scouting item.

## 9. The ground nobody holds

As far as this review found, nobody has shown any of the following from scratch:

1. A vocabulary of operations that grows from ARC puzzles, where the puzzles did not have to be
   solved by search first.
2. Learned words that take arguments, such as "do this with colour c".
3. Learned words and hand-written words in one exact program.
4. A test that separates a new primitive from an abbreviation, with a count kept over time.
5. A hand-written prior that shrinks: operations removed and relearned, at an equal score.

Limits of this claim: the search was not exhaustive, several papers were read only in part, and
ARC Prize 2026's papers are not yet public.

## 10. What this changes for Ultron

- **M2 is dropped as the main line.** A copy of TRM would cost about 190 H100-hours, would at
  best equal a published result, and would not produce words. The idea of clustering its internal
  states is dropped with it: a network that memorises puzzle identities is the wrong place to look
  for concepts.
- **The network's job changes.** It no longer answers puzzles. It carries out words, one exact
  step at a time. That is a much easier thing to learn and to check, and it fits an 8 GB GPU.
- **The claim to aim at** is section 9, items 1 to 5, measured by the "new primitives" row of the
  scoreboard and by the count of hand-written operations.
- **The honest odds.** The closest published work succeeded on simpler synthetic tasks. The first
  gate (G0) is built so that a failure shows up early and cheaply.
