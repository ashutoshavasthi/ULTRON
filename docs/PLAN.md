# Ultron: the plan, on one page

## What
A learner that writes programs in **a language it builds itself**, and trains its own
networks, to explain what it sees from a few examples. There is no pretrained model and no
language model: Ultron trains everything it uses, from its own experience and from puzzles
it makes itself.

## Goal
General intelligence that improves itself, and then goes beyond human. The checkpoint for
human level is the ARC Prize grand-prize bar: **85% on ARC-AGI-2**. Nobody can promise
the end goal. What this plan guarantees is that we never fool ourselves, never stall
silently, and change course by fixed rules when stuck.

## How: three engines, one judge, a loop that feeds itself
1. **Programs:** the shortest program, in its own language, that explains the examples.
   Its language grows: recurring pieces become new words. A guide learned from its dreams
   tells the search which steps a puzzle needs.
2. **Its own network:** a small recursive network (in the spirit of TRM) that answers
   directly, trained from scratch on its experience, augmentations and dreams. It covers
   the perceptual puzzles short programs can't express.
3. **Compression per puzzle:** "the shortest description wins", applied to each puzzle at
   test time (in the spirit of CompressARC).
4. **The judge:** an answer is given only if it passes checks the engines can't game.
   - A program must hold with any one example left out.
   - A network's answer must agree across augmentations, or with another engine.

**The loop:**
1. It solves what it can.
2. Solutions grow its language.
3. The language makes dreams (new puzzles with known answers).
4. Dreams train the guide and the networks.
5. Those solve more, and the loop repeats.

It compounds through data, not only through words.

## Milestones (targets and kill rules fixed in advance)
| # | What | Target | If missed |
|---|---|---|---|
| M1 (now, CPU) | Dreams plus a learned search guide | Practice explained 46 → ≥ 80 within 3 rounds; held-out net gain ≥ +15 at ≥ 95% precision | Gain < +10 after 3 rounds: stop tuning program search; M2 becomes the main line |
| M2 (GPU) | Its own network and compression per puzzle, plus the judge | ARC-AGI-1 evaluation ≥ 30% at ≥ 90% precision, then ≥ 45% | Network < 30%: check our version against TRM's published code before anything else |
| M3 | Engines teach each other (programs label dreams; confident network answers seed program search) | ARC-AGI-2 ≥ 10%, then ≥ 30%; every round a significant held-out gain | Two rounds without a significant gain: follow the bottleneck report |
| M4 | It improves its own learning: proposes changes to its settings and strategies, sandboxed, scored and owner-approved | Each kept change a significant gain with zero regressions; at least one it proposed itself | No better than random changes: stop and rethink |
| M5 | Breadth and beyond: the same engines on lessons, list functions, Engc code tasks and ARC-AGI-3; then rewriting its own code (its Engc twin) | ≥ 85% on ARC-AGI-2, and transfer to the other domains | — |

## Rules that can't bend
- No pretrained model and no language model. Every network is trained by Ultron, from
  scratch.
- **Every work block ends with a scoreboard row** (`python -m ultron learn` or `score`).
- **Every gain carries a 95% bootstrap interval;** it counts only if the interval excludes 0.
- **A bottleneck report every round** (wrong / found with 4× the budget / not found). The
  next work targets the biggest bucket.
- Two tiers of held-out: the dev half every round; the official evaluation sets only at
  milestones, always logged (`python -m ultron arc --split evaluation`).
- Self-changes are sandboxed, kept only if held-out scores rise with nothing broken, and
  approved by the owner. Ultron never edits its own tests.
- Report failures as plainly as successes. Apply kill rules as written.

## Where it stands
- **Last logged official scores:** ARC-AGI-1 evaluation 12.75%, ARC-AGI-2 0.83%.
- **The learning curve:** [reports/learning_curve.md](../reports/learning_curve.md).
- **M1 is done, and its kill rule triggered** (2026-11-07). After three rounds with 3,000
  dreams a night and a learned guide:
  - practice explained 48 (target ≥ 80);
  - held-out net gain +3, 95% interval +0 to +7 (target ≥ +15);
  - precision 100%.

  In every round, **0 of 40** missed held-out puzzles were found even with 4× the search.
  The wall is what its language can express, not search. Program search stays as the
  high-precision engine; **M2 is the main line**.
- **M2's code is ready and tested on CPU:**
  - `ultron/arc/net/`: its own recursive network;
  - `ultron/arc/judge.py`: the judge.

  The full training run needs the GPU.

## Running M2 on a GPU
Two ways to get there; either works:
- **Your own machine with an NVIDIA GPU:** run Claude Code there on a clone of this
  repository, or share the folder with this session through the Claude desktop app
  (Settings → Claude Code → Remote Control).
- **A cloud GPU machine:** one modern NVIDIA GPU (for example an H100 or A100) is enough
  to start.

Then:

```bash
git clone https://github.com/ashutoshavasthi/ULTRON && cd ULTRON
git checkout claude/dreamy-darwin-neiflp
pip install -e ".[net,dev]"          # PyTorch: a library, not a pretrained model
python -m ultron net train --device cuda      # about a day on one H100-class GPU
python -m ultron net score --device cuda      # held out, judged: programs / network / both
```

- **On Windows (PowerShell):** type the commands one per line (Windows PowerShell 5 doesn't
  accept `&&`). Install PyTorch's CUDA build before the `pip install -e` line:
  `pip install torch --index-url https://download.pytorch.org/whl/cu128`. Plain
  `pip install torch` on Windows gives a build without GPU support.
- **Cost:** the full setting is about 2×10¹⁹ operations in bfloat16. That's roughly 15–25
  hours on one H100-class GPU (more on smaller ones). `--steps` makes it shorter.
- **Scale:** we only go bigger (more views, steps, GPUs) if the held-out curve justifies it.
- **M2's rule:** below 30% held out after the full run, first compare our network with
  TRM's published code on the same data, then fix ours or re-plan.

## Where things are
- [ARCHITECTURE.md](ARCHITECTURE.md): how the code works.
- [ARC_REPORT.md](ARC_REPORT.md): the technical report on ARC-AGI.
- [history/](history/): earlier plans. The simulated room is parked on branch `park/room`.

Sources for the field's results:
- TRM: [arXiv 2510.04871](https://arxiv.org/abs/2510.04871)
- CompressARC: [arXiv 2512.06104](https://arxiv.org/abs/2512.06104)
- Induction and transduction: [arXiv 2411.02272](https://arxiv.org/abs/2411.02272)
- ARC Prize 2025: [results](https://arcprize.org/blog/arc-prize-2025-results-analysis)
