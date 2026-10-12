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

For statements (C2) the given core knowledge is stated the same way: a line can change
one name, print one value, choose which line runs next, or hand back a value and leave
a routine; some lines open a block and some close one; a block can be run, skipped, run
again, or run once for each thing in a row; a routine is a block that runs when called,
with fresh memory holding what it was given. Three row-building pieces join its program
language (an empty row, a row with one more at its end, counting from one number to
another), offered to a search only when it asks for rows, so earlier lessons never see
them. Which mark opens a block, which word closes one, what each kind of line does,
which words are its name and its value, what each phrase means, how a call is written
and how a row prints are all found from the films.

## Exit test (fixed now, before the work)

Every test runs on held-out programs from a generator Ultron never sees, with exam seeds
70xx that are never used during development (development uses seeds 75xx). Every row
reports **precision** (answers right of answers given): Ultron may say "I don't know",
and a wrong answer counts against it. Every row beats baselines fixed here.

| # | Criterion |
|---|---|
| C1 | **Reading Engc: what expressions mean.** From ≤ 400 runs of one-line programs `PRINT <expression> .` (numbers 0–20, at most 2 operators, in the lesson), Ultron learns what each word and mark means (`PLUS`, `MINUS`, `TIMES`, `MODULO`, `RAISED TO`, the comparisons `IS GREATER THAN`, `IS LESS THAN`, `IS EQUAL TO`, `IS AT LEAST`, `IS AT MOST`, `IS NOT`, the logic words `AND`, `OR`, `NOT`, leading `MINUS`, their symbol twins `+ - * % ** > < == >= <= !=`, and brackets) and how they group. On **200 held-out expressions** with 3–6 operators, numbers up to 999 and combinations it never saw, it predicts the printed output **without running it**: ≥ 190/200 exactly right, precision ≥ 99%. Baselines: lookup (seen programs), nearest (the output of the most similar seen program), and left-to-right reading with the right word meanings but no grouping learned. Ultron must beat the best baseline by ≥ 30 points. (`DIVIDED BY` waits for C2, where decimals are printed.) |
| C2 | **Reading Engc: what statements do.** `SET`, `IF`/`ELSE`, `WHILE`, `FOR EACH`, lists, `THE LENGTH OF` and other library phrases, `DEFINE ROUTINE`/`CALL`/`RETURN`, recursion. Ultron learns each statement's effect as a law of change on its memory, from ≤ 1,000 runs watched line by line. On **200 held-out programs** of 5–40 lines, with loops that run up to 1,000 times and nesting deeper than any it watched, it predicts the full printed output without running it: ≥ 180/200, precision ≥ 98%. Baselines: lookup, nearest, and a straight-line reader that runs each line once in order; as in C1, Ultron must beat the best by ≥ 30 points |
| C3 | **Coding in general: a second language, faster.** Two languages it has never seen, each its own lesson: **an invented language** (lesson 102: the Trainer gives every Engc word and mark a fresh word or mark, so only the ideas carry over) and **a Python subset** (lesson 103: Python's own words and marks, blocks shown by indentation with no closing word, calls as `f ( n = 3 )`, rows as `[ 1 , 2 ]`, `len`, `sum`, `range`; Python has no "row with one more" in this subset). Each is learned to C1 **and** C2 level with **≤ 141 runs in all** (one third of the 425 Engc took: 328 for C1, 97 for C2), because what it learned about values, grouping, names, blocks, loops and calls carries over. Exams, fixed now: for each language, the C1 exam (200 held-out expressions, ≥ 190/200, precision ≥ 99%) and the C2 exam (200 held-out programs, ≥ 180/200, precision ≥ 98%), each translated by the Trainer from the Engc exam generators with fresh seeds (invented: 7003 and 7004; Python: 7005 and 7006), with the same baselines and the same ≥ 30-point margin |
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
| C2 | **met** (lesson 101, exam seed 7002): **197/200** held-out programs (5–40 lines, loops up to 1,000 turns, blocks nested up to 3 deep, recursion) printed exactly right, precision **100%** (197 answered, 0 wrong, 3 declined), from **97 runs** (92 the Trainer's, 5 its own). Baselines: lookup 0, nearest 0, straight line 64: margin 133 points. From the films it found which mark opens a block (`:`), which word closes one (`END`), the split word (`ELSE`), what each kind of line does (`SET` changes the name in place 2, `PRINT` prints, `IF` tests, `WHILE` tests again and again, `FOR` walks a row, `DEFINE` names a routine, `RETURN` hands back a value), how a call gives its inputs, how a row prints, and what each row phrase means as its own law (`THE SUM OF` = start at 0 and merge in each one). Two phrases it saw too seldom (`THE LENGTH OF`, `THE SUM OF`) it tested with programs it wrote itself. Dev: 9 lesson settings on dev seeds 7561–7569 gave 195–200/200, never a wrong answer. Retrain byte-identical; every lesson passes on the first attempt; failure lab and all 118 tests pass |
| C3 | **met** (lessons 102 and 103, exam seeds 7003–7006), never a wrong answer. **Invented language** (every word and mark new): C1 exam **196/200**, C2 exam **198/200**, precision 100%, from **124 runs** in all (≤ 141). Baselines: C1 left to right 46, nearest 29; C2 straight line 60, nearest 1. **Python subset**: C1 exam **197/200**, C2 exam **198/200**, precision 100%, from **91 runs** in all. Baselines: C1 left to right 34, nearest 20; C2 straight line 79, nearest 2. What carried over: the meanings of operators (it checks which known meaning a new word has with probes that split the candidates), its grammar (kept when the runs agree with it, so no grammar experiments were needed), and its picture of how programs run. What it found new in Python, from the films alone: blocks shown only by how far lines are pushed in (no closing word), lines known by the word after a name (`x = ...`), calls written by the routine's own name with the inputs inside a group, rows written between two marks, and that `range` can only be walked along (when it set a name to one and the name never appeared, it wrote a loop instead). Phrases it saw too seldom (`sum`, `range`, the invented words for THE SUM OF, THE NUMBERS, WITH ... ADDED) it tested with programs of its own. Dev seed 7590 over 4–5 lesson settings: invented 198 and 195/200, Python 198 and 196/200, never wrong. Retrain byte-identical; every lesson passes on the first attempt |
| C4–C9 | open |

## Order

C1 → C2 → C3 → C4 → C5 → C6 → C7 → C8, with the safety pieces built before C9. ARC is re-measured
after each criterion is met.
