# The combined candidate: every open PR on one branch

Branch `claude/integrate-stages-5hnowy`, built from the base
`claude/trusting-lovelace-ddio2g` (b1af4fa) on 2026-10-11. It is a candidate for
merging the open work together, not a replacement for the PRs it contains.

## What is in it

| PR | Branch head | What it brings |
|---|---|---|
| #6 | 0d13160 | eyes that explain away touching things |
| #7 | bbbb7e2 | Stage 2 real footage: g (lesson 29), pendulums (lesson 30) |
| #8 | 50c7fdb | Stage 3 language: L1, L2, L3 |
| #11 | f85c852 | ARC cell rules (solver only, not in the curriculum) |
| #9, #10 | d8b59bd, fa9aaae | Stage 4 and Code stage plans (docs only) |

## One curriculum

Stage 2 and Stage 3 were built side by side, and both numbered their lessons from 29.
Here Stage 2 keeps its numbers and the language lessons move up by two:

| Lesson | What | Numbered in its own PR |
|---|---|---|
| 29 | g from real films of falling | 29 (#7) |
| 30 | real pendulums, the √length law | 30 (#7) |
| 31 | words by pointing (L1) | 29 (#8) |
| 32 | words for what happens (L2) | 30 (#8) |
| 33 | how words combine (L3) | 31 (#8) |

Lessons 0-28 are untouched. The language lessons keep their seeds (`seed + 29`, `+ 30`,
`+ 31`) and their exams keep seeds 1029, 1030 and 1031, so they are taught and examined
on exactly the worlds fixed before they were measured. Only the number changed.

One merge hazard was caught: Git merged PR #8's grammar lesson into the trainer as a
second `lesson.number == 31` branch and a second `31:` key in the concept names. Python
keeps the last duplicate key silently, so "kinds of thing" would have lost its name.
Both are fixed (grammar is 33).

## Checks on the combined tree

| Check | Result |
|---|---|
| Retrain twice (separate checkouts) | **byte-identical**: brain, exams, report card, transcript (sha256 5b2a9338...) |
| Lessons passed on the first attempt | **32 of 34**: lessons 30 and 31 fail (below) |
| Exams, lessons 0-29 | identical to the PR that owns each lesson (0-28 as #6, 29 as #7) |
| Blind tests | 60/60, 60/60, 50/50, and 14/14 on the non-blind example |
| Failure lab | running |
| Full test suite | running |

## Numbers that changed against the individual PRs

All differences come from PR #6's eyes. Lessons 0-29 are the same as in PR #6 (which
itself changed lesson 20's baselines and lesson 26's sphere count, as that PR reports).

**Lesson 30, real pendulums (#7): fails here, passes in #7.**
- On the 0.5 m film (Pendulum50cm) the eyes learned with PR #6 follow the bob for 125
  pictures and time 8 half swings with a spread of 0.123 s (8.5%); with #7's eyes, 80
  pictures, 4 half swings, 0.015 s (1.1%). The period is the same (1.444 against 1.445 s).
- Ultron's precision is set by its worst film, so it becomes 8.5%. At that precision the
  shortest law it finds is L/T (0.424), not L/T² ("found the law": 1/1 -> 0/1).
- V4 per film: 0.5 m no longer passes (0 of 3 films, was 1 of 3).
- The √length check still passes, but only because the error grew: power 0.530 ± 0.134
  (was 0.470 ± 0.029), constant 2.016 ± 0.014 (was 2.023 ± 0.013).
- Cause isolated: with #7's learned eyes and the combined code, the film gives 1.445 s
  ± 0.0155 over 4 half swings (as in #7); with the combined eyes and #7's code it gives
  the combined result. So it is the eyes learned under PR #6, not the motion code.

**Lesson 31, words by pointing, L1 (#8 lesson 29): fails here, passes in #8.**
- "Each word learned within 20 sentences": 9/10 (was 10/10). "the" settles after 40
  sentences instead of 20, "box" after 20 instead of 10.
- With PR #6's eyes Ultron sees every thing on all 120 teaching tables. With #8's eyes it
  missed one thing on 3 of them (tables 5, 94 and 99). So here the eyes are better, and
  the result is worse.
- Why: after 20 sentences the shortest lexicon and its best rival are 0.1 bits apart
  (with #8's eyes they were 0.2 bits apart, the other way round). Seeing table 5 correctly
  tips the tie, so at 20 sentences "the" is taken to mean a long shape. L1's ≤ 20 passed
  in #8 on a 0.2-bit margin.
- The other L1 rows hold: 200/200 named, 30/30 refused, margin 58 points (was 61; the
  co-occurrence baseline rose from 78 to 84 with the better eyes).

**Lesson 32, words for what happens, L2: better.** Comparing words 120/120 (was 113/120);
the co-occurrence baseline 106/120 (was 100/120). Naming events still 200/200.

**Lesson 33, grammar, L3: better.** Deeper nesting 70/70 (was 69/70); more joined phrases
59/60 and new places 70/70, as in #8.

**Lesson 29, g:** identical to #7 (g = 9.757 ± 0.157 m/s²).

## What it needs before it can merge

The exit tests are not moved. Two lessons fail on the combined tree, both because PR #6's
eyes reach parts of the curriculum built after it:
1. Stage 2 (PR #7): timing the 0.5 m pendulum with PR #6's eyes.
2. Stage 3 (PR #8): L1's ≤ 20 sentences rests on a 0.1-bit tie; a general fix belongs to
   the language work.

Once either PR changes, this branch is re-synced and every check above is run again.
