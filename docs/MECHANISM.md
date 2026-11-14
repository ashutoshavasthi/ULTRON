# The mechanism: learned words

*The specification for the `ultron-final` branch. The reasons are in [RESEARCH.md](RESEARCH.md);
the code is in `ultron/words/`; the measured results are in `reports/words_g0.md`.*

## The problem it answers

Ultron's language could only grow by abbreviation. A new word was a combination of the 38
hand-written operations, so it computed nothing new, and it could only be mined from puzzles
Ultron had already solved. The deep puzzles that would yield useful words could not be solved
without those words.

The task is to find compact concepts that make hard puzzles short, without first solving those
puzzles.

## The idea

One language with two kinds of word.

- A **hand-written word** is one of the 38 operations with its argument, such as
  `gravity(down)`. Its code carries it out.
- A **learned word** has no code. A small network, the **interpreter**, carries it out: given a
  picture and a word, it writes the next picture.

A program is a short sequence of words of both kinds. The state between two words is always a
real picture, snapped to exact colours, so a mistake cannot build up quietly over a long program.

Because a learned word's meaning is found by gradient descent on puzzles, a puzzle does not have
to be solved before it can teach. And because the interpreter is a network, a learned word can
mean something that no combination of the hand-written words can say.

## The parts

| Part | What it does | Code |
|---|---|---|
| Pictures as tokens | A grid on a small square canvas, with its edges marked, so its size can be read back | `state.py` |
| Words | An operation plus one argument (none, a colour, a side, ...). Arguments are shared, so a learned word can take a colour the way a hand-written one does | `vocab.py` |
| Dreams | Hand-written words run on real pictures from the practice half: every step has an exact answer | `curriculum.py` |
| Interpreter | A two-layer transformer used three times over; the word's vector is added to every cell | `interpreter.py` |
| Teaching | The interpreter imitates the hand-written words on dreams | `learn.teach` |
| Free words | Words with no meaning yet, given one from unexplained puzzles (below) | `learn.rediscover` |
| Search | The shortest program of both kinds of word that explains a puzzle exactly | `search.py` |
| New or abbreviation | Can a program of hand-written words imitate the learned word? | `crystallise.py` |

## How a free word gets its meaning

Take the puzzles that no program of hand-written words explains.

1. **Start from one puzzle.** A new word begins from a single unexplained puzzle. It is tried in
   two forms at once: bare, and taking a colour.
2. **Grow with the puzzles it fits.** The first round is the starting puzzle alone. Each later
   round, the word trains with the starting puzzle, every puzzle it has confirmed (step 3), and
   the unconfirmed puzzles it fits best. Those are chosen afresh each round, more each time
   (1, 2, 3, 5, 8, 12, ...), and only from puzzles it fits about as well as its best few. A puzzle
   that belongs to some other word fits far worse and stays out. Dreams of the hand-written words
   are mixed into every batch so that nothing already learned is lost.
3. **Check, with an example never trained on.** Each puzzle keeps one example back. A puzzle
   counts as explained by the word only when that example also comes out exactly right. A word
   that fits the examples it trained on but keeps failing the check has memorised the puzzle, and
   the puzzle is turned away.
4. **Earn its place.** The form (bare or colour) that explains more puzzles is kept, and only if
   it explains at least three. A word for one puzzle is that puzzle memorised.
5. **Repeat** with the puzzles still unexplained, until none are left or no new word earns a
   place.

This is the shortest-description rule applied to words: a word is worth its cost only when many
puzzles share it.

## What is measured

- **Exactness.** An answer counts only if the whole picture is right.
- **New primitives.** For each kept word, the hand-written words alone are searched for a program
  that imitates it. Found: the word is an abbreviation. Not found: it is a new primitive. The
  scoreboard carries this count.
- **Three checks on every rediscovery result.**
  1. The hand-written words alone must not already explain the puzzles.
  2. A comparison with no shared word: one vector fitted to each puzzle separately, at test time,
     which is how TRM and the Latent Program Network work.
  3. Held-out puzzles on pictures never trained on, including ones that mix the learned word with
     a hand-written word.

## Gates and kill rules (fixed before the runs)

### G0: small pictures, CPU
48 hand-written words are taught. Five families are never shown: `flip_h`, `recolour_all`,
`gravity`, `fill_enclosed`, `outline`. With only rot180, transpose and antitranspose taught, a
left-right flip cannot be built from the taught words. For the three colour families, two colours
(4 and 7) never appear in the training puzzles.

- **G0-a, carrying out.** Target: single words exact on at least 99% of kept-aside pictures, and
  six-word programs exact on at least 90%. Kill rule: below that, raise capacity or training once;
  if still below, stop and report.
- **G0-b, rediscovery.** For each hidden family in turn, Ultron gets 120 puzzles whose rule is one
  word of that family. Target: a free word matches the hidden word on at least 95% of kept-aside
  pictures, for at least 3 of the 5 families. Kill rule: fewer than 3 of 5 after one round of
  fixes means the mechanism does not work in this form. Report it plainly.

### G1: full-size pictures, real ARC, one 8 GB GPU
- Train on the practice half (317 puzzles) plus dreams.
- Target: at least +10 net on the 316 held-out puzzles over engine 1's 32, at 95% precision or
  better, with an interval that excludes zero; and at least one new primitive that repeats across
  two rounds.
- Kill rule: no significant gain after three rounds. Then follow the bottleneck report.

## What G0 cannot show

- The hidden words are operations a person once wrote. Relearning them shows the mechanism can
  find a concept of that kind from puzzles. It does not show it will find the concepts real ARC
  puzzles need.
- G0's puzzles each use the hidden word alone, so the learner starts from single-step puzzles.
  Real unexplained puzzles are mostly longer. G1 must learn words from inside longer programs.
- Small pictures (8 x 8) are easier than 30 x 30.

## Known limits of this design

- **One picture in, one picture out.** A learned word cannot yet return a number or a choice
  among things, so counting-style steps stay hand-written.
- **One argument.** Words with two arguments (a colour and a side) are not covered.
- **No branching.** Programs are straight sequences, as in the published work this builds on.
- **The interpreter is a person's design**, as the 38 operations were. What is learned is the
  meaning of the words, not the shape of the network.

## Rules that still hold

No pretrained model. Pictures for teaching come only from the practice half. The evaluation sets
stay locked. Learned words never enter the frozen list of 38 (`ops.registry`); they live beside
it. Ultron never edits its own tests. Failures are reported as plainly as successes.
