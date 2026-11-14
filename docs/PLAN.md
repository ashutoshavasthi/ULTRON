# Ultron: the plan, on one page

## What
A learner that writes programs in **a language it builds itself**, to explain what it sees from a
few examples. There is no pretrained model and no language model: Ultron trains everything it
uses, from its own experience and from puzzles it makes itself.

## Goal
General intelligence that improves itself, and then goes beyond human. Nobody can promise that.
What this plan fixes is the next thing to prove, and how we will know.

**The checkpoint has changed.** Pretrained models now score about 95% on ARC-AGI-2, so that
benchmark is no longer a first. From scratch, the best published results are about 45% on
ARC-AGI-1 and 8% on ARC-AGI-2; Ultron is at 12.75% and 0.83%. Ultron's claim is the one nobody
holds yet: **a language whose vocabulary of operations grows by itself, measured.** The reasons
are in [RESEARCH.md](RESEARCH.md).

## How: learned words
Ultron's old words were abbreviations of 38 hand-written operations, so they added nothing new.
Now the language has a second kind of word.

- A **hand-written word** is run by its code.
- A **learned word** has no code. A small network (the interpreter) carries it out on a picture.
- A program mixes both. The state between words is always an exact picture.
- A learned word gets its meaning from puzzles no hand-written program explains. It is kept only
  if at least three puzzles share it and it passes an example it never trained on.
- Each kept word is tested: if hand-written words can imitate it, it is an abbreviation; if not,
  it is a **new primitive**.

The full specification is [MECHANISM.md](MECHANISM.md).

## Milestones (targets and kill rules fixed in advance)
| # | What | Target | If missed |
|---|---|---|---|
| G0 (CPU, small pictures) | Carry out taught words; relearn five families it was never shown | Single words 99% exact, six-word programs 90%; a free word matches the hidden word on 95% of unseen pictures for 3 of 5 families | One round of fixes, then report the failure and stop this form |
| G1 (one 8 GB GPU, real ARC) | Learn words from the practice half's unexplained puzzles | Held-out net +10 over engine 1's 32 of 316, at 95% precision, interval excluding 0; one new primitive repeating over two rounds | No significant gain in three rounds: follow the bottleneck report |
| G2 | Words from lessons: grid worlds (falling, mirrors, inside and outside) teach words before ARC | A word learned in a lesson is used in a held-out ARC answer | Rethink how lessons and puzzles connect |
| G3 | The hand-written count falls: remove operations and relearn them | From 38 to 35 at an unchanged score | Report which operations cannot be relearned, and why |
| G4 | Past the from-scratch marks, checked by others | Above 45% on ARC-AGI-1 and 8% on ARC-AGI-2; a public write-up and an independent rerun | - |
| Later | ARC-AGI-3; Ultron proposing changes to itself, sandboxed and owner-approved; the chip | - | - |

## Rules that can't bend
- No pretrained model and no language model. Every network is trained by Ultron, from scratch.
- **Every work block ends with a scoreboard row** (`python -m ultron score`).
- **Every gain carries a control and a 95% interval;** it counts only if the interval excludes 0.
- Pictures for teaching come only from the practice half. The official evaluation sets are opened
  only at milestones, always logged (`python -m ultron arc --split evaluation`).
- Learned words never enter the frozen list of 38 hand-written operations.
- Self-changes are sandboxed, kept only if held-out scores rise with nothing broken, and approved
  by the owner. Ultron never edits its own tests.
- Report failures as plainly as successes. Apply kill rules as written.

## Where it stands
- **Last logged official scores:** ARC-AGI-1 evaluation 12.75%, ARC-AGI-2 0.83% (engine 1).
- **G0, measured 2026-11-14** ([reports/words_g0.md](../reports/words_g0.md)):
  - **Relearning hidden words: met, on the second run** (one round of fixes, as allowed).
    Three of five families reach a 95% match: a flip, a recolour and an outline. With the
    learned word, held-out puzzles go from 1 of 240 solved to 223 of 240. No program of
    hand-written words imitates any of the three, so each counts as a new primitive.
  - **Two families were not relearned:** gravity and fill-enclosed. The measured reason for
    gravity is the amount to learn from, not the choice of puzzles.
  - **Carrying out taught words: not met.** Single words are exact on 87.7% of unseen
    pictures (target 99%) and six-word programs on 49.5% (target 90%). Words that re-map
    cells or colours are near perfect; words about whole things are not.
- **What this means:** the mechanism works for simple words on small pictures, on a CPU. It
  has not been shown on real ARC puzzles. G1 is next, and it needs a stronger interpreter
  first: wider, trained longer, on the GPU.

## Running it
```bash
pip install -e ".[net,dev]"            # PyTorch: a library, not a pretrained model
python -m ultron words teach           # teach the interpreter (about two hours on four CPU cores)
python -m ultron words g0              # gate G0; writes reports/words_g0.md
python -m ultron words g0 --quick      # a few minutes: checks the pipeline only
```

### The next run, on an NVIDIA GPU (sized for 6 GB)
G0-a was not met at the CPU size. The `gpu` size is the same gate with a stronger interpreter
(twice as wide, one more pass, more than three times the training) and more pictures per word in
the measurement. On Windows (PowerShell), type the commands one per line:

```
git clone https://github.com/ashutoshavasthi/ULTRON
cd ULTRON
git checkout ultron-final
pip install torch --index-url https://download.pytorch.org/whl/cu128
pip install -e ".[dev]"
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
python -m ultron words teach --size gpu --device cuda
python -m ultron words g0 --size gpu --device cuda
```

- The sixth line must print `True` and the card's name. If it prints `False`, PyTorch was
  installed without GPU support: use the install command pytorch.org gives for your CUDA version.
- `teach` prints its progress twelve times and saves the interpreter each time
  (`brain/words_base_gpu.pt`). If it is interrupted, continue with
  `python -m ultron words teach --size gpu --device cuda --start brain/words_base_gpu.pt --steps N --lr 2e-4`,
  where N is the number of steps still to go (of 100,000).
- `g0` writes `reports/words_g0_gpu.md` after every family.

## Where things are
- [RESEARCH.md](RESEARCH.md): what is known, and the ground nobody holds.
- [MECHANISM.md](MECHANISM.md): learned words, the gates and their kill rules.
- [ARCHITECTURE.md](ARCHITECTURE.md): how the lessons brain works.
- [ARC_REPORT.md](ARC_REPORT.md): engine 1 on ARC-AGI.
- [history/](history/): earlier plans, including the M1 and M2 plan this one replaces.
