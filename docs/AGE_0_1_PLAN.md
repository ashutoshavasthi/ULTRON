# Ages 0 and 1: newborn and infant

**Mission.** Give Ultron what a baby has in its first year: a body that lives in one
world, day after day, with a person who looks after it. By the end of the year it should
know that hidden things still exist, that things don't pass through each other or float in
mid-air, what its own hands do, how to get a toy it can't reach, where its caregiver is
looking, and how to copy what the caregiver does.

Nothing here is new to psychology. Every milestone below is a classic test that real
infants are given, and each names the age at which infants pass it. The new part is
passing them with **one general learner** (Ultron's explanation engine, its small learned
networks, its memory and its drives) instead of one hand-built module per test.

*Plan fixed 2026-10-15, before any Age 0 or Age 1 work. Rules: [MASTER_PLAN.md](MASTER_PLAN.md) §4.*

---

## The nursery

One continuous 2D room, seen from the side, built on the existing simulated camera and
scenes (`senses/camera.py`, `senses/tabletop.py`, `senses/world.py`). Its true state stays
with the simulator; only the Judge may read it.

- **Things:** balls, blocks, cups, cloths, a box with a lid, screens that can hide things,
  a toy that lights up when pressed, a stick, a mirror (used from Age 2). There are several
  of each, in varied sizes, brightness and colours.
- **Physics:** gravity, support, solidity (things don't pass through each other), friction,
  and containment (a cup over a ball hides it and moves it).
- **Ultron's body:** a gaze (where its camera view points, with sharp vision only near its
  centre), two arms with hands, touch at the hands, and a sense of where its hands are.
  Each step it may move its gaze and its hands, and grasp or let go.
- **Time:** a **day** is 10,000 waking steps followed by a night of sleep. Days are counted
  and reported next to children's ages (rule 4). If a day must be shortened, that is
  recorded **before any milestone is measured**.
  - Measured in WP1: 4.5 ms per step with reflexes only, which is 45 s per day and about
    67 minutes for the 90-day Age 0 budget. The day stays at 10,000 steps.
- **Budgets:** the Age 0 gate within 90 simulated days; the Age 1 gate within 365 days in
  all.

**As built in WP1** (`ultron/nursery/`, `python -m ultron nursery`):
- **The ground:** three steps that touch, so nothing can get wedged between them: the
  baby and the cushion it leans against, the mat, and the floor. Nothing ever goes under
  the ground.
- **Collisions** use boxes. A ball is a circle only in the picture.
- **How good the physics is:** a check of 24,000 steps of babbling over 6 seeds found
  nothing ever inside the ground. Solid things overlapped by more than 0.3 units 4 times,
  by at most 2.1 units, each time briefly, when things were squeezed together sideways.
- **What exists now:** balls, blocks, a cloth, a screen and the light toy. Cups, the box
  with a lid, the stick and the mirror come with the work packages that first need them
  (WP6 and the Toddler plan).
- **What Ultron gets:** only its senses (`body.Senses`): the view around where it looks,
  its four joint angles, its gaze, and touch at its palms and body. Hand positions and the
  positions of things stay with the world.

## The caregiver

A scripted person with a face (eyes that open and close), a head that turns, and two hands.

**What it may do:** come and go; look at things; show, hand over, hide and move toys; play
peekaboo; press the light toy; smile when Ultron is near and active (the comfort signal);
come and stroke the baby when it cries (added in WP3, as a parent answers crying).

**What it may not do:**
- read Ultron's insides;
- change its behaviour depending on how an exam is going;
- reward the answer to a milestone;
- act on held-out exam seeds during learning.

The script is a fixed program with randomness, **committed with its hash before WP5**.
Everything it does is logged. A failure-lab row turns it off, and another makes its gaze
mislead, so we can see what Ultron learns from it and what it doesn't.

`ultron/nursery/caregiver.py` SHA-256: `6d69dfa82030715513b24824e920e2505c8198d5fe73d7e41dcb5f026067a54e`

History of the script, all before any milestone was measured: `498e7e25…` (WP2), then
`6d69dfa8…` (WP3: it hears the baby cry and comes to stroke it).

A test (`tests/test_nursery.py`) fails if the script changes without this line changing
too. It also fails if the script imports Ultron's brain or the Judge.

## The innate endowment (fixed; rule 5)

| Kind | Innate |
|---|---|
| Senses | The retina (`senses/retina.py`) on the camera picture; touch at each hand; where each hand is |
| Reflexes | Look toward motion and strong contrast; close the hand when the palm is touched; random arm movements (motor babbling) |
| Core knowledge | Things are bounded lumps that move as one; a moving thing is followed along a connected path (`senses/track.py`); things that start moving by themselves are agents; faces stand out; sets of 1–3 are seen at a glance, larger amounts only roughly |
| Learning | The explanation engine (MDL search, kinds, laws with exceptions, rival laws); training small networks on its own experience (as the eyes were trained); episodic memory; sleep (consolidation and abstraction, `brain/abstraction.py`) |
| Drives | Curiosity as learning progress (`brain/curiosity.py`); habituation (familiar things become boring, new things interesting); comfort near the caregiver |

**Proposed additions from WP3, waiting for the owner's approval (rule 5).** Building the
newborn's eyes needed four things the list above does not name. Each is something human
newborns have:
- **a blurry wide view** (`Senses.around`): a coarse picture of almost everything around
  where it looks, as newborns see coarsely almost everywhere. Without it, a toy outside the
  sharp middle can never catch its eye;
- **saccadic suppression:** change in the wide view is not noticed while the eyes move,
  because while they move everything seems to change;
- **inhibition of return:** a spot it has just looked away from can't pull its eyes
  straight back;
- **crying** when comfort is low.

Until the owner approves them they are marked as proposed in the ledger
([LEDGER.md](LEDGER.md)), and the Age 0 gate can't pass with them unapproved.

**Not innate** (it must be learned):
- object permanence;
- solidity, support and gravity;
- what its hands do;
- where others look;
- imitation;
- exact counting, which was innate in lessons 0–28. Those banked lessons keep running as
  regression checks, and are re-examined under this endowment at their own ages' gates.

---

## Age 0 gate: newborn (N1–N6)

Each milestone is tested on held-out situations (exam seeds 8001 onwards, never used in
learning).

| # | Milestone | Pass rule | Baselines | Human comparison |
|---|---|---|---|---|
| N1 | **Habituation and novelty.** One event is shown again and again, then a new one. *Protocol details, added in WP3 before N1 was measured (pass rule unchanged):* the baby sits in an infant seat (its arms rest); the experimenter dangles a toy in front of it, swinging 8 units side to side, for 60-step showings with 40-step gaps; the new event is a toy of a different colour; looking means the toy is within 10 units of the middle of its view | In ≥ 18 of 20 held-out event pairs: looking time (steps with gaze on the event) falls to ≤ 50% of the first three showings within 10 showings, and recovers to ≥ 2× the habituated level for the new event | Random gaze; the motion-and-contrast reflex alone | The standard infant-controlled habituation criterion (looking falls to 50%), used with newborns |
| N2 | **The eyes, in the nursery.** Lesson 19 (eyes trained from touch) re-hosted: the training pairs come from its own grasps during the days | On 25 held-out nursery scenes: every toy found within 1.5 pixels in ≥ 23/25, and the count right in ≥ 23/25 | The untrained retina's blobs | None direct (engineering milestone) |
| N3 | **A body map.** From babbling only, no reaching lessons | On 100 held-out toy positions, including ones its hands never touched: the hand's first reach ends within one toy-width of the toy in ≥ 90 | Random reaching; reaching to the nearest position remembered | Reaching for seen objects appears at about 3–5 months |
| N4 | **The caregiver and where they look.** | On 100 held-out scenes: tells the caregiver from toys in ≥ 98; the caregiver's head direction within 30° in ≥ 90 | A detector of the biggest moving thing | Newborns prefer faces; head direction is a precursor to gaze following (I7) |
| N5 | **Yesterday.** Episodic memory | On 50 held-out probes about the previous day ("where was the red cup left?"), asked as a search task: it looks there first in ≥ 45 | Search where it last looked; random | None direct |
| N6 | **Sleep consolidates.** | After a night, stored experiences fall ≥ 10× while every prediction on held-out events from that day stays as good (within 1 point) | Keep everything; keep a random 10% | Sleep-dependent consolidation is well documented in infants, but not as a pass/fail test, so this is an engineering milestone |

**The owner's blind check (rule 2):** the owner writes 10 nursery situations from this
table's public wording, without seeing the code. Ultron must behave as the milestone says
in ≥ 8.

---

## Age 1 gate: infant (I1–I10)

| # | Milestone | Pass rule | Baselines | Human comparison |
|---|---|---|---|---|
| I1 | **Things still exist when hidden** (violation of expectation) | On 100 held-out occlusion events (a toy goes behind a screen; then it is there, or impossibly gone or changed), its surprise (its own prediction error) is larger for the impossible outcome in ≥ 95 | A pixel predictor that repeats the last picture; the same Ultron with episodic memory switched off | Infants show this by about 3.5–5 months (Baillargeon) |
| I2 | **Solidity, support, gravity** | 100 held-out events each (passing through, floating, falling): surprise larger for the impossible one in ≥ 95 each. Acting: when putting a toy down, it puts it on a support in ≥ 95 of 100 | As I1 | Support and solidity expectations develop over 3–12 months |
| I3 | **IntPhys 2019** (outside yardstick) | Scored with the benchmark's own metric on its public sets. The pass rule is copied from the paper in WP0, before any run: beat its published baseline models and come within its published human performance on each block (object permanence, shape constancy, spatio-temporal continuity) | The benchmark's published baselines | The benchmark's published human results |
| I4 | **Search and A-not-B** | A toy is hidden under one of 2–3 cloths in view. At location A it finds it on the first reach in ≥ 95 of 100. After hiding at A several times, the toy is hidden at B in view: it searches B first in ≥ 90 of 100, at delays of 0–5 seconds. Errors against delay are reported | Search the last place it found something; random | Infants of 8–10 months reach back to A (the A-not-B error), and by about 12 months they don't (Piaget; Diamond 1985). Its error curve is reported against theirs |
| I5 | **What its actions do** | On 100 held-out pushes, pulls, drops and presses of toys it never touched, the next positions of the things it acted on are within one toy-width in ≥ 90 | A passive learner that watched the same films without acting (as `reports/active_vs_passive.json`) | Infants learn action–effect contingencies from about 2–3 months (the mobile studies) |
| I6 | **Means-end: pulling the cloth** | A toy lies on a cloth out of reach: it pulls the cloth then grasps, on the first try, in ≥ 80 of 100 held-out layouts. When the toy lies *beside* the cloth, it doesn't pull in ≥ 80 of 100 | Random actions; reaching straight for the toy | Intentional cloth pulling with the control condition at about 8–12 months (Willatts) |
| I7 | **Gaze following** | When the caregiver turns to look at one of 2–4 toys, Ultron looks at the same toy in ≥ 90 of 100 held-out trials with the caregiver's eyes **open**, and in ≤ 20 of 100 with eyes **closed** | Following head motion only; random | 10–11-month-olds follow open-eyed turns but not closed-eyed ones (Brooks & Meltzoff 2005) |
| I8 | **Imitation, now and later** | The caregiver shows a new act on a new toy (for example, pressing the light toy with a hand). Ultron makes the same outcome within 3 tries in ≥ 80 of 100. Deferred: after a night's sleep, with the toy shown again, in ≥ 70 of 100 | Trying random acts on the toy | Deferred imitation of a new act after a delay by 9–14 months (Meltzoff 1988) |
| I9 | **Baby Intuitions Benchmark** (outside yardstick) | Scored on its public evaluation (agents' goals, preferences, efficient action, inaccessible goals) with its own metric. The pass rule is copied from the paper in WP0 before any run: beat its published model baselines on each task family | The benchmark's published baselines | Infants' expectations from the studies it was built from |
| I10 | **It knows when its world is wrong** | In nursery days where one law changes once (a cloth becomes sticky, a light toy stops lighting), it notices at the first contradicting event in ≥ 95 of 100 and relearns within 20 events | Never relearning; relearning everything | None direct |

**Fallback if an outside benchmark can't be obtained (WP0):**
- The gate uses that benchmark's published *task designs*, rebuilt in the nursery with
  held-out seeds, and says so plainly.
- The gate is then marked **"passed without its outside yardstick"**. That mark stays until
  the benchmark is run.

**The owner's blind check:** 10 situations written by the owner from the public wording of
I1–I10. Ultron must behave like a 12-month-old in ≥ 8.

---

## Work packages

| WP | What | Done when |
|---|---|---|
| WP0 | Outside yardsticks: fetch IntPhys 2019 and the Baby Intuitions Benchmark; copy their metrics and published human and model results into this plan | Both pass rules written here and committed, or the fallback recorded |
| WP1 | The nursery and the body on the existing camera, retina and scenes; days and nights; the step cost measured | A day runs; a retrain is byte-identical |
| WP2 | The caregiver's script | Committed with its hash; failure-lab rows "caregiver off" and "misleading gaze" exist |
| WP3 | Drives, episodic memory, sleep | Habituation and curiosity measured in the failure lab |
| WP4 | Lesson 19 re-hosted in the nursery | N2 measurable |
| WP5 | **Age 0 gate**: N1–N6, the owner's blind check, the ledger, merge to `main` | Every milestone met, or the gate reported as not passed |
| WP6 | Objects, actions, the caregiver's gaze, imitation | I1–I10 measurable |
| WP7 | **Age 1 gate**: I1–I10, the owner's blind check, the ledger, merge to `main`; the Toddler plan written with its exit tests fixed | Every milestone met, or the gate reported as not passed |

## Rules for these ages

- Everything Ultron has passed before must still pass (lessons 0–33 and their exams, the
  failure lab, the blind tests). A retrain stays byte-identical.
- No pretrained networks and no language model (design law 7).
- Exam seeds 8001 onwards are never used in learning, and exams are never shown to the
  caregiver's script.
- **The ledger:** each work package lists every new hand-written mechanism it added and
  why. The list is printed in the gate's verdict.
- A pass rule is never changed after a result is seen. If a protocol has to change, both
  results are reported.

## Status

| # | Status |
|---|---|
| WP1 | **done** (2026-10-15): the nursery, the body, days and nights, the innate reflexes (`brain/reflexes.py`); 4.5 ms per step; deterministic (same seed, same day); the curriculum's retrain unchanged |
| WP2 | **done** (2026-10-15): the caregiver's script, hash recorded above; modes `normal`, `off`, `misleading_gaze`. The failure-lab rows that use the modes are added in WP3, when there is a learner to stress |
| WP3 | **done** (2026-10-15): the newborn mind (`brain/newborn.py`): habituation, curiosity by learning progress over arm postures, comfort and crying, episodic memory of fixations, sleep. Failure-lab rows (`judge/nursery_lab.py`): habituation (breaks at 3× camera noise), curiosity and the noisy TV, the caregiver switched off. The misleading-gaze row joins with gaze following (WP6). Four innate additions are proposed above and wait for the owner |
| WP0, WP4–WP7 | open |
| N1–N6 | open (main line) |
| I1–I10 | open (exit tests fixed) |
