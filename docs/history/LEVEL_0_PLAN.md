# Level 0: foundations

**Mission.** Give Ultron the foundations every later level stands on, and nothing more:
- it sees things;
- it acts with a body;
- it knows that things persist when hidden, don't pass through each other, and fall
  unless supported;
- it knows what its own actions do and how to get something out of reach;
- it notices when its world changes;
- it remembers its days and consolidates them.

This level is the starting point of the ladder ([ROADMAP.md](ROADMAP.md)), not a goal in
itself. It takes only as long as these foundations need; most effort goes to the levels
above it.

The test is whether **one general learner** passes it: Ultron's explanation engine, its
small learned networks, its memory and its curiosity. One hand-built module per test would
not count (rule 6, the ledger).

*Exit tests carried over unchanged from the 2026-10-15 plan (seeds and pass rules as
fixed then). The child-imitation parts were dropped on 2026-10-18; see "What changed".
Rules: [MASTER_PLAN.md](MASTER_PLAN.md) §4.*

---

## The room

Ultron's first world: one continuous 2D room seen from the side, built on the existing
simulated camera and scenes (`senses/camera.py`, `senses/tabletop.py`, `senses/world.py`).
Its true state stays with the simulator; only the Judge may read it.

**As built** (`ultron/room/`, `python -m ultron room`):
- **The ground:** three steps that touch, so nothing can get wedged between them: Ultron
  and the cushion it leans against, the mat, and the floor. Nothing ever goes under the
  ground.
- **Things:** balls, blocks, a cloth (things lying on it move with it), a screen (it hides
  what is behind it), and a light toy that glows when pressed. More things come with the
  work packages that first need them.
- **Physics:** gravity, support, solidity, friction. Collisions use boxes; a ball is a circle
  only in the picture.
  - A check of 24,000 steps over 6 seeds found nothing ever inside the ground.
  - Solid things overlapped by more than 0.3 units 4 times, by at most 2.1 units, each time
    briefly, when squeezed sideways.
- **Its body:** two arms of two joints, two hands that grasp, and a gaze. A hand pressing on
  the mat slides along it.
- **What Ultron gets:** only its senses (`body.Senses`):
  - a sharp, noisy 48×64 view around where it looks;
  - a blurry wide view around that;
  - its four joint angles and its gaze;
  - touch at its palms and body.

  Hand positions and the positions of things stay with the world.
- **Time:** experience is counted in days: 10,000 waking steps, then a night of sleep.
  - The Level 0 gate is to be reached within 90 days of experience.
  - Measured cost: about 6 ms per step with the explorer, or about 1.5 hours of compute for
    90 days.

## The teacher

Another agent in the room, scripted, with a head whose eyes show where it looks, and two
hands.
- **What it may do:** come and go; look at things; show, hand over and hide things; press
  the light toy. From Level 1 it will also name things and demonstrate, each change recorded
  here.
- **What it may not do:**
  - read Ultron's insides;
  - change its behaviour depending on how an exam is going;
  - reward the answer to an exam;
  - act on held-out exam seeds during learning.

The script is a fixed program with randomness, and everything it does is logged. A
failure-lab mode turns it off, and another makes its gaze mislead.

`ultron/room/teacher.py` SHA-256: `eefbbf7fffbae4463c3db1bd2d13c72a17c7e2275e7ff8d947117103a96a9dfb`

History of the script, all before any exam was measured:
- `498e7e25…`: WP2, then called the caregiver;
- `6d69dfa8…`: WP3, it answered crying;
- `eefbbf7f…`: 2026-10-18, child-imitation removed (no stroking, crying, smiles or
  peekaboo).

A test (`tests/test_room.py`) fails if the script changes without this line changing too.
It also fails if the script imports Ultron's brain or the Judge.

## The starting kit (fixed; rule 5)

| Kind | In the kit |
|---|---|
| Senses | The retina (`senses/retina.py`) on the camera picture; touch at each hand; where each hand is |
| Reflexes | Look toward motion and strong contrast; close the hand when the palm is touched; random arm movements (babbling) |
| Priors | Things are bounded lumps that move as one; a moving thing is followed along a connected path (`senses/track.py`); things that start moving by themselves are agents; faces stand out; sets of 1–3 are seen at a glance, larger amounts only roughly |
| Learning | The explanation engine (MDL search, kinds, laws with exceptions, rival laws); training small networks on its own experience; episodic memory; sleep (consolidation and abstraction, `brain/abstraction.py`) |
| Drives | Curiosity as learning progress (`brain/curiosity.py`); attention to the new (familiar things become boring) |

**Proposed additions from WP3, waiting for the owner's approval (rule 5).** Building its
eyes needed three things the list above does not name:
- **a blurry wide view** (`Senses.around`): without it, nothing outside the sharp middle
  could ever catch its eye;
- **saccadic suppression:** change is not noticed while the eyes move, because while they
  move everything seems to change;
- **inhibition of return:** a spot it has just looked away from can't pull its eyes
  straight back.

Until the owner approves them they are marked as proposed in [LEDGER.md](LEDGER.md), and
the Level 0 gate can't pass with them unapproved.

**Not in the kit** (it must be learned):
- object permanence;
- solidity, support and gravity;
- what its hands do;
- where others look;
- exact counting.

Exact counting was given in lessons 0–28. Those banked results are re-examined at their
own level's gate.

---

## Level 0 gate (L0-1 to L0-11)

Each test is on held-out situations (exam seeds 8001 onwards, never used in learning).
"Was" names the test's number in the 2026-10-15 plan; its pass rule is unchanged.

| # | Test | Pass rule | Baselines | Was |
|---|---|---|---|---|
| L0-1 | **Seeing things, with its retina.** *Changed 2026-10-18 by the owner's decision, before any exam run (pass rule unchanged):* at Level 0, seeing is the job of the retina in the starting kit (bounded lumps that stand out from their surroundings, `brain/explorer.py: lumps`). Learned eyes move to the level that needs them (clutter, real films). Scenes: 0–5 toys at rest, whole in view, its body out of view, no teacher, screen or cloth; looked at once for positions, 5 times for the count (`judge/room_exams.py`) | On 25 held-out room scenes: every toy found within 1.5 pixels in ≥ 23/25, and the count right in ≥ 23/25 | Bright spots with no comparison to their surroundings (`by_brightness`) | N2 |
| L0-2 | **Reaching.** From babbling only, no reaching lessons | On 100 held-out toy positions, including ones its hands never touched: the hand's first reach ends within one toy-width of the toy in ≥ 90 | Random reaching; reaching to the nearest remembered position | N3 |
| L0-3 | **Memory of yesterday** | On 50 held-out probes about the previous day ("where was the red ball left?"), asked as a search task: it looks there first in ≥ 45 | Search where it last looked; random | N5 |
| L0-4 | **Sleep consolidates** | After a night, stored experiences fall ≥ 10× while every prediction on held-out events from that day stays as good (within 1 point) | Keep everything; keep a random 10% | N6 |
| L0-5 | **Things still exist when hidden** (violation of expectation) | On 100 held-out occlusion events (a toy goes behind a screen; then it is there, or impossibly gone or changed), its surprise (its own prediction error) is larger for the impossible outcome in ≥ 95 | A pixel predictor that repeats the last picture; the same Ultron with episodic memory switched off | I1 |
| L0-6 | **Solidity, support, gravity** | 100 held-out events each (passing through, floating, falling): surprise larger for the impossible one in ≥ 95 each. Acting: when putting a toy down, it puts it on a support in ≥ 95 of 100 | As L0-5 | I2 |
| L0-7 | **IntPhys 2019** (outside yardstick) | Scored with the benchmark's own metric on its public sets. The pass rule is copied from the paper in WP0, before any run: beat its published baseline models, and come within its published human performance on each block (object permanence, shape constancy, spatio-temporal continuity). Human performance is a checkpoint here, not a ceiling | The benchmark's published baselines | I3 |
| L0-8 | **Searching for hidden things** | A toy is hidden under one of 2–3 cloths in view. At location A it finds it on the first reach in ≥ 95 of 100. After hiding at A several times, the toy is hidden at B in view: it searches B first in ≥ 90 of 100, at delays of 0–5 seconds. Errors against delay are reported | Search the last place it found something; random | I4 |
| L0-9 | **What its actions do** | On 100 held-out pushes, pulls, drops and presses of toys it never touched, the next positions of the things it acted on are within one toy-width in ≥ 90 | A passive learner that watched the same films without acting (as `reports/active_vs_passive.json`) | I5 |
| L0-10 | **Getting what is out of reach** (means-end) | A toy lies on a cloth out of reach: it pulls the cloth then grasps, on the first try, in ≥ 80 of 100 held-out layouts. When the toy lies *beside* the cloth, it doesn't pull in ≥ 80 of 100 | Random actions; reaching straight for the toy | I6 |
| L0-11 | **It knows when its world is wrong** | On days where one law changes once (a cloth becomes sticky, a light toy stops lighting), it notices at the first contradicting event in ≥ 95 of 100 and relearns within 20 events | Never relearning; relearning everything | I10 |

**If IntPhys can't be obtained (WP0):** the gate uses its published task designs, rebuilt
in the room with held-out seeds, and says so plainly. The gate is then marked **"passed
without its outside yardstick"** until the benchmark is run.

**The owner's blind check (rule 2):** the owner writes 10 situations from this table's
public wording, without seeing the code. Ultron must do as the test says in ≥ 8.

**Moved to other levels:**
- old N1 (habituation) is now a **mechanism** checked in the failure lab (attention row
  below), not a gate test;
- old N4 (telling the teacher apart and where it looks), I7 (gaze following) and I8
  (imitation) go to **Level 1**, where Ultron learns from a teacher;
- old I9 (the Baby Intuitions Benchmark, agents' goals) goes to **Level 2**, as a test of
  modelling other agents.

---

## What the failure lab found (WP3, development seeds)

Rows in `judge/room_lab.py`, run with `python -m ultron stress`.

| Row | Result |
|---|---|
| **Attention to the new** against camera noise (5 seeds each; arms held still, one toy dangled 10 times, then a new one) | 4/5 habituate at the normal noise (0.08) and at 2× (0.16). It **breaks at 3×** (0.24: 3/5) and is gone at 4× (0.32: 1/5). At normal noise, looking falls from about 14 steps to 5, and the new toy gets 20 |
| **Curiosity and the noisy TV** (share of time in postures where the palm feels pure noise; 2 seeds) | With 1, 3 and 5 noisy postures of 9: learning progress 7%, 35%, 54%; random babbling 11%, 38%, 58%; chasing the biggest error 38%, 43%, 66%. Curiosity never gets stuck in the noise, and the error-chaser does. But it keeps away only a little better than babbling at random |

**How the curiosity row got there.** It broke twice first (at 3 noisy postures: 79%, then
64% of the time in noise, against 52% and 38% at random). It took three fixes:
- one averaged record per posture per stretch of babbling, instead of one every step;
- a hand pressing on the mat slides along it instead of freezing (a body fix);
- a posture it aims for and never reaches counts as a try with nothing learned.

None of the three adds a mechanism: they are how curiosity and the body work.

A comfort row (with and without the caregiver) was measured on 2026-10-15 and removed on
2026-10-18, together with comfort itself.

## WP4 so far (development seeds; the exam seeds are untouched)

L0-1's protocol runs (`judge/room_exams.py`, `seeing()`). In each scene: are all the toys
found within 1.5 pixels, and is the count right? There are two development sets: 5101–5125,
used while building, and 5201–5225, kept back to check them.

| Who looks | All toys found | Count right |
|---|---|---|
| **Its retina** (what L0-1 now tests) | 22/25 and 20/25 | 20/25 and 19/25 |
| Bright spots, no surround (the baseline) | 8/25 and 8/25 | 11/25 and 11/25 |
| Learned eyes, self-taught on what lasts (first version; now a prototype) | 7/25 after 1 day and after 2 | 12/25 after 1 day, 8/25 after 2 |

**Not yet at the gate's 23/25.** Nearly every remaining error is the **front face of the
mat**: a long bright band whose pieces between toys pass as lumps. A few are toys missed
when five crowd together. Tried while building, none of which reached 23/25 on both sets:
- a smallest-lump size of 10 pixels;
- splitting lumps with two peaks;
- requiring lumps to be compact;
- looking longer (averaging 5 aligned glances), which put toys better (22/25 on both sets)
  but counted worse (the band showed more).

**The principled fix:** Ultron learns which parts of what it sees are its room, the fixed
structure that is there every time it looks (the mat's edge), and which are things that
come and go. It needs that anyway for L0-11 (noticing that its world changed), so it is
built in WP5 and L0-1 is re-measured then.

**The first approach, kept as a prototype** (`Explorer(learn_eyes=True)`): eyes self-taught
at night on lumps that last across glimpses, as lesson 26 did. They lost to the retina
they learn from. The likely causes:
- the network's 7×7 view is smaller than the larger toys;
- the self-taught labels are inconsistent (some real toys missed, its own arms and the
  teacher included).

What was tried for them:
- average and median surrounds;
- bright and dark lumps, and bright only;
- labels from every lump, and only from lumps that last;
- brightness, ON, and ON and OFF as input.

## Work packages

| WP | What | Done when |
|---|---|---|
| WP0 | Outside yardstick: fetch IntPhys 2019; copy its metric and published human and model results into this plan | The pass rule is written here and committed, or the fallback is recorded |
| WP1 | The room and the body; days and nights; the step cost measured | **done** |
| WP2 | The teacher's script | **done** |
| WP3 | Attention, curiosity, episodic memory, sleep (`brain/explorer.py`); failure-lab rows | **done** |
| WP4 | Seeing in the room: L0-1's protocol, its retina and a baseline (learned eyes kept as a prototype) | L0-1 measurable: **done**; see "WP4 so far" |
| WP5 | Objects and actions: predicting what happens, searching, means-end, noticing change; and **knowing its room** (what is always there, as opposed to things), then L0-1 re-measured | L0-2 to L0-11 measurable |
| WP6 | **Level 0 gate:** every test, the owner's blind check, the ledger, merge to `main`; the Level 1 plan written with its exit tests fixed | Every test met, or the gate reported as not passed |

## Rules for this level

- Everything Ultron has passed before must still pass (lessons 0–33 and their exams, the
  failure lab, the blind tests). A retrain stays byte-identical.
- No pretrained networks and no language model.
- Exam seeds 8001 onwards are never used in learning, and exams are never shown to the
  teacher's script.
- **The ledger:** each work package lists every new hand-written mechanism it added, and
  why.
- A pass rule is never changed after a result is seen. If a protocol has to change, both
  results are reported.

## What changed on 2026-10-18

The 2026-10-15 plan framed this level as "Ages 0 and 1: newborn and infant" and imitated a
baby: a caregiver who comforted it, crying, infant-seat protocols, and milestones judged by
the age at which infants pass them. The owner's goal is growth *from* a child's start
*toward* the most advanced intelligence, not a simulated child. So the following were
removed or renamed:
- comfort and crying were removed;
- the caregiver became a teacher;
- "newborn" became the explorer, and the nursery became the room;
- infant ages became test numbers;
- the human comparisons that were only about imitating infants were dropped.

Every exit test that is a foundation was kept, with its pass rule unchanged.

## Status

| # | Status |
|---|---|
| WP1–WP3 | done (2026-10-15; reframed 2026-10-18) |
| WP0, WP4–WP6 | open |
| L0-1 to L0-11 | open (main line) |
