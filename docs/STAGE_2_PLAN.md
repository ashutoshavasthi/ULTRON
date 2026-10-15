# Stage 2: the real world through its eyes

> **No longer the main line (2026-10-15).** The plan was rebuilt around growing up
> from a newborn ([MASTER_PLAN.md](MASTER_PLAN.md), [ROADMAP.md](ROADMAP.md)). This plan is
> kept as a record and its results are banked: the eyes (V1) are re-hosted in the nursery at Age 0 (N2), and the real-footage criteria (V2–V6) belong to Age 5 (adolescent). See
> [DEVELOPMENT_MAP.md](DEVELOPMENT_MAP.md).

**Mission.** Ultron has seen one real film, and its eyes don't generalise. Stage 2 gives
it eyes that hold up in hard conditions, then has it rediscover physics from **real
footage**.

## Exit test (fixed now, from `MASTER_PLAN.md`)

| # | Criterion |
|---|---|
| V1 | ✅ **met, and robust** (2026-10-12): every gating eyes row ≥ 23/25 in the failure lab and on 8 fixed sets of 25 unseen trays (normal, 16% noise, big, faint 200/200; 32% noise 199/200; touching 195/200, every set 23–25), and on 8 fresh sets (touching 197/200). Before Stage 2: 25, 1, 0, 0, 2, 19. No regressions elsewhere in the lab; 34 lessons pass on the first attempt; a retrain is byte-identical |
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
| V1 | ✅ **met** (2026-10-11): every gating eyes row 24–25/25 in the failure lab (was 25, 1, 0, 0, 2, 19); on a second set of unseen trays 24–25/25. No regressions elsewhere in the lab; all 28 lessons pass on the first attempt; a retrain is byte-identical; 109 tests pass |
| V2 | ✅ **met** (2026-10-11): lesson 26 is in the curriculum and passes on the first attempt. From the real trackpy microscope film: Einstein's law (spread² ∝ time); D = 0.396 µm²/s against the scientists' tool trackpy's 0.412 (4%) and the textbook's 0.455 (13%); on 150 frames it never learned from it finds 87% of trackpy's spheres and predicts the spread at 1–2 s (21/21); it claims no law for a single sphere |
| V3 | ✅ **met** (2026-10-11): lesson 29. From three real lab films (Tracker project, on GitHub) Ultron finds the law of falling itself (change of speed ∝ time) and measures **g = 9.65 ± 0.15 m/s²** (9.80 at the lab: 1.0 errors off; error 1.6%). Films: 9.95 ± 0.10, 9.56 ± 0.18, 9.45 ± 0.06; they disagree more than their fits admit, so the spread across films is the error. 30 lessons pass on the first attempt; a retrain is byte-identical; every exam, failure-lab row and blind test unchanged (60/60, 60/60, 50/50); 115 tests pass. Report: [`stage2_v3_falling.md`](../reports/stage2_v3_falling.md) |
| V3 recheck | after the V6 changes to how it looks: g = 9.75 ± 0.16 (films 10.06, 9.67, 9.53), still met |
| V4 | ❌ **not met** (2026-10-11, three lengths): per film, Pendelgesetz 0.5 m 1.445 ± 0.016 s against 1.437 (passes); pendulum_drag 0.785 m 1.782 ± 0.014 against 1.818 (−2.5 errors, fails; the lab's Tracker step implies 29.4 pictures/s, noticed after measuring and not used); Pendulum 1 m 2.060 ± 0.094 against 2.060 (agrees, but one swing gives 4.6%, over 3%). **√length law met** (lesson 30): Ultron finds L/T² constant itself; power 0.470 ± 0.029 (−1.05 errors), constant 2.023 ± 0.013 against 2.007 (+1.27 errors). Report: [`stage2_v4_v6.md`](../reports/stage2_v4_v6.md) |
| V5 | ❌ **not met** (2026-10-11): GB Drop passes, e = 0.843 ± 0.003 against the lab's 0.836 ± 0.006 over all four bounces (+1.05 errors); in the corridor film Ultron follows the ball through only one of four bounces (two needed). Report: [`stage2_v4_v6.md`](../reports/stage2_v4_v6.md) |
| V6 | ✅ **met** (2026-10-11): against the lab's Tracker hand marks, BallTossOut 10/11 found, median 2.9 px (radius 4.4), scatter 0.34 vs the lab's 0.39; Pendulum 21/21, 0.8 px (radius 5.5), 1.12 vs 1.09; unchanged with the eyes changed for V4/V5 (0.7 px, 1.06). Report: [`stage2_v4_v6.md`](../reports/stage2_v4_v6.md) |

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
- **Broader handling:** lesson 19 handles things in varied spacing, size, light and
  camera noise. Touching: 19 → 24.
- **Explaining away** (2026-10-11): two things just touching (centres 3.0–3.2 px apart)
  make one ridge in the eyes' map, and the dimmer one was never counted; every touching
  error was that undercount, and the tray sets that scored lowest simply had more such
  pairs. From touch the eyes now learn one thing's footprint in their map; close up, what
  each thing seen accounts for is taken away, and a leftover beside a thing that is
  clearly stronger than any leftover its hands said was nothing is a thing too. On 8
  fixed sets of 25 touching trays: 162 → 193 right, every set 23–25 (was 17–23);
  overlapping (ungated) 64 → 85 of 100; every other eyes row 100/100 before and after.
- **The same trays for every pair of eyes:** the failure lab drew trays and camera
  pictures from one generator, so eyes that looked a different number of times were
  shown different trays. Trays and camera now have their own generators.
- **Measured and not kept:** a sharper spot (σ 0.7) with handling from touching to apart
  and looking longer at crowded scenes (4 pictures) reached touching 189/200 (worst set
  22), 32% noise 96/100 (worst 23) and overlapping 62/100 on the same fixed trays;
  combined with explaining away, 195/200 touching but 32% noise 94/100 (worst 22). 16
  filters with explaining away: touching 187/200 (worst 20).
- **Combined with the later lessons (2026-10-12).** The σ 1.0 eyes above, on their own
  trays, were not the eyes Stage 2's real films (lessons 29–30) and Stage 3's tables were
  built and measured with (σ 0.7, the trays from touching to apart). With them, the 0.5 m
  pendulum was timed 8.5% loose (two things stitched into one swing), BallTossOut lost
  one of its 10/11 marks, and L1's ≤ 20 sentences flipped on a 0.1-bit tie: 32 of 34
  lessons. So explaining away now sits on the σ 0.7 eyes (their learned weights are
  byte-for-byte the ones lessons 20–33 were measured with), close up and when a crowd is
  looked at longer; and a noisy still scene is looked at until it is a little cleaner
  than usual (0.8 of its noise reference), which removes the 32% noise dip above. On the
  failure lab's protocol, 8 fixed sets of 25 (seeds 13, 99, 7, 2024, 1–4): normal, 16%
  noise, big, faint 200/200; 32% noise 199/200; touching 195/200, every set 23–25;
  overlapping (ungated) 121/200. On 8 fresh sets never used before (seeds 5001–5008),
  against the σ 1.0 eyes: 32% noise 199 vs 198, faint 200 vs 199, touching **197 vs
  192**, other gated rows 200 both; overlapping (ungated) 131 vs 170 (the one row that
  is lower). All 34 lessons pass on the first attempt; the exams of lessons 21–33 are
  identical to the PRs that built them.

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

**V5, restitution** (written 2026-10-11, before anything bouncing was measured).
- **The films** must show a ball bouncing on a hard floor, with a scale in view and at
  least two bounces wholly in view. The only bouncing footage found so far (a cart
  against a spring bumper on a slope, Tracker project) has no reference to judge
  against: the lab's file holds a model, not marks or a measured restitution. It is not
  used for V5.
- **Ultron measures** the coefficient of restitution e as the upward speed just after
  each bounce over the downward speed just before it, from its own track, with an error
  from the scatter over bounces (or, with one bounce, from its own fits).
- **The reference** is the lab's own analysis of the same film where one exists (its
  hand marks fitted the same way). Where none exists, e from the heights of successive
  bounces (e² = next height / this height, Ultron's own track) is reported as a check,
  and V5 is not claimed on that film.
- **Pass:** on every film with a lab reference, |e − e_lab| ≤ 2 × the combined error,
  and Ultron's error at most 5% of e.

**Frame rate for new films** (written 2026-10-11, before any new film is measured). Ultron
uses the rate written in the video file. Before Ultron measures a new film, the Judge reads
every independent record of its timing: the lab's own analysis (Tracker's time step), a
clock or stopwatch in view, or the maker's description. If one of them disagrees with the
file by more than 0.5%, the Judge decides which rate counts and writes it down with the
reason, still before measuring, and the verdict uses that rate. A rate found only after
measuring is reported and never used: this is why pendulum_drag's 29.4 pictures/s does not
count.

**V5, the films and the details** (written 2026-10-11, after reading the films' records
and before Ultron or the Judge measured anything on them).
- **The films:** both real bouncing-ball films with the lab's own hand marks that were
  found, from the Singapore Ministry of Education's Open Source Physics collection
  (iwant2study.org, Tracker experiments by Loo Kang Wee and colleagues, CC BY-SA 4.0):
  - *GB Drop*: a ball dropped beside a metre rule and bouncing four times; 1920×1080
    at 30 pictures/s; 104 pictures marked by hand.
  - *ballbouncelookang01*: a ball dropped in a corridor and bouncing four times;
    720×576 at 25 pictures/s, progressive; 70 pictures marked by hand.
- **Frame rate check:** the file and the lab's Tracker step agree on both (30/s and
  33.33 ms; 25/s and 40 ms). In any case e is a ratio of two speeds, so neither the rate
  nor the scale affects it.
- **How e is measured, for Ultron and for the lab's marks alike:** a bounce is where the
  ball is lowest between two flights. Each flight's height is fitted with a parabola in
  time, leaving out the picture nearest each bounce (the ball is touching the floor).
  The bounce happens where the two flights' parabolas meet, and e is the upward speed of
  the later flight there over the downward speed of the earlier one. A bounce counts
  only if both of its flights keep at least 5 pictures. A film's e is the mean over its
  bounces, with the standard error of that mean as its error. Bounces the lab marked
  but Ultron didn't see are reported as missed.
- **Pass, per film:** Ultron measures at least 2 of the bounces,
  |e − e_lab| ≤ 2·√(error² + error_lab²) over the same bounces, and Ultron's error is at
  most 5% of e. V5 is met when both films pass.

**V4, a third length** (written 2026-10-11, before Ultron measured anything on this film).
- **The film:** *Pendelgesetz (mit Rechnung)* by Rhetos (Mathe-AC Lernwerkstatt Aachen,
  Wikimedia Commons, CC BY-SA 4.0), Wikimedia's 720p copy, 25 pictures/s. "0,5 m" is
  written beside the pendulum and in the film's description; the pendulum swings ten
  times.
- **What Ultron is shown:** this is a teaching film, so the Trainer shows only the
  experiment: the 17 seconds from 118 s, in which the pendulum swings, and the part of
  the picture around it (x 330–650, y 0–440). That leaves out the text and the timer the
  film's editor laid over it, the lesson on the board and the stopwatch. Ultron is given
  the frame rate and the length, as for the other films.
- **Frame rate check:** the film's own timer, laid over it in editing, runs one second
  per 25 pictures. Nothing disagrees with the file's 25/s. (The timer stops at 14.20 s
  for the ten swings; that is the film's own answer, and Ultron is not shown it.)
- **Judged** by the same V4 rule. With three lengths (0.5, 0.785 and 1 m), the
  √length law is judged too. Ultron must find it itself: across the films, the period
  grows as the square root of the length (power 0.5 ± 2 errors), and its constant must
  agree with 2π/√g within 2 errors.
- **How the law is judged** (written 2026-10-11, while Ultron's first measurement of the
  0.5 m film was running and before its result was seen):
  - Ultron is given each film's period as it measured it, with the length, in a lesson of
    its own (lesson 30), and must find the law by itself: the period squared over the
    length stays the same (or the same law upside down). Its law must be that one.
  - The power: the Judge fits log T against log L over the films, each weighted by
    Ultron's own error. The power's error is the fit's error from Ultron's errors, or from
    the scatter about the line if that is larger. Pass: 0.5 within 2 errors.
  - The constant: each film gives T/√L, with Ultron's error over √L. The constant is
    their weighted mean, with the error from Ultron's errors or from the scatter between
    films if that is larger. Pass: within 2 errors of 2π/√9.80 = 2.007 s/√m, and that error
    at most 3%. No allowance for the swing's angle is made here: the per-film rule
    already has one.

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
