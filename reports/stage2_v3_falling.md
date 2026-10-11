# Stage 2, V3: g from real footage of falling

*Written by Claude, as Ultron's trainer and judge, 2026-10-11.*

## Verdict

**V3 is met.** From three real lab films, Ultron finds the law of falling itself (the
change of speed grows in proportion to the time) and measures

**g = 9.65 ± 0.15 m/s²**, against 9.80 m/s² at the lab (Aptos, California).

The gap is 0.15 m/s², which is 1.0 of its measured errors (the pass line is 2). The
error is 1.6% of g (the limit is 3%). All three films were measured. The rule was
written into `docs/STAGE_2_PLAN.md` and committed (ee26f22) before Ultron measured
anything.

| Film | How it was filmed | Pictures with nothing touching the ball | g (m/s²) | its own fit's error |
|---|---|---|---|---|
| BallTossOut | 30 frames/s, tossed across | 16 | 9.945 | ± 0.103 |
| BallDrop | interlaced, 60 half-pictures/s, dropped | 22 | 9.557 | ± 0.179 |
| BallTossUp | interlaced, 60 half-pictures/s, tossed up | 47 | 9.448 | ± 0.060 |
| **Mean** | | | **9.650** | **± 0.151** (spread across films; combined per-film error 0.075) |

Judged film by film against its own error, 2 of the 3 films fall within 2 errors of 9.80.
BallTossUp does not (9.45 ± 0.07). This is reported only, as the plan says, because a single
film can't show errors that depend on how it was filmed. The disagreement between films is
larger than any one fit admits. That is why the plan uses the spread across films as the
measured error, and the spread is what decides the verdict.

The law's constant over all 46 of Ultron's experiences is 9.58 m/s² (a robust fit across
every lag of every film). The mean of the three films is 9.65.

## The footage

The films come from the Tracker project (Douglas Brown and colleagues, Open Source Physics,
GPL-3.0), which is the standard tool for physics video analysis in schools. They are hosted on
GitHub (`OpenSourcePhysics/resources` at 3b07d46 and `OpenSourcePhysics/tracker-website` at
77737aa), which is first in WP3's order of preference. All three were filmed in the same
Cabrillo College lab with the same metre stick in view. `ultron/env/footage.py` fetches each
archive from its pinned commit and checks its SHA-256. It also checks the SHA-256 of the
decoded pixels. Only the brightness (Y) plane is used, and it is copied exactly, so ffmpeg 6.1
and 7.0 give identical bytes; both were checked. Nothing from the films is committed, only the
manifest.

Ultron was given the pictures, the frame rate written in the file, whether the video is
interlaced, and the stick's scale. It was given no positions, no tracks and no answers.
- **BallTossOut:** the lab's own Tracker calibration, 398.7 px per metre.
- **BallDrop and BallTossUp:** the Trainer read the stick's 10 cm marks, giving 400.7 and
  400.3 px per metre (`ultron/judge/footage_reference.py`).

The marks give 400.0 on BallTossOut. That agrees with Tracker's tape measure to 0.3%, which
confirms that the marks are 10 cm apart. That 0.3% is the scale error the verdict uses.

Two films were left out before measuring:
- **FreeFall** (a kitchen film), because nothing in it gives a readable scale;
- **TossOutStrobe and WhichLandsFirst**, because they are composites made for teaching.

## How Ultron sees and measures (lesson 29)

Its eyes grew up on simulator pictures. Run straight on these films, they found hundreds of
"things" per picture: compression speckle, the arm, the stick. Two general rules
(`ultron/senses/motion.py`) fixed this without touching the eyes or the retina:

1. **What changes stands out.** Each picture is compared with how the room usually looks
   (the median picture). Only the difference is looked at, with the film's strongest changes
   at the contrast its eyes are used to. Each picture is also looked at from further back,
   because the ball is larger than the things the eyes learned.
2. **Things keep moving as they were moving.** Following predicts where each thing is
   heading. The ball is the lasting track that travels furthest. For interlaced films, each
   half-picture is a picture of its own, and the order of the two halves is the one in which
   the ball moves more smoothly.

It measures only the pictures in which the ball is **on its own and wholly in view**: no
other moving thing within 40 px (so not while the hand holds or releases it) and not at the
picture's edge. One measured pitfall was fixed: on BallTossUp, a last sighting cut off by the
bottom edge pulled one speed reading 20% low.

For each film and each lag τ, it averages how much faster the ball is going after τ (dv) and
gives (τ, dv) to its law-finder. Its precision comes from comparing the films at the same
τ = 1/6 s, before any law is known (1.0%). The law-finder settled on **dv / τ = constant**
after doubting it twice, when BallDrop's lower values arrived. Only after that law was found
did it measure each film's rate, from the line through all its speeds.

These rules were checked on things other than g:
- where the ball is, against the lab's hand marks in Tracker on BallTossOut;
- whether the right pictures were kept (the ball free of the hand, in view).

They were not tuned to bring g closer to 9.80.

## Honest notes

- **The films disagree by more than their fits admit** (9.95, 9.56, 9.45). The two
  interlaced films are lower. A light ball slowed by air would read low when dropped, and a
  ball nearer to or further from the camera than the stick changes the scale. One camera
  can't tell these apart, which is why the spread across films is the error.
- **BallTossOut agrees with the lab's own tool.** Tracker's hand-marked positions fitted the
  same way give 10.06 m/s² at 30 frames/s. Ultron gives 9.95, a 1% difference. Ultron's
  positions sit 1.3 to 3.6 px from the lab's marks (6 points). The V6 test has not been
  fixed yet; these distances were seen before it is written and will be declared then.
- **Interlaced films show a half-picture effect.** On BallDrop, starting from even
  half-pictures gives 10.6 and from odd ones 8.4, while the line through all speeds is
  unaffected. The two half-pictures of a frame are not perfectly aligned. This is recorded
  and not hidden.
- **Determinism.** A retrain on this machine is byte-identical. Lessons 0 to 28 learn
  exactly what they learned before lesson 29 existed: the only differences in the brain file
  are additions under `fall`. The committed brain file differs from a retrain on this
  machine in the last digit of 139 floating-point numbers. That difference was there before
  this change, from a different numpy or BLAS, and it is recorded as a cross-machine limit.
- **Decoding needs ffmpeg** (or `pip install imageio-ffmpeg`). Without it, or without
  network on a first run, lesson 29 says so and fails, as lesson 26 does without network.

## What V3 does not show

It does not show g measured to better than 1.6%, or from footage outside one lab. It also
doesn't separate air drag from perspective. More films from other places would shrink the
error and test the law further.
