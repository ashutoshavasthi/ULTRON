# The ledger of hand-built mechanisms

Rule 6 ([MASTER_PLAN.md](MASTER_PLAN.md) §4): every level records each new hand-written
mechanism of Ultron's **mind** that it needed, and why. As Ultron climbs and learns to
learn, this list should get shorter from one level to the next. If it doesn't, we say so.

Kept separately, and not counted against the mind:
- **the starting kit,** which is fixed and listed in [LEVEL_0_PLAN.md](LEVEL_0_PLAN.md);
- **the worlds and the agents in them,** which are environment.

## Level 0 (foundations)

| Work package | New hand-built mechanisms of the mind | Why |
|---|---|---|
| WP1 | none | The reflexes (`brain/reflexes.py`: babbling, orienting, grasping) are in the starting kit |
| WP2 | none | The teacher is environment, not mind |
| WP3 | **3, proposed for the starting kit** (waiting for the owner): a blurry wide view, saccadic suppression, inhibition of return | None was in the kit. Without the wide view, nothing outside the sharp middle could catch its eye. Without suppression, every eye movement looked like a change everywhere. Without inhibition of return, it kept coming back to what it had just left |
| WP3 | otherwise none | Attention, curiosity, episodic memory and sleep are in the kit. The explorer sees "the lump nearest the middle" by the retina's centre-surround, which is the kit's "things are bounded lumps" |

A fourth proposal (crying, with a comfort drive) was made on 2026-10-15 and withdrawn on
2026-10-18, when the child-imitation parts were removed.

**Environment built so far** (not counted):
- the room and its physics (`room/world.py`);
- the body and senses (`room/body.py`);
- the teacher's script (`room/teacher.py`);
- days and nights (`room/life.py`).

**How the explorer's settings were chosen** (WP3):
- The attention constants are as first written (look 30 steps for interest to fall to
  1/e, half as interesting after 50 fixations, look away below one half). They were not
  tuned.
- The wide view's thresholds were adjusted on development seeds 11–15 while building it:
  the noise of a coarse pixel, how big a change catches its eye, and how much a patch must
  stand out.
- The Level 0 exams use seeds 8001 and up, which no learning or building has used.

**Count for Level 0 so far: 3 proposed starting-kit additions (waiting for the owner), 0
other hand-built mechanisms.**
