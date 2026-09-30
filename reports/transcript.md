# Training transcript

Everything Ultron and the Trainer said, in order (individual play choices omitted; see `brain/ultron_brain.json`).


## Lesson 0

- **Trainer**: Lesson 0: Hidden things
- Ultron _meet_: new kind of experience: peekaboo
- Ultron _revise_: peekaboo: surprised; new best explanation is went_in (was nothing; 1 experiences, 2 programs searched)
- Ultron _confirm_: peekaboo: went_in predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 0, attempt 1: passed
- **Trainer**: What you found in 'peekaboo' is what people call object permanence.

## Lesson 1

- **Trainer**: Lesson 1: Same number
- Ultron _meet_: new kind of experience: pair_off
- Ultron _revise_: pair_off: surprised; new best explanation is false (was nothing; 1 experiences, 6 programs searched)
- Ultron _revise_: pair_off: surprised; new best explanation is eq(nA, nB) (was false; 2 experiences, 27 programs searched)
- Ultron _confirm_: pair_off: eq(nA, nB) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 1, attempt 1: passed
- **Trainer**: What you found in 'pair_off' is what people call same number (one-to-one correspondence).

## Lesson 2

- **Trainer**: Lesson 2: Putting together and taking away
- Ultron _meet_: new kind of experience: merge
- Ultron _meet_: new kind of experience: take_away
- Ultron _meet_: new kind of experience: lamps
- Ultron _revise_: merge: surprised; new best explanation is nA (was nothing; 1 experiences, 1 programs searched)
- Ultron _revise_: take_away: surprised; new best explanation is nA (was nothing; 1 experiences, 1 programs searched)
- Ultron _revise_: lamps: surprised; new best explanation is succ(succ(lit_before)) (was nothing; 1 experiences, 10 programs searched)
- Ultron _revise_: merge: surprised; new best explanation is repeat nA times [succ] starting from nB (was nA; 2 experiences, 150 programs searched)
- Ultron _stuck_: lamps: no simple law explains all 2 experiences (searched 587 programs)
- Ultron _revise_: take_away: surprised; new best explanation is repeat n_taken times [pred] starting from nA (was nA; 3 experiences, 152 programs searched)
- Ultron _stuck_: lamps: no simple law explains all 4 experiences (searched 587 programs)
- Ultron _stuck_: lamps: no simple law explains all 8 experiences (searched 587 programs)
- Ultron _confirm_: merge: repeat nA times [succ] starting from nB predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: take_away: repeat n_taken times [pred] starting from nA predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _stuck_: lamps: no simple law explains all 16 experiences (searched 1831 programs)
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 2, attempt 1: passed
- **Trainer**: What you found in 'merge' is what people call addition.
- **Trainer**: What you found in 'take_away' is what people call subtraction.

## Lesson 3

- **Trainer**: Lesson 3: Groups of groups
- Ultron _meet_: new kind of experience: groups
- Ultron _revise_: groups: surprised; new best explanation is size (was nothing; 1 experiences, 2 programs searched)
- Ultron _revise_: groups: surprised; new best explanation is succ(succ(succ(1))) (was size; 2 experiences, 95 programs searched)
- Ultron _revise_: groups: surprised; new best explanation is repeat size times [merge(·, groups)] starting from 0 (was succ(succ(succ(1))); 3 experiences, 850 programs searched)
- Ultron _confirm_: groups: repeat size times [merge(·, groups)] starting from 0 predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 3, attempt 1: passed
- **Trainer**: What you found in 'groups' is what people call multiplication.

## Lesson 4

- **Trainer**: Lesson 4: Names for things
- Ultron _meet_: new kind of experience: numeral
- **Trainer**: I pointed at piles and said their names: marks 0-9 and words zero-ten.
- Ultron _word_: 'plus' behaves exactly like my law 'merge' (arguments xy) in all 6 demonstrations
- Ultron _word_: '+' behaves exactly like my law 'merge' (arguments xy) in all 6 demonstrations
- Ultron _word_: 'minus' behaves exactly like my law 'take_away' (arguments xy) in all 6 demonstrations
- Ultron _word_: '-' behaves exactly like my law 'take_away' (arguments xy) in all 6 demonstrations
- Ultron _word_: 'times' behaves exactly like my law 'groups' (arguments xy) in all 6 demonstrations
- Ultron _word_: '×' behaves exactly like my law 'groups' (arguments xy) in all 6 demonstrations
- Ultron _word_: '*' behaves exactly like my law 'groups' (arguments xy) in all 6 demonstrations
- Ultron _word_: 'equals' joins things that are the same amount
- Ultron _word_: '=' joins things that are the same amount
- **Trainer**: I acted out 'plus', 'minus', 'times' with real piles and said the words.
- Ultron _revise_: numeral: surprised; new best explanation is succ(succ(groups(8, 9))) (was nothing; 1 experiences, 1115 programs searched)
- Ultron _revise_: numeral: surprised; new best explanation is merge(right, groups(left, 10)) (was succ(succ(groups(8, 9))); 2 experiences, 2789 programs searched)
- Ultron _confirm_: numeral: merge(right, groups(left, 10)) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: I wrote two-mark numerals next to piles of 10-99 things.
- **Trainer**: Exam for lesson 4, attempt 1: passed
- **Trainer**: What you found in 'numeral' is what people call place value.

## Lesson 5

- **Trainer**: Lesson 5: Pushing, stretching, colliding
- Ultron _meet_: new kind of experience: push
- Ultron _meet_: new kind of experience: stretch
- Ultron _meet_: new kind of experience: collide
- Ultron _stuck_: push: nothing stays constant yet (1 experiences)
- Ultron _stuck_: stretch: nothing stays constant yet (1 experiences)
- Ultron _revise_: collide: total m·v is the same before and after in every collision (1 experiences)
- Ultron _revise_: push: F / (a·m) = 1 [dimensionless] in every experiment (22 candidates searched)
- Ultron _stuck_: stretch: nothing stays constant yet (2 experiences)
- Ultron _stuck_: stretch: nothing stays constant yet (3 experiences)
- Ultron _stuck_: stretch: nothing stays constant yet (4 experiences)
- Ultron _stuck_: stretch: nothing stays constant yet (5 experiences)
- Ultron _stuck_: stretch: nothing stays constant yet (6 experiences)
- Ultron _revise_: stretch: F / x is constant for each spring but differs between them: a hidden property of each spring [N/m] (20 candidates searched)
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _reflect_: collide: total m·v is the same before and after in every collision; total m·v^2 is the same before and after only in steel collisions (16 experiences)
- **Trainer**: Exam for lesson 5, attempt 1: passed
- **Trainer**: What you found in 'push' is what people call Newton's second law.
- **Trainer**: What you found in 'stretch' is what people call stiffness (Hooke's law).
- **Trainer**: What you found in 'collide' is what people call conservation of momentum.

## Lesson 6

- **Trainer**: Lesson 6: Real measurements
- Ultron _meet_: new kind of experience: orbit
- Ultron _meet_: new kind of experience: gas
- Ultron _stuck_: orbit: nothing stays constant yet (1 experiences)
- Ultron _revise_: orbit: T^2 / r^3 = 2.97473e-19 [m^-3·s^2] in every experiment (20 candidates searched)
- **Trainer**: I showed real distances and orbital periods of six planets.
- Ultron _stuck_: gas: nothing stays constant yet (1 experiences)
- Ultron _revise_: gas: P·V = 1401.94 [the data's own units] in every experiment (2 candidates searched)
- **Trainer**: I showed Boyle's 1662 measurements for the larger air volumes.
- **Trainer**: Exam for lesson 6, attempt 1: passed
- **Trainer**: What you found in 'orbit' is what people call Kepler's third law.
- **Trainer**: What you found in 'gas' is what people call Boyle's law.

## Lesson 7

- **Trainer**: Lesson 7: A lab with cheap instruments
- Ultron _meet_: new kind of experience: lab_push
- Ultron _meet_: new kind of experience: lab_stretch
- Ultron _stuck_: lab_push: nothing stays constant yet (1 experiences)
- Ultron _stuck_: lab_stretch: nothing stays constant yet (1 experiences)
- Ultron _revise_: lab_push: F / (a·m) = 0.991157 [dimensionless] in every experiment (7 candidates searched)
- Ultron _stuck_: lab_stretch: nothing stays constant yet (2 experiences)
- Ultron _stuck_: lab_stretch: nothing stays constant yet (3 experiences)
- Ultron _revise_: lab_stretch: F / x is constant for each spring but differs between them: a hidden property of each spring [N/m] (6 candidates searched)
- Ultron _measure_: lab_stretch: met new spring L4; measured its property F / x = 16.6613
- Ultron _measure_: lab_stretch: met new spring L3; measured its property F / x = 68.8365
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 7, attempt 1: passed
- **Trainer**: What you found in 'lab_push' is what people call Newton's second law (measured with noise).
- **Trainer**: What you found in 'lab_stretch' is what people call stiffness (measured with noise).

## Lesson 8

- **Trainer**: Lesson 8: The tough final exam
- **Trainer**: No teaching today. Show me what you can do.
- **Trainer**: Exam for lesson 8, attempt 1: passed
