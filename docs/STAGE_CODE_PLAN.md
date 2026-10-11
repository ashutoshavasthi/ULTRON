# The Code stage: how programs work, Engc, and improving itself

**Mission.** Ultron finds laws in worlds, but it cannot read or write a real program,
it has never looked at its own code, and every building block it has was designed by
people. The Code stage teaches it how programs work the way it learned physics: by
running them in a sandbox and finding the shortest laws that explain what they do.
Then it writes programs, in **Engc** (the owner's structured-English language,
[Engc-V1](https://github.com/ashutoshavasthi/Engc-V1)), understands what algorithms
cost and how **AI and machine learning** work (gradients, how training behaves, and
writing learners of its own), then it writes **itself** in Engc, then it **improves
itself** continuously, under checks it can never change.

**Scope (owner, 2026-10-11):** coding understood completely and in general, not only
Engc, plus AI and ML. C1–C2 are Engc, C3 a second language, C4 its own code, C5 writing
programs, C6 algorithms in general, C7 AI and ML, C8 its twin, C9 self-improvement.

**Why first (owner, 2026-10-11).** The owner made this the first priority: "the first
thing should be learning how its code works and how coding works in general and full,
I want it to write itself and improve itself constantly." It merges the roadmap's old
stage 7 (code, itself and Engc) and stage 8 (self-improvement) into one stage and moves
it to the front. The other stages keep running alongside. ARC stays a yardstick: it is
re-measured after every criterion below is met, never chased.

## The world: a sandbox that runs programs

Programs are Ultron's new world. The Trainer writes programs and inputs; the sandbox
runs them; Ultron sees what a scientist sees:

- the program's text, as words and marks separated by spaces;
- what it printed, or that it failed;
- for statements (from C2 on), the value of every name after each line runs, like the
  frames of a film.

Ultron never sees Engc's compiler, its grammar tables or its documentation. Engc is
pinned to one commit, so the world never changes under it. The sandbox has no network,
no files, and limits on time and memory. Later (C9) Ultron may *propose* programs to
run, including changes to itself; it still only ever runs them inside the sandbox.

**What is given by hand, stated plainly.** As with its program language (`dsl.py`),
some structure is core knowledge and is given: a program is a sequence of words; a
word between two values may join them; marks may group words. **Which** word does what,
**how strongly** each word groups and **which way** it chains, and what each statement
does to its memory, are all learned. No word's meaning, no precedence and no statement
effect is written in.

## Exit test (fixed now, before the work)

Every test runs on held-out programs from a generator Ultron never sees, with exam seeds
70xx that are never used during development (development uses seeds 75xx). Every row
reports **precision** (answers right of answers given): Ultron may say "I don't know",
and a wrong answer counts against it. Every row beats baselines fixed here.

| # | Criterion |
|---|---|
| C1 | **Reading Engc: what expressions mean.** From ≤ 400 runs of one-line programs `PRINT <expression> .` (numbers 0–20, at most 2 operators, in the lesson), Ultron learns what each word and mark means (`PLUS`, `MINUS`, `TIMES`, `MODULO`, `RAISED TO`, the comparisons `IS GREATER THAN`, `IS LESS THAN`, `IS EQUAL TO`, `IS AT LEAST`, `IS AT MOST`, `IS NOT`, the logic words `AND`, `OR`, `NOT`, leading `MINUS`, their symbol twins `+ - * % ** > < == >= <= !=`, and brackets) and how they group. On **200 held-out expressions** with 3–6 operators, numbers up to 999 and combinations it never saw, it predicts the printed output **without running it**: ≥ 190/200 exactly right, precision ≥ 99%. Baselines: lookup (seen programs), nearest (the output of the most similar seen program), and left-to-right reading with the right word meanings but no grouping learned. Ultron must beat the best baseline by ≥ 30 points. (`DIVIDED BY` waits for C2, where decimals are printed.) |
| C2 | **Reading Engc: what statements do.** `SET`, `IF`/`ELSE`, `WHILE`, `FOR EACH`, lists, `THE LENGTH OF` and other library phrases, `DEFINE ROUTINE`/`CALL`/`RETURN`, recursion. Ultron learns each statement's effect as a law of change on its memory, from ≤ 1,000 runs watched line by line. On **200 held-out programs** of 5–40 lines, with loops that run up to 1,000 times and nesting deeper than any it watched, it predicts the full printed output without running it: ≥ 180/200, precision ≥ 98%. Baselines: lookup, nearest, and a straight-line reader that runs each line once in order |
| C3 | **Coding in general: a second language, faster.** A language it has never seen (a Python subset, then a language the Trainer invents with fresh words for the same ideas) is learned to C1 + C2 level with **≤ 1/3 of the runs** Engc took, because what it learned about variables, loops and calls carries over. Same held-out exams and baselines as C1–C2 |
| C4 | **Its own code.** A fixed list, chosen now by rule: every top-level function in `ultron/brain/dsl.py`, `ultron/brain/amounts.py` and `ultron/brain/columns.py` that takes and returns numbers, rows or truth values. (a) From ≤ 20 runs each, it finds a law in its own program language for ≥ 80% of them and predicts 50 held-out inputs each (wider ranges) ≥ 98% right. (b) From **reading the source alone** (Python, learned in C3), it predicts the same held-out outputs ≥ 80% right, precision ≥ 98%. Baselines: lookup and nearest from the 20 runs |
| C5 | **Writing programs, in Engc.** **100 held-out tasks**, each given as 5 input/output examples, with 20 hidden tests each. Ultron finds the shortest program in its own language and writes it in Engc using the meanings it learned (writing is reading backwards: nothing translates for it). Every program is compiled by the real Engc compiler and run on the hidden tests: ≥ 70/100 tasks pass every hidden test; ≥ 95% of the programs it hands in pass (it may decline). Baselines: an enumerator of Engc programs with the same budget of runs, and a memoriser. The task file is written by the Trainer, committed and its hash recorded **before any C5 work begins**. If the published List Functions benchmark (Rule et al., 250 tasks) can be obtained, it is scored too and reported against its published human score |
| C6 | **Coding in general: algorithms and what they cost.** 20 held-out programs (sorting, searching, recursion, dynamic programming, graph walks), each run on inputs of size ≤ 50. From those runs Ultron finds the law of how many steps (lines executed) each takes as the input grows, and names its kind (constant, logarithmic, linear, n log n, square, cube, exponential). Predicts the steps on inputs 20–1,000× bigger within 10% for ≥ 18/20, and the kind right for ≥ 18/20. Baselines: a straight line through the last two sizes, and lookup |
| C7 | **AI and machine learning.** Engc's own from-scratch autodiff and its neural-network library are the world. (a) **Gradients:** from watching `COMPUTE GRADIENTS OF` on ≤ 300 expressions, Ultron finds the laws of how a change flows back through `PLUS`, `TIMES`, `RAISED TO`, `THE EXP OF`, `THE TANH OF` and the rest, and predicts the printed gradients of **200 held-out expressions** (deeper, unseen combinations) within 10⁻⁶ relative error: ≥ 190/200, precision ≥ 99%. (b) **How learning behaves:** from training runs of gradient descent on held-out problems it finds the laws of the loss over steps (for example, a geometric fall whose ratio depends on the learning rate, and the learning rate beyond which training blows up) and predicts the loss at step 1,000 from the first 20 steps within 5% for ≥ 16/20 held-out runs, and the blow-up threshold within 10% for ≥ 8/10. (c) **Writing learners:** for **20 held-out datasets** (regression and classification, given only data and a loss it can measure), it writes, in Engc, a program that learns, built from its own gradient laws and C5's method; the program's held-out test loss is within 5% of a fixed reference (the least-squares or logistic-regression optimum computed by numpy, recorded before the work) on ≥ 16/20. Baselines: random search over parameters with the same number of loss evaluations, and the training-set mean (or majority class) |
| C8 | **Its twin, in Engc: writing itself.** Ultron writes its own program language's evaluator (the code that runs its laws) in Engc, by C5's method, from what it learned about that code in C4. Nobody writes the twin's code. On every law in its brain and 1,000 held-out inputs per law, the twin's answers are **identical** to the Python original. Then the twin of its law search: on lessons 0–4 and 28 it finds the identical laws |
| C9 | **Improving itself, constantly and safely.** A loop that never stops proposes changes to its own code and program language, each tried in a sandbox copy. A change is **kept** only if (1) every protected check passes (below), (2) it improves **learning** on held-out measures by ≥ 10% (search steps per law found, and experiences needed per law, on held-out lessons and tasks never used to choose the change), (3) it can be undone, and (4) the owner approves it. Exit: ≥ 3 kept changes, zero regressions, and at least one is a **building block Ultron invented** that later laws use. Baseline: random changes with the same budget, which must do worse |

**Protected checks** (C9, and every change in this stage): the curriculum (every lesson
passes on the first attempt), every exam, every failure-lab row, the blind tests, the
full pytest suite, and a retrain that is byte-for-byte identical, twice.

**Safety, built before C9.** Ultron can never change its own exams, sandbox or goals:
- exams, the sandbox, the protected checks and this plan are outside what it may
  propose to change, and the Judge checks their hashes before every run;
- every self-change is a reversible commit in a sandbox copy, with an audit log of what
  changed, why, and the measured evidence;
- no change reaches the main line without the owner's approval; a kill switch stops the
  loop.

Everything earlier stages passed must still pass: the curriculum, every exam, every
failure-lab row, the blind tests and the full test suite. A retrain stays byte-for-byte
identical.

## Rules for this stage

- **Nothing learned by hand-coding the answer.** No table from Engc words to meanings,
  no precedence table, no hand-written Engc translator. No pretrained code models.
- **Every belief carries its evidence**: each word's meaning keeps the runs that
  decided it, and a meaning is dropped when a run contradicts it.
- **Code lessons are numbered from 100** (lesson 100 is C1) so they never collide with
  the main curriculum's numbers, which other open work is still extending.
- **Engc is pinned** to one commit of Engc-V1; it is installed for the sandbox only.
- Report failures and null results as plainly as successes.

## Status

| # | Status |
|---|---|
| C1 | **met** (lesson 100, exam seed 7001): **198/200** held-out expressions right, precision **100%** (198 answered, 0 wrong; the 2 it declined have values too big for it to work out), from **328 runs** (107 the Trainer's, 221 its own). Baselines: lookup 0, nearest 37, left to right 29: margin 161 points (≥ 60 needed). Every word's meaning is one of its own laws found by its ordinary search; `MODULO`, which no short program explains, was found by **stepping** (a usual rule, when it fails, what instead) and checked to come round after whole turns. Its grammar, found from ordering constraints and its own experiments where rival grammars disagree: `**` tightest and chaining from the right, then `* % −(before a value)`, then `+ −`, then the comparisons, then `AND NOT`, then `OR`. Dev seeds 7501/7502: 198/200 and 197/200, precision 100%. Retrain byte-identical, every lesson passes on the first attempt, failure lab and all 115 tests pass |
| C2 | open (in progress: films of running programs, held-out program writer) |
| C3–C9 | open |

## Order

C1 → C2 → C3 → C4 → C5 → C6 → C7 → C8, with the safety pieces built before C9. ARC is re-measured
after each criterion is met.
