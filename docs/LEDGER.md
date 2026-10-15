# The ledger of hand-built mechanisms

Rule 6 ([MASTER_PLAN.md](MASTER_PLAN.md) §4): every age records each new hand-written
mechanism of Ultron's **mind** that it needed, and why. As Ultron grows up and learns to
learn, this list should get shorter from one age to the next. If it doesn't, we say so.

Kept separately, and not counted against the mind:
- **the innate endowment,** which is fixed and listed in [AGE_0_1_PLAN.md](AGE_0_1_PLAN.md);
- **the world and the people in it,** which are environment.

## Age 0 (newborn)

| Work package | New hand-built mechanisms of the mind | Why |
|---|---|---|
| WP1 | none | The reflexes (`brain/reflexes.py`: babbling, orienting, grasping) are on the innate list |
| WP2 | none | The caregiver is environment, not mind |
| WP3 | **4, proposed as innate** (waiting for the owner): a blurry wide view, saccadic suppression, inhibition of return, crying | Each is something human newborns have, but none was on the innate list. Without the wide view, nothing outside the sharp middle could catch its eye. Without suppression, every eye movement looked like a change everywhere. Without inhibition of return, it kept coming back to what it had just left. Crying is how a newborn calls for comfort |
| WP3 | otherwise none | Habituation, curiosity, comfort, episodic memory and sleep are on the innate list. The newborn sees "the lump nearest the middle" by the retina's centre-surround, which is the listed "things are bounded lumps" |

**Environment built so far** (not counted):
- the nursery room and its physics (`nursery/world.py`);
- the body and senses (`nursery/body.py`);
- the caregiver's script (`nursery/caregiver.py`);
- days and nights (`nursery/life.py`).

**How the newborn's settings were chosen** (WP3):
- The habituation constants are as first written (look 30 steps for interest to fall to
  1/e, half as interesting after 50 fixations, look away below one half). They were not
  tuned.
- The wide view's thresholds were adjusted on development seeds 11–15 while building it:
  the noise of a coarse pixel, how big a change catches its eye, and how much a patch must
  stand out.
- The milestone exams use seeds 8001 and up, which no learning or building has used.

**Count for Age 0 so far: 4 proposed innate additions (waiting for the owner), 0 other
hand-built mechanisms.**
