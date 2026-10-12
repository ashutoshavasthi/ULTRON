# The combined candidate: every open PR on one branch

Branch `claude/integrate-stages-5hnowy` (draft PR #12), built from the base
`claude/trusting-lovelace-ddio2g` (b1af4fa) on 2026-10-11 and 2026-10-12. It is a
candidate for merging the open work together, not a replacement for the PRs it contains.

## What is in it

| PR | Branch head | What it brings |
|---|---|---|
| #6 | 0d13160 | eyes that explain away touching things (see "The eyes" below) |
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

## The eyes

PR #6 explains away touching things, and to do so it also went back to a wider learned
spot (σ 1.0) and other handling trays. Lessons 20-33 of #7 and #8 were built and measured
with the base's eyes (σ 0.7, trays from touching to apart). Put together as #6 had them,
the first combined run passed **32 of 34** lessons:

- **Lesson 30, pendulums:** on the 0.5 m film the σ 1.0 eyes stitched two things into
  one swing (125 pictures, 8 half swings, 8.5% spread; with #7's eyes 80 pictures, 4 half
  swings, 1.1%). Precision follows the worst film, and at 8.5% the shortest law was L/T,
  not L/T². Shown directly: #7's learned eyes with the combined code time it as #7 did,
  and the combined eyes with #7's code reproduce the failure.
- **Lesson 31, L1:** "each word within 20 sentences" 9/10. The σ 1.0 eyes saw all 120
  teaching tables right (#8's eyes missed one thing on 3), which tipped a 0.1-bit tie
  between the shortest lexicon and its rival at 20 sentences.
- **V6:** BallTossOut found 9 of the lab's 11 marks (was 10).
- **Failure lab:** the events rows stopped with an error (numpy could not average the crops of a followed thing).

**The fix kept explaining away and changed what it sits on** (`senses/eyes.py`): the σ 0.7
eyes and the base's handling trays, whose learned weights are byte-for-byte the ones
lessons 20-33 were measured with. Explaining away is used close up and when a crowd is
looked at longer. And a noisy still scene is now looked at until it is a little cleaner
than usual (0.8 of its noise reference): without that, these eyes with explaining away
dipped to 22/25 on one 32%-noise set, as #6's own notes had measured.

| Eyes rows (25 trays a set) | σ 0.7, no explaining away (base) | #6 (σ 1.0) | **combined** |
|---|---|---|---|
| failure-lab protocol, 8 sets: 32% noise | 191 (worst 22) | 199 | **199** (worst 24) |
| faint | 200 | 198 | **200** |
| touching | 189 (worst 22) | 193 | **195** (worst 23) |
| overlapping (ungated) | 118 | 159 | 121 |
| **8 fresh sets (5001-5008):** 32% noise | 191 (worst 22) | 198 | **199** |
| faint | 199 | 199 | **200** |
| touching | 188 (worst 21) | 192 | **197** (worst 23) |
| overlapping (ungated) | 122 | 170 | 131 |

Normal, 16% noise and big are 200/200 for all three. The one row where the combined eyes
are below #6 is overlapping, which is not gated (merged blobs, reported only).

## Checks on the combined tree

| Check | Result |
|---|---|
| Retrain twice (separate checkouts) | **byte-identical**: brain, exams, report card, transcript |
| Lessons passed on the first attempt | **34 of 34** |
| Exams, lessons 21-33 | identical to the PR that built each lesson (#7 for 29-30, #8 for 31-33) |
| Exams, lessons 0-28 | identical, except lesson 20's memoriser baselines (lookup 1 → 0, nearest 1 → 2 of 25); Ultron's own scores unchanged; lesson 26 as in #7 and #8 (2477 of 2854 spheres; #6 had 2480) |
| Blind tests | 60/60, 60/60, 50/50, and 14/14 on the non-blind example |
| ARC-AGI-1 training split | 37.1% (148.5 of 400; 149 answers, 14 wrong), as #11 measured. The evaluation split was not opened |
| Failure lab | every row passes; every breakpoint as before. Rows identical to the source PRs except run times and the eyes: touching 25/25 (#6 and base 24), 32% noise 24/25 (#6 25, base 24), overlapping (ungated) 20/25 (#6 24, base 19). The language and events rows are exactly #8's |
| Full test suite | 144 of 145 pass. The one failure was PR #6's own explaining-away test: on 12 trays it showed one shared camera stream to the explaining-away eyes and then to the plain eyes, so they saw different pictures (11 vs 12). With each tray's pictures shown to both (as PR #6 did for the failure lab), explaining away gets 12/12 and plain 11/12; the test now pairs the pictures and passes |

Lesson 29 g = 9.757 ± 0.157 m/s², lesson 30 √length law power 0.470 ± 0.029 and constant
2.023 ± 0.013, L1 200/200 with every word within 20 sentences, L2 200/200 and 113/120,
L3 69/70, 59/60, 70/70: each exactly its own PR's number.
