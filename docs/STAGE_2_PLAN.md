# Stage 2: the real world through its eyes

**Mission.** Ultron has seen one real film, and its eyes don't generalise. Stage 2 gives
it eyes that hold up in hard conditions, then has it rediscover physics from **real
footage**.

## Exit test (fixed now, from `MASTER_PLAN.md`)

| # | Criterion |
|---|---|
| V1 | **Eyes:** every gating row of the failure lab's *eyes* experiment ≥ 23/25 trays counted right, with no regressions elsewhere in the lab |
| V2 | **Diffusion** from the real microscope film (lesson 26): Ultron's D agrees with the scientists' own tool within measured error |
| V3 | **g** from real footage of falling, within measured error |
| V4 | **Pendulum periods** from real footage, within measured error (and the √length law) |
| V5 | **Restitution** from real footage of bouncing, within measured error |
| V6 | **Detection on par with lab tools** on the same real footage (positions, counts) |

Everything Stage 1 passed must still pass: the curriculum, every exam, the failure lab
and the blind tests. A retrain must stay byte for byte identical.

## Where the eyes stand (failure lab, 2026-10-11)

| Condition | Trays counted right |
|---|---|
| normal (8% noise) | 25/25 |
| 16% noise | 1/25 |
| 32% noise | 0/25 |
| big things (radius 4–6) | 0/25 |
| faint things (30% brightness) | 2/25 |
| touching (gap = diameter) | 19/25 |
| overlapping | 14/25 (a physical limit, reported only) |

## Status

| # | Status |
|---|---|
| V1 | ✅ **met, and robust** (2026-10-11): every gating eyes row ≥ 23/25 on the failure lab's trays **and on three sets of unseen trays** (normal 25; 16% noise 25; 32% noise 23–24; big 25; faint 25; touching 23–24). Before Stage 2: 25, 1, 0, 0, 2, 19. No regressions elsewhere in the lab; 29 lessons pass on the first attempt; a retrain is byte-identical; 111 tests pass |
| V2 | ✅ **met** (2026-10-11): lesson 26 is in the curriculum and passes on the first attempt. From the real trackpy microscope film: Einstein's law (spread² ∝ time); D = 0.396 µm²/s against the scientists' tool trackpy's 0.412 (4%) and the textbook's 0.455 (13%); on 150 frames it never learned from it finds 87% of trackpy's spheres and predicts the spread at 1–2 s (21/21); it claims no law for a single sphere |
| V3 | ✅ **met** (2026-10-11): lesson 29. From three real lab films (Tracker project, on GitHub) Ultron finds the law of falling itself (change of speed ∝ time) and measures **g = 9.65 ± 0.15 m/s²** (9.80 at the lab: 1.0 errors off; error 1.6%). Films: 9.95 ± 0.10, 9.56 ± 0.18, 9.45 ± 0.06; they disagree more than their fits admit, so the spread across films is the error. 30 lessons pass on the first attempt; a retrain is byte-identical; every exam, failure-lab row and blind test unchanged (60/60, 60/60, 50/50); 115 tests pass. Report: [`stage2_v3_falling.md`](../reports/stage2_v3_falling.md) |
| V4–V6 | open. Real footage found on GitHub: two pendulums (0.785 m over about three swings; 1 m over one swing) and a bouncing cart, with the lab's Tracker files. Two lengths are too few for the √length law, so a third is still needed |

How V1 was met (`senses/eyes.py`, `senses/world.py`):
- **Looking longer:** when a still scene is noisier than usual (its own noise measure, as
  the retina's), pictures are lined up against shake and averaged until as clean as
  usual. 16% noise: 1 → 25; 32%: 0 → 25.
- **Adapting to the light:** the background is moved back to where the eyes are used to
  it, but only when it is noticeably off. In a dim scene, once looking long enough makes
  something really stand out, the contrast is turned up to how things look in its clear
  views. Faint: 2 → 25.
- **Stepping back:** the picture shrunk 2× and 3×, kept only when its eyes respond
  clearly more strongly there. Big things: 0 → 25.
- **Broader handling:** lesson 19 handles things of varied size, with spacing from
  touching (2× radius) to well apart (4×), and learns a sharper spot (σ 0.7). Light and
  noise are left to how it looks: training on varied light made the eyes fire on
  real-film noise.
- **Looking longer at a crowded scene:** when the things it sees sit closer than 5 px,
  it averages 4 pictures before counting, so touching neighbours no longer blur into one.
  Touching: 19 → 23–24 on every tray set, where it had been 16–24.

Two measured pitfalls, fixed:
- recentring the background on every picture dimmed small crowded things;
- "usual brightness" averaged over dim scenes was too low.

How V2 was met:
- **A false law closed.** "Each position is near the last" passed as a law of change for
  one jiggling sphere. A recurrence must now explain at least 90% of the *change* (the
  rule measurement laws already follow), so a random walk has none (test).
- **Eyes learn form; looking handles light.** Handling in varied light and noise made
  the eyes fire on real-film noise (66% vs 81% of trackpy's spheres before
  self-teaching). Handling now varies only size and spacing, and noise and dim light are
  handled at looking time (V1 still met).
- **A new instrument kept apart.** Self-teaching on the film made the everyday eyes worse
  at touching things (24 → 18 of 25). The adapted eyes are now kept separate
  (`brain.microscope_eyes`) and used for the microscope only.

## Work packages

### WP1: eyes that generalise (V1)

Each change is general, plausible for an animal, and measured against every row. It is
kept only if no row regresses and the curriculum still passes.

1. **Look longer at a still scene.** Average several frames, aligned for camera shake,
   until the picture's own noise, which Ultron measures itself (as the retina does), is
   down to what its eyes grew up with. This targets the 16% and 32% noise rows.
2. **Adapt to the light.** Choose "how strong must a spot be" relative to the picture's
   own noise, not as one fixed number. This targets the faint row.
3. **Step back.** Look at the picture shrunk 2× and 3× as well, and keep, for each thing,
   the scale where it looks most like the things the eyes learned. This targets the big
   row.
4. **Broader handling.** In lesson 19, touch also covers things that are close
   together, faint, larger, and in dimmer and noisier light, as a child handles things in
   all conditions. This targets the touching row and makes the eyes more robust overall.

### WP2: lesson 26, the real microscope film (V2)

Finish the work in progress end to end: real particles through the retina, tracks,
mean squared displacement, then D compared with the scientists' tool on the same film.

### How V3 is judged (written 2026-10-11, before any of Ultron's measurements)

The exit test says "g from real footage of falling, within measured error". It is not
changed; these are the details it left open, fixed before measuring:

- **The films** are every real film of a freely falling or tossed ball in the source
  found (the Tracker project's films on GitHub, `OpenSourcePhysics/resources` and
  `tracker-website`, pinned commits): *BallTossOut*, *BallDrop* and *BallTossUp*, all three
  filmed at Cabrillo College with the same metre stick in view. *FreeFall* (a kitchen
  film) is left out because nothing in it gives a readable scale; *TossOutStrobe* and
  *WhichLandsFirst* are left out because they are composites made for teaching, not plain
  footage. This choice was made from what the films show, not from any g measured on them.
- **What Ultron is given:** the pictures, the frame rate written in the file, and the
  scale written on the stick (its marks are 10 cm apart; on *BallTossOut*, Tracker's own
  calibration, 398.7 px per metre, is the label). No positions, tracks or answers.
- **Ultron must find the law itself** (that the change of speed grows in proportion to
  the time), and g is the constant of that law.
- **Measured error:** Ultron's g is the mean of its per-film values. Its error is the
  larger of (a) the standard error across films and (b) the combined error of each film
  (its own fit, the scale it read, and 0.2% for the frame rate: NTSC cameras run at 29.97,
  not 30). Errors that one film cannot show, such as perspective (the ball and the stick
  at different distances from the camera), show up as disagreement between films, which
  (a) counts.
- **Pass:** |g − 9.80 m/s²| ≤ 2 × the measured error, **and** the measured error is at
  most 3% of g (so a vague answer can't pass), **and** at least 2 of the 3 films give an
  answer (a film where it cannot follow the ball is reported, not dropped).

### How V4 and V6 are judged (written 2026-10-11, before Ultron measures them)

The exit tests are unchanged. These details are fixed now:

**V4, pendulum periods.**
- **The films** are the two real pendulum films in the same source: *pendulum_drag* (a
  small bob on a string; the lab's model gives the length as 0.785 m) and *Pendulum*
  (Flashmedia 1997; "length: 1 m" is printed on the film; it shows about one swing).
- **Ultron is given** the pictures, the frame rate and the length written by the lab.
- **Ultron measures** each period from its own track of the bob, with an error from the
  scatter of its own timings (or, with a single swing, the timing resolution: one picture
  at each end).
- **Pass, per film:** |T − T_ref| ≤ 2 × the measured error, with T_ref = 2π√(L/g)·(1 + θ₀²/16),
  g = 9.80 m/s² and θ₀ the swing's angle as Ultron measures it. The error must be at most 3%.
- **The √length law** needs at least three lengths. With two it is reported, not claimed,
  and V4 stays open until a third real length is found.

**V6, detection on par with a lab tool.**
- **The lab tool** is the positions the lab itself marked by hand in Tracker. Those exist
  on *BallTossOut* (11 points) and *Pendulum* (21 points).
- **Pass, on every such film:**
  - Ultron finds the object in at least 90% of the pictures the lab marked;
  - the median distance between its positions and the lab's is at most the object's
    radius;
  - its positions scatter about a smooth path (a parabola for the ball; a sine for the
    pendulum) at most 1.5 times as much as the lab's own marks do.
- **Disclosed:** on BallTossOut, Ultron's distances to 6 of the lab's points (1.3–3.6 px)
  were seen while V3 was being built, before this rule was written.

**V5, restitution.** The only real bouncing footage in the source is a cart rolling down a
slope against a spring bumper, not a bouncing ball. V5 will be fixed here before it is
measured. A film of a bouncing ball beside a scale is the better test, and it is being
looked for.

### WP3: more real footage (V3–V6)

**Status (2026-10-11):** the network now reaches Wikimedia, archive.org and YouTube.
Wikimedia rate-limits original files from here, but its transcoded copies download. The
footage used so far is GitHub-hosted (preference 1). The Wikimedia pendulum films checked
(a pendulum wave outdoors, a 60 cm pendulum in an edited teaching video) are not usable
footage.

Real videos of falling, swinging and bouncing. The network policy decides the sources:
Wikimedia, YouTube and archive.org are blocked here. The order of preference:
1. footage hosted on GitHub or PyPI;
2. the environment's network settings opened for those sites (owner's choice);
3. failing both, footage the owner provides.

Each video is measured with Ultron's own eyes and compared with a lab tool (for
example, a standard blob tracker) on the same frames.

## Order

WP1 first: the roadmap says *eyes first*. Then WP2, then WP3.
