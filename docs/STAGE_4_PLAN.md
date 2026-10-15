# Stage 4: interactive worlds

> **No longer the main line (2026-10-15).** The plan was rebuilt around growing up
> from a newborn ([MASTER_PLAN.md](MASTER_PLAN.md), [ROADMAP.md](ROADMAP.md)). This plan is
> kept as a record and its results are banked: learning what its actions do (W1, W2, W7) moves into the nursery at Age 1 (infant), games with unknown rules (W3–W5) belong to Age 3, and ARC-AGI-3 (W6, W8) to Age 4. See
> [DEVELOPMENT_MAP.md](DEVELOPMENT_MAP.md).

**Mission.** Ultron has acted only once: one kick of a puck in a world whose quantities it
was told, running a law it already had backwards (`brain/body.py`). It has never been
dropped into a world whose rules nobody told it, had to find out what its own actions do,
worked out what the world wants, and then planned a way there. Stage 4 does that, in grid
games with unknown rules and unknown goals, like ARC-AGI-3.

What Ultron must do in each new game, with nothing but the pictures and a few buttons:
1. **find out what its actions do**, by experiment, as laws about the things it sees;
2. **find out what the game wants** (the goal), as a law, from the moments it wins or loses;
3. **plan in its own learned model** to win the next level in close to the fewest actions;
4. **carry what it learned** into the next game, so later games need fewer actions.

Stage 4 depends on nothing unfinished in Stage 2 (real footage) or Stage 3 (language).
It uses the curiosity of Phase 1, the body of Phase 3 and the thing laws of Stage 1's ARC
work, and it does not need words.

## Exit test (fixed now, before the work)

Two kinds of world are used, and each criterion says which.

- **Trainer games.** A game generator in the Trainer, which Ultron cannot read. A game is
  a grid of up to 16 × 16 cells in up to 10 colours, 4 buttons, and a few levels. Its rules
  are made of **pieces** (listed below), with colours, button meanings and layouts drawn at
  random per game, so no colour or button means the same thing from one game to the next.
  Ultron sees only the picture after each button press and, at the end of a level, "won"
  or "lost". Splits are fixed now by seed and stored in code: training games (seeds
  4000–4999), exam games (seeds 14000–14999, never played during development) and
  failure-lab games (seeds 24000–24999). Held-out exam games use **combinations of pieces
  never seen together** in training, and one exam set uses **one piece never seen at all**.
- **ARC-AGI-3 public games** (arcprize.org), played locally with the official toolkit
  (`arc-agi` on PyPI, 25 public games, version hashes recorded at the first run), each
  level with the human baseline action count the toolkit ships. Ultron sees only frames,
  the available buttons, the game state and the levels completed; **it never reads a
  game's source**. Three games are the development set and may be watched during the
  work: `ls20`, `ft09` and `vc33` (the three released first, in the 2025 preview). The
  other 22 are **sealed**: played only for a verdict, every run logged in `reports/`.

Every row reports **precision** (predictions or answers right, of those given) as well as
score, and the actions Ultron spent to get there.

| # | Criterion |
|---|---|
| W1 | **What my actions do.** On 40 held-out Trainer games, after exploring each with at most 150 button presses, Ultron predicts the **whole next picture** exactly for ≥ 95% of 50 held-out (picture, button) pairs per game, situations it never saw, made by the Trainer (5 walks of 10 presses on layouts of that game it never saw, its laws frozen; it predicts each picture before seeing it; presses that end a level are judged in W3 and W4, not here); precision ≥ 98% (it may say "I can't tell" instead of predicting). On 20 games with one piece it never met in training: ≥ 80%, precision ≥ 95%. It beats two baselines fixed in advance by ≥ 30 points: "nothing changes" and a memoriser of every (picture, button) → picture it saw |
| W2 | **Experiments that decide.** Ultron chooses its own button presses to split its rival explanations. It reaches W1's level on the same 40 games with ≤ 0.5× the presses of a random explorer and ≤ 0.7× those of a fixed sweep (each button in turn from every place it reaches), both run with the same learner |
| W3 | **What the game wants.** The goal is never told: the world says only "won" or "lost". After at most 3 wins in a held-out Trainer game, Ultron states the goal as a law, and on 30 held-out end pictures per game says which are wins ≥ 95% of the time (40 games), beating a baseline that remembers the winning pictures |
| W4 | **Planning in its own model.** On the held-out levels of 40 held-out Trainer games (levels after the first), Ultron wins ≥ 90% of levels, with presses ≤ 1.25× the fewest possible (found by the Trainer's own search in the true game), counting every press, its experiments included. Baselines: a random player and a novelty-seeking player with the same budget |
| W5 | **Learning compounds.** Over a run of 30 held-out Trainer games that share pieces, the presses to the first win in games 21–30 are ≤ 0.6× those in games 1–10, and ≤ 0.7× those of a fresh Ultron (no earlier games) on games 21–30. What carried over is shown: the laws that recurred and became priors |
| W6 | **ARC-AGI-3, sealed games.** On the 22 sealed public games, each level with a budget of 5× its human baseline presses: Ultron completes ≥ 50% of all levels, and on the levels it completes it uses ≤ 2× the human baseline presses in total. It beats a random player given the same budget (fixed seed) on levels completed. Played once per verdict, never tuned on |
| W7 | **It knows when its model is wrong.** In Trainer games whose rules change once mid-game (failure lab), it notices the change at the first press that contradicts its laws (100%), says which law broke, and is back to W1's level within 50 presses. It never claims to have won when it hasn't |
| W8 | **Blind test.** From a public syllabus of the pieces (not their colours, layouts or combinations), examiners who never saw the code write 10 games: Ultron wins ≥ 8 at first sight, within 2× the fewest presses |

Efficiency: the presses spent in all training games are reported, and W1–W5 together are
reached with **≤ 20,000** training-game presses in all.

Everything Stages 1–3 passed must still pass: the curriculum (every lesson on the first
attempt), every exam, every failure-lab row, the blind tests and the full test suite. A
retrain stays byte-for-byte identical.

## The pieces (the Trainer's syllabus, public)

These are what the Trainer builds games from. The roles are public; which colour plays
which role, which button does what, the layouts and the combinations are drawn per game.

| Piece | What it does |
|---|---|
| mover | one thing moves one cell per press; each of 4 buttons moves it one way (which way is drawn per game) |
| wall | cells of one colour that nothing passes through |
| box | a thing the mover pushes when it walks into it, if the cell beyond is free |
| pickup | a thing that disappears when the mover steps on it |
| paint | a cell that changes the mover's colour to its own when stepped on |
| hazard | a cell that loses the level when the mover steps on it |
| ice | cells on which the mover keeps sliding until something stops it |
| door | cells that block until every pickup is gone, then vanish |
| goals | one per game: mover on the target; every box on a target; every pickup gone; the mover on the target wearing the paint's colour |

Held out from training, used only in W1's one-new-piece set: **portal** (two cells of one
colour; stepping on one puts the mover on the other).

## Rules for this stage

- **The Trainer sets up worlds; Ultron finds the laws.** The game generator and its rules
  live in `env/` and the Trainer. Ultron's code never imports them; it gets pictures,
  buttons and "won"/"lost". Its laws are written in its own terms (things, colours, places,
  moves) and checked against what happens, so a law can be wrong and found wrong.
- **No game knowledge written in.** Nothing in Ultron says "walls block" or "boxes are
  pushed". It may assume what an infant may: the world is made of things, a thing usually
  stays itself from one picture to the next, and the same press in the same situation does
  the same thing. These assumptions are listed in code where they are used.
- **Rivals, not guesses.** Explanations nearly as short as the best are kept as rivals.
  Where they disagree, Ultron says "I can't tell", and that disagreement is what it
  experiments on.
- **Determinism.** Games, exploration and planning are seeded; a rerun is identical.
- **ARC-AGI-3 sealed games are never tuned on.** Only the three development games are
  watched. A sealed run is logged with its date, commit and score, failures included.
- **The failure lab gets an interactive-worlds experiment**: pictures with flickering
  noise, a button that sometimes does nothing, a thing that changes at random (the noisy
  TV, which curiosity must learn to ignore), rules that change mid-game, and a hidden
  counter. Its breakpoints are recorded and only move outward.

## Work packages

### WP1: a world to act in (W1)

`env/gridgames.py`: the game generator, the pieces, the splits, and the Trainer's exact
search for the fewest presses. A small adapter gives Ultron the same interface (picture,
buttons, won/lost) for Trainer games and ARC-AGI-3 games.

### WP2: what my actions do (W1)

`brain/worldmodel.py`: from pairs of pictures, the things and how each changed (moved,
recoloured, vanished, appeared). For each button, the shortest set of laws, each "things
of this kind, in this situation, do this", that explains every press seen. Situations are
described in Ultron's own terms: the colour of the thing, the colours next to it in each
direction, whether the thing next to it could move. Rivals kept; "I can't tell" when they
disagree.

### WP3: experiments that decide (W2)

Curiosity's information gain, applied to presses: go where the rivals disagree, and press
the button that splits them. Novelty first, the noisy-TV rule second (stop chasing what
never becomes predictable).

### WP4: what the game wants (W3)

The goal as a law about the winning pictures: the shortest description, in the same terms,
true of every winning picture and of no picture that came before a win. Rivals kept;
losses ("lost") give laws about what to avoid.

### WP5: planning (W4)

Search in its own model, not the world: from the current picture, the shortest sequence of
presses after which the goal law holds. Where the model says "I can't tell", plan an
experiment first.

### WP6: priors across games (W5)

Laws that recur across games, with their colours and buttons abstracted ("a colour that
nothing passes", "a thing that is pushed"), kept as priors that make the matching laws
cheaper to state in the next game, as library learning made recurring program pieces
cheaper in Stage 1.

### WP7: ARC-AGI-3 (W6)

The same learner, through the adapter, on the 64 × 64 frames of the ARC-AGI-3 games, with
the clicking buttons (a press at a place) added. Development on `ls20`, `ft09` and `vc33`
only.

### WP8: the failure lab and the blind test (W7, W8)

## Order

WP1 and WP2 first (W1 is the foundation), then WP3, WP4 and WP5, then WP6, then WP7, then
WP8.

## Status

| # | Status |
|---|---|
| W1–W8 | not started (plan fixed 2026-10-11) |
