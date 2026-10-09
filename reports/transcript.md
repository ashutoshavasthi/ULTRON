# Training transcript

Everything Ultron and the Trainer said, in order (individual play choices omitted; see `brain/ultron_brain.json`).


## Lesson 0

- **Trainer**: Lesson 0: Hidden things
- Ultron _meet_: new kind of experience: peekaboo
- Ultron _revise_: peekaboo: surprised; new best explanation is hidden (was nothing; 1 experiences, 8 programs searched)
- Ultron _confirm_: peekaboo: hidden predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 0, attempt 1: passed
- **Trainer**: What you found in 'peekaboo' is what people call object permanence.

## Lesson 1

- **Trainer**: Lesson 1: Same number
- Ultron _meet_: new kind of experience: pair_off
- Ultron _revise_: pair_off: surprised; new best explanation is true (was nothing; 1 experiences, 12 programs searched)
- Ultron _revise_: pair_off: surprised; new best explanation is eq(nA, nB) (was true; 2 experiences, 55 programs searched)
- Ultron _confirm_: pair_off: eq(nA, nB) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 1, attempt 1: passed
- **Trainer**: What you found in 'pair_off' is what people call same number (one-to-one correspondence).

## Lesson 2

- **Trainer**: Lesson 2: Putting together and taking away
- Ultron _meet_: new kind of experience: merge
- Ultron _meet_: new kind of experience: take_away
- Ultron _meet_: new kind of experience: lamps
- Ultron _revise_: merge: surprised; new best explanation is nA (was nothing; 1 experiences, 6 programs searched)
- Ultron _revise_: take_away: surprised; new best explanation is nA (was nothing; 1 experiences, 6 programs searched)
- Ultron _revise_: lamps: surprised; new best explanation is 1 (was nothing; 1 experiences, 7 programs searched)
- Ultron _revise_: merge: surprised; new best explanation is repeat nA times [succ] starting from nB (was nA; 2 experiences, 526 programs searched)
- Ultron _revise_: take_away: surprised; new best explanation is pred(n_taken) (was nA; 2 experiences, 70 programs searched)
- Ultron _stuck_: lamps: no simple law explains all 2 experiences (searched 793 programs)
- Ultron _revise_: take_away: surprised; new best explanation is repeat n_taken times [pred] starting from nA (was pred(n_taken); 3 experiences, 629 programs searched)
- Ultron _stuck_: lamps: no simple law explains all 4 experiences (searched 1610 programs)
- Ultron _stuck_: lamps: no simple law explains all 8 experiences (searched 1636 programs)
- Ultron _confirm_: merge: repeat nA times [succ] starting from nB predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: take_away: repeat n_taken times [pred] starting from nA predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _stuck_: lamps: no simple law explains all 16 experiences (searched 3594 programs)
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _reflect_: 'merge' gives the same answer either way round, so I can count along the smaller number
- **Trainer**: Exam for lesson 2, attempt 1: passed
- **Trainer**: What you found in 'merge' is what people call addition.
- **Trainer**: What you found in 'take_away' is what people call subtraction.

## Lesson 3

- **Trainer**: Lesson 3: Groups of groups
- Ultron _meet_: new kind of experience: groups
- Ultron _revise_: groups: surprised; new best explanation is groups (was nothing; 1 experiences, 10 programs searched)
- Ultron _revise_: groups: surprised; new best explanation is repeat groups times [merge(·, groups)] starting from 0 (was groups; 2 experiences, 1195 programs searched)
- Ultron _revise_: groups: surprised; my other idea repeat size times [merge(·, groups)] starting from 0 fits everything (was repeat groups times [merge(·, groups)] starting from 0)
- Ultron _confirm_: groups: repeat size times [merge(·, groups)] starting from 0 predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _reflect_: 'groups' gives the same answer either way round, so I can count along the smaller number
- Ultron _reflect_: 'groups' is 'merge' repeated: groups(groups, size) = repeat size times [merge(·, groups)] starting from 0, which is 'merge''s nothing (merge(0, x) = x)
- Ultron _invent_: 'groups' is 'merge' repeated (I have seen this shape 1 time). If REPEAT is a general way of making laws, then applied to 'groups' it predicts a law I have never met: repeated_groups(amount, times) = repeat times times [groups(·, amount)] starting from 1. That is only a guess from a pattern, so I'll keep it as a prediction until the world agrees.
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
- Ultron _revise_: numeral: surprised; new best explanation is succ(succ(groups(8, 9))) (was nothing; 1 experiences, 11273 programs searched)
- Ultron _revise_: numeral: surprised; my other idea merge(right, groups(left, 10)) fits everything (was succ(succ(groups(8, 9))))
- Ultron _confirm_: numeral: merge(right, groups(left, 10)) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _invent_: My place-value law hides a shortcut. I checked on 40 examples each: adding two numerals is adding their columns; ten in a column is one in the next (a carry); times spreads over the columns; and a 0 on the end is times ten. So I never need to count a big number out: I can work column by column, where every step is a small sum or product I already know by heart. That is column arithmetic.
- Ultron _reflect_: the column way of 'times' gives the same answer as my law 'groups' on 60 examples; I'll use it for big numbers
- Ultron _reflect_: the column way of 'add' gives the same answer as my law 'merge' on 60 examples; I'll use it for big numbers
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
- Ultron _revise_: collide: total m·v is the same before and after in every collision [tentative: 1 event(s)] (1 experiences)
- Ultron _revise_: push: F / (a·m) = 1 [dimensionless] in every experiment (22 candidates searched; tentative until it predicts 3 new experiences)
- Ultron _stuck_: stretch: nothing stays constant yet (2 experiences)
- Ultron _stuck_: stretch: nothing stays constant yet (3 experiences)
- Ultron _stuck_: stretch: nothing stays constant yet (4 experiences)
- Ultron _stuck_: stretch: nothing stays constant yet (5 experiences)
- Ultron _stuck_: stretch: nothing stays constant yet (6 experiences)
- Ultron _revise_: stretch: F / x is constant for each spring but differs between them: a hidden property of each spring [N/m] (20 candidates searched; tentative until it predicts 3 new experiences)
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
- Ultron _revise_: orbit: T^2 / r^3 = 2.97473e-19 [m^-3·s^2] in every experiment (20 candidates searched; tentative until it predicts 3 new experiences)
- **Trainer**: I showed real distances and orbital periods of six planets.
- Ultron _stuck_: gas: nothing stays constant yet (1 experiences)
- Ultron _revise_: gas: P·V = 1401.94 [the data's own units] in every experiment (2 candidates searched; tentative until it predicts 3 new experiences)
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
- Ultron _revise_: lab_push: F / (a·m) = 0.991157 [dimensionless] in every experiment (7 candidates searched; tentative until it predicts 3 new experiences)
- Ultron _stuck_: lab_stretch: nothing stays constant yet (2 experiences)
- Ultron _stuck_: lab_stretch: nothing stays constant yet (3 experiences)
- Ultron _revise_: lab_stretch: F / x is constant for each spring but differs between them: a hidden property of each spring [N/m] (6 candidates searched; tentative until it predicts 3 new experiences)
- Ultron _measure_: lab_stretch: met new spring L4; measured its property F / x = 16.6613
- Ultron _measure_: lab_stretch: met new spring L3; measured its property F / x = 68.8365
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 7, attempt 1: passed
- **Trainer**: What you found in 'lab_push' is what people call Newton's second law (measured with noise).
- **Trainer**: What you found in 'lab_stretch' is what people call stiffness (measured with noise).

## Lesson 8

- **Trainer**: Lesson 8: Owing
- Ultron _meet_: new kind of experience: earn_coins
- Ultron _meet_: new kind of experience: earn_notes
- Ultron _meet_: new kind of experience: spend_coins
- Ultron _meet_: new kind of experience: spend_notes
- **Trainer**: Here is a purse. You can earn coins and spend coins. If you spend with an empty purse, the shop gives you an IOU note. Play.
- Ultron _revise_: earn_coins: a prediction I had in mind, repeated_groups(coins, notes), fits my first 1 experience(s); only a suspicion, so I'll test it before searching for anything else
- Ultron _revise_: earn_notes: surprised; new best explanation is coins (was nothing; 1 experiences, 15 programs searched)
- Ultron _revise_: spend_coins: surprised; new best explanation is coins (was nothing; 1 experiences, 15 programs searched)
- Ultron _revise_: spend_notes: a prediction I had in mind, repeated_groups(coins, notes), fits my first 1 experience(s); only a suspicion, so I'll test it before searching for anything else
- Ultron _revise_: earn_coins: surprised; new best explanation is succ(coins) (was repeated_groups(coins, notes); 2 experiences, 1049 programs searched)
- Ultron _revise_: earn_notes: surprised; my other idea notes fits everything (was coins)
- Ultron _revise_: spend_coins: surprised; my other idea pred(coins) fits everything (was coins)
- Ultron _revise_: spend_notes: a prediction I had in mind, repeated_groups(notes, coins), fits my first 2 experience(s); only a suspicion, so I'll test it before searching for anything else
- Ultron _revise_: earn_coins: surprised; new best explanation is take_away(succ(coins), notes) (was succ(coins); 3 experiences, 38927 programs searched)
- Ultron _revise_: spend_notes: surprised; new best explanation is take_away(succ(notes), coins) (was repeated_groups(notes, coins); 3 experiences, 38925 programs searched)
- Ultron _revise_: earn_notes: surprised; new best explanation is pred(notes) (was notes; 4 experiences, 1232 programs searched)
- Ultron _confirm_: spend_coins: pred(coins) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: earn_coins: take_away(succ(coins), notes) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: spend_notes: take_away(succ(notes), coins) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: earn_notes: pred(notes) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _invent_: My coins/notes states all lie on ONE line: 'earn' and 'spend' undo each other, and from the empty state 'earn' counts coins up 1, 2, 3... But 'spend' from the empty state doesn't stop: it keeps going, into states with notes. Those are places *below* zero. I'll treat them as numbers too, and use a new step 'down' that has no floor.
- Ultron _reflect_: 'up one' and 'down one' undo each other on my line
- **Trainer**: You say some purses are 'below zero'. Let's buy and sell with that idea.
- Ultron _meet_: new kind of experience: pay
- Ultron _meet_: new kind of experience: get_paid
- Ultron _revise_: pay: surprised; new best explanation is repeat price times [down] starting from purse (was nothing; 1 experiences, 2940 programs searched)
- Ultron _revise_: get_paid: surprised; new best explanation is succ(purse) (was nothing; 1 experiences, 86 programs searched)
- Ultron _revise_: get_paid: surprised; my other idea merge(purse, wage) fits everything (was succ(purse))
- Ultron _confirm_: pay: repeat price times [down] starting from purse predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: get_paid: merge(purse, wage) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _reflect_: 'get_paid' gives the same answer either way round, so I can count along the smaller number
- Ultron _reflect_: imagining with my laws: 'pay' always undoes 'get_paid'
- Ultron _reflect_: imagining with my laws: 'pay' always undoes 'merge'
- Ultron _reflect_: the column way of 'add' gives the same answer as my law 'get_paid' on 60 examples; I'll use it for big numbers
- Ultron _reflect_: the column way of 'take away' gives the same answer as my law 'pay' on 60 examples; I'll use it for big numbers
- Ultron _word_: '-' in front of a number means that far below zero
- Ultron _word_: 'negative' in front of a number means that far below zero
- **Trainer**: People write your below-zero places as -1, -2, -3 and say 'negative one, negative two'.
- Ultron _word_: 'minus' behaves exactly like my law 'pay' (arguments yx) in all 8 demonstrations
- Ultron _word_: '-' behaves exactly like my law 'pay' (arguments yx) in all 8 demonstrations
- Ultron _word_: 'plus' behaves exactly like my law 'get_paid' (arguments xy) in all 8 demonstrations
- Ultron _word_: '+' behaves exactly like my law 'get_paid' (arguments xy) in all 8 demonstrations
- **Trainer**: I bought and sold things with you and said 'minus' and 'plus' out loud.
- **Trainer**: Exam for lesson 8, attempt 1: passed
- **Trainer**: What you found in 'line:earn/spend' is what people call negative numbers (the integers).

## Lesson 9

- **Trainer**: Lesson 9: Sharing cakes
- Ultron _meet_: new kind of experience: cake_balance
- Ultron _meet_: new kind of experience: recut
- **Trainer**: Here are cakes, a knife that cuts into equal pieces, and a balance. Play.
- Ultron _revise_: cake_balance: surprised; new best explanation is true (was nothing; 1 experiences, 51 programs searched)
- Ultron _revise_: recut: a prediction I had in mind, repeated_groups(cut, recut), fits my first 1 experience(s); only a suspicion, so I'll test it before searching for anything else
- Ultron _revise_: cake_balance: surprised; new best explanation is lt(pieces, cut) (was true; 2 experiences, 2300 programs searched)
- Ultron _revise_: recut: a prediction I had in mind, repeated_groups(recut, cut), fits my first 2 experience(s); only a suspicion, so I'll test it before searching for anything else
- Ultron _revise_: recut: surprised; new best explanation is groups(cut, recut) (was repeated_groups(recut, cut); 3 experiences, 2134 programs searched)
- Ultron _revise_: cake_balance: surprised; my other idea eq(pieces, wholes) fits everything (was lt(pieces, cut))
- Ultron _confirm_: recut: groups(cut, recut) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: cake_balance: eq(pieces, wholes) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _revise_: cake_balance: surprised; new best explanation is eq(pieces, groups(cut, wholes)) (was eq(pieces, wholes); 16 experiences, 157078 programs searched)
- Ultron _confirm_: cake_balance: eq(pieces, groups(cut, wholes)) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _reflect_: 'recut' gives the same answer either way round, so I can count along the smaller number
- Ultron _invent_: Walking by single pieces of a cake cut into 2, I pass a whole every 2 steps, and in between I'm at places no whole number reaches: one piece balances no whole number of cakes, yet 2 of them balance exactly 1. So my number line is FINER than I thought: there are numbers *between* my numbers. Every pile of equal pieces is one. And since scaling the count and the kind of piece together with my 'groups' law never changes what balances, two piles are the same number when, cut into the same kind of piece, they have the same count. My whole numbers are piles of pieces 'cut into 1'.
- Ultron _reflect_: the column way of 'times' gives the same answer as my law 'recut' on 60 examples; I'll use it for big numbers
- Ultron _word_: 'a/b' means a pieces of a cake cut into b
- **Trainer**: People write 'so many pieces of a cake cut into so many' like 2/3.
- Ultron _word_: 'divided' asks: what, times the second number, gives the first? (checked on all 6 sharings)
- Ultron _word_: '÷' asks: what, times the second number, gives the first? (checked on all 6 sharings)
- **Trainer**: I shared cakes fairly between people and said 'divided' out loud.
- **Trainer**: Exam for lesson 9, attempt 1: passed
- **Trainer**: What you found in 'finer:cake_balance' is what people call fractions (the rational numbers).

## Lesson 10

- **Trainer**: Lesson 10: The tough final exam
- **Trainer**: No teaching today. Show me what you can do.
- **Trainer**: Exam for lesson 10, attempt 1: passed

## Lesson 11

- **Trainer**: Lesson 11: The wheel
- Ultron _meet_: new kind of experience: tick
- **Trainer**: Here is a wheel with a pointer. You can make it tick. Play.
- Ultron _revise_: tick: surprised; new best explanation is 1 (was nothing; 1 experiences, 21 programs searched)
- Ultron _revise_: tick: surprised; new best explanation is spend_notes(slot, 0) (was 1; 2 experiences, 1838 programs searched)
- Ultron _revise_: tick: surprised; new best explanation is if eq(slot, 5) then 0 else succ(slot) (was spend_notes(slot, 0); 3 experiences, 2042715 programs searched)
- Ultron _confirm_: tick: if eq(slot, 5) then 0 else succ(slot) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _invent_: Repeating 'tick' from the start, slot counts 1, 2, ... 5, and the 6th 'tick' brings me back to the start. So here numbers go round: after 5 comes 0 again. 6 'tick's change nothing, and going back one is the same as going on 5. These are a new kind of number that repeats every 6.
- **Trainer**: Now spin it as many ticks as you like and watch where it stops.
- Ultron _meet_: new kind of experience: spin
- Ultron _revise_: spin: surprised; new best explanation is start (was nothing; 1 experiences, 15 programs searched)
- Ultron _revise_: spin: surprised; new best explanation is take_away(start, 4) (was start; 2 experiences, 2129 programs searched)
- Ultron _revise_: spin: surprised; new best explanation is repeat ticks times [tick] starting from start (was take_away(start, 4); 4 experiences, 114651 programs searched)
- Ultron _confirm_: spin: repeat ticks times [tick] starting from start predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _word_: 'after' behaves exactly like my law 'spin' (arguments yx) in all 6 demonstrations
- **Trainer**: I spun the wheel and said '3 after 5 equals 2' and so on.
- **Trainer**: Exam for lesson 11, attempt 1: passed
- **Trainer**: What you found in 'cycle:tick' is what people call clock numbers (arithmetic modulo 6).

## Lesson 12

- **Trainer**: Lesson 12: Hills and valleys
- Ultron _meet_: new kind of experience: roll
- Ultron _stuck_: roll: nothing stays constant yet (1 experiences)
- Ultron _stuck_: roll: nothing stays constant yet (2 experiences)
- Ultron _stuck_: roll: nothing stays constant yet (3 experiences)
- Ultron _stuck_: roll: nothing stays constant yet (4 experiences)
- Ultron _stuck_: roll: nothing stays constant yet (5 experiences)
- Ultron _stuck_: roll: nothing stays constant yet (6 experiences)
- Ultron _revise_: roll: Along each run, none of y, v^2 stays the same, but y + 0.0509684·v^2 does. Each run has its own amount of this hidden quantity: whatever y is lost turns up as v^2, and the total never changes. (The coefficient of v^2 is one over 19.62 m/s²: the same units as 'a' in my 'lab_push' experiences.)
- Ultron _invent_: Along each run, none of y, v^2 stays the same, but y + 0.0509684·v^2 does. Each run has its own amount of this hidden quantity: whatever y is lost turns up as v^2, and the total never changes. (The coefficient of v^2 is one over 19.62 m/s²: the same units as 'a' in my 'lab_push' experiences.)
- Ultron _measure_: roll: new run R3; its hidden amount is 2.76
- Ultron _measure_: roll: new run R4; its hidden amount is 3.748
- Ultron _measure_: roll: new run R5; its hidden amount is 1.893
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 12, attempt 1: passed
- **Trainer**: What you found in 'hidden:roll' is what people call energy (height + speed²/2g, per unit of weight).
- **Trainer**: What you found in 'roll' is what people call conservation of energy.

## Lesson 13

- **Trainer**: Lesson 13: Growing
- Ultron _meet_: new kind of experience: grow
- Ultron _revise_: grow: a prediction I had in mind, repeated_groups(split, days), fits my first 1 experience(s); only a suspicion, so I'll test it before searching for anything else
- Ultron _confirm_: grow: repeated_groups(split, days) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: my predicted law 'repeated_groups' was right: the world does exactly what REPEAT said it would
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _reflect_: 'repeated_groups' is 'groups' repeated: repeated_groups(amount, times) = repeat times times [groups(·, amount)] starting from 1, which is 'groups''s nothing (groups(1, x) = x)
- Ultron _reflect_: Repeating 'repeated_groups' could mean two different things: repeated_groups(2, 3) is not repeated_groups(3, 2), so I can't tell which input to feed back in. The REPEAT pattern stops telling me what comes next here, so I won't guess.
- Ultron _reflect_: the column way of 'repeated times' gives the same answer as my law 'grow' on 60 examples; I'll use it for big numbers
- Ultron _reflect_: the column way of 'repeated times' gives the same answer as my law 'repeated_groups' on 60 examples; I'll use it for big numbers
- Ultron _invent_: Two things are always true of my 'repeated_groups' law (checked on 80 examples): repeating p times and then that q times is repeating p·q times, and repeating p times and then q more is repeating p+q times. So if 'repeating half a time' means anything, doing it twice must be repeating once. The only meaning that keeps both laws true: repeating p/q times gives the amount whose q-fold repeat equals the p-fold repeat. It may be a pile of pieces, or a number in a gap.
- Ultron _reflect_: the same law lets me repeat faster: to repeat 2k times, repeat k times and then do that twice (squaring)
- Ultron _invent_: I asked myself grow(2, ?) = 2. No whole number works, and no pile of pieces either (I tried cakes cut into up to 60). But the answer is squeezed: 7/5 gives too little, 8/5 too much, and however finely I cut, it is always caught between two piles, never on one. So my finer line has GAPS: places no pile of pieces reaches. I'll treat each such place as a number too: I can't write it as pieces, but I can pin it between two piles as tightly as I can count.
- Ultron _word_: 'power' behaves exactly like my law 'grow' (arguments yx) in all 6 demonstrations
- **Trainer**: I grew cells and said '3 power 2 equals 9' and so on.
- **Trainer**: Exam for lesson 13, attempt 1: passed
- **Trainer**: What you found in 'repeated_groups' is what people call powers (exponentiation).
- **Trainer**: What you found in 'grow' is what people call exponential growth.

## Lesson 14

- **Trainer**: Lesson 14: Hills and a spring
- Ultron _meet_: new kind of experience: bounce
- Ultron _stuck_: bounce: nothing stays constant yet (1 experiences)
- Ultron _stuck_: bounce: nothing stays constant yet (2 experiences)
- Ultron _stuck_: bounce: nothing stays constant yet (3 experiences)
- Ultron _stuck_: bounce: nothing stays constant yet (4 experiences)
- Ultron _stuck_: bounce: nothing stays constant yet (5 experiences)
- Ultron _stuck_: bounce: nothing stays constant yet (6 experiences)
- Ultron _revise_: bounce: Along each run, none of y, v^2, c^2 stays the same, but y + 0.0509684·v^2 + 10.1937·c^2 does. Each run has its own amount of this hidden quantity: whatever y is lost turns up as v^2 and c^2, and the total never changes. (The coefficient of v^2 is one over 19.62 m/s²: the same units as 'a' in my 'lab_push' experiences.) (The coefficient of c^2 is one over 0.0981 m: the same units as 'x' in my 'lab_stretch' experiences.)
- Ultron _invent_: Along each run, none of y, v^2, c^2 stays the same, but y + 0.0509684·v^2 + 10.1937·c^2 does. Each run has its own amount of this hidden quantity: whatever y is lost turns up as v^2 and c^2, and the total never changes. (The coefficient of v^2 is one over 19.62 m/s²: the same units as 'a' in my 'lab_push' experiences.) (The coefficient of c^2 is one over 0.0981 m: the same units as 'x' in my 'lab_stretch' experiences.)
- Ultron _measure_: bounce: new run S3; its hidden amount is 2.101
- Ultron _measure_: bounce: new run S4; its hidden amount is 2.615
- Ultron _measure_: bounce: new run S5; its hidden amount is 3.496
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 14, attempt 1: passed
- **Trainer**: What you found in 'hidden:bounce' is what people call energy: gravitational + kinetic + elastic (spring).
- **Trainer**: What you found in 'bounce' is what people call conservation of energy with a spring.

## Lesson 15

- **Trainer**: Lesson 15: The diagonal of a tile
- Ultron _meet_: new kind of experience: square
- **Trainer**: Here are square tiles. Build squares and count the tiles in them.
- Ultron _revise_: square: surprised; new best explanation is side (was nothing; 1 experiences, 18 programs searched)
- Ultron _revise_: square: surprised; new best explanation is groups(side, side) (was side; 2 experiences, 2240 programs searched)
- Ultron _confirm_: square: groups(side, side) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _reflect_: the square built on a tile's diagonal is covered by 4 half-tiles: 2 tiles
- Ultron _reflect_: a square is a square: my 'square' law holds for the square on the diagonal too, so the diagonal is the side whose square holds 2 tiles: a number in a gap of my line, between 141/100 and 71/50
- **Trainer**: Now measure the diagonal with rulers. Say what each will read first.
- Ultron _meet_: new kind of experience: ruler
- **Trainer**: Exam for lesson 15, attempt 1: passed
- **Trainer**: What you found in 'gaps' is what people call irrational numbers (the real numbers).
- **Trainer**: What you found in 'diagonal' is what people call the square root of 2 (√2), a tile's diagonal.

## Lesson 16

- **Trainer**: Lesson 16: Phase 2 final exam
- **Trainer**: No teaching today. Show me what you can do.
- **Trainer**: Exam for lesson 16, attempt 1: passed

## Lesson 17

- **Trainer**: Lesson 17: Coiled springs
- Ultron _meet_: new kind of experience: coil_stretch
- Ultron _meet_: new kind of experience: coil_look
- Ultron _stuck_: coil_stretch: nothing stays constant yet (1 experiences)
- Ultron _stuck_: coil_stretch: nothing stays constant yet (2 experiences)
- Ultron _stuck_: coil_stretch: nothing stays constant yet (3 experiences)
- Ultron _stuck_: coil_stretch: nothing stays constant yet (4 experiences)
- Ultron _revise_: coil_stretch: F / x is constant for each spring but differs between them: a hidden property of each spring [N/m] (12 candidates searched; tentative until it predicts 3 new experiences)
- Ultron _measure_: coil_stretch: met new spring C5; measured its property F / x = 100
- Ultron _measure_: coil_stretch: met new spring C1; measured its property F / x = 60
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _invent_: Each spring's F / x (a property I invented, in N/m) isn't arbitrary: it·coils is the same, 600, for all 6 springs whose coils I have counted. That's a law about my law. Now I can know a new spring's property just by counting its coils, and predict what it will do before I ever try it.
- **Trainer**: Exam for lesson 17, attempt 1: passed
- **Trainer**: What you found in 'why:coil_stretch' is what people call a law about a law: stiffness is inversely proportional to the number of coils.

## Lesson 18

- **Trainer**: Lesson 18: Phase 3 exam: the hardest questions
- **Trainer**: No teaching today. Show me what you can do.
- **Trainer**: Exam for lesson 18, attempt 1: passed

## Lesson 19

- **Trainer**: Lesson 19: Handling things
- **Trainer**: Pick these things up and put them down. Your hands will tell you where they are; watch at the same time.
- Ultron _invent_: I handled things 400 times while watching. My hands said where each thing was; I trained a small network of 3 layers of 3x3 filters to light up where my hands felt something (error per picture fell from 83.4 to 3.2). A spot must be at least 0.15 strong to be a thing: that threshold matched my hands best. From now on I see without touching.
- **Trainer**: Now put your hands behind your back. Only look.
- **Trainer**: Exam for lesson 19, attempt 1: passed
- **Trainer**: What you found in 'eyes' is what people call vision (a learned convolutional neural network).

## Lesson 20

- **Trainer**: Lesson 20: Seeing numbers
- Ultron _meet_: new kind of experience: see_merge
- Ultron _meet_: new kind of experience: see_take
- Ultron _revise_: see_merge: surprised; new best explanation is nA (was nothing; 1 experiences, 15 programs searched)
- Ultron _revise_: see_take: surprised; new best explanation is nA (was nothing; 1 experiences, 15 programs searched)
- Ultron _revise_: see_merge: surprised; new best explanation is merge(nA, nB) (was nA; 2 experiences, 10544 programs searched)
- Ultron _revise_: see_take: surprised; new best explanation is take_away(nA, n_taken) (was nA; 2 experiences, 2698 programs searched)
- Ultron _confirm_: see_merge: merge(nA, nB) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: see_take: take_away(nA, n_taken) predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- Ultron _reflect_: 'see_merge' gives the same answer either way round, so I can count along the smaller number
- Ultron _reflect_: imagining with my laws: 'pay' always undoes 'see_merge'
- Ultron _reflect_: the column way of 'add' gives the same answer as my law 'see_merge' on 60 examples; I'll use it for big numbers
- **Trainer**: Exam for lesson 20, attempt 1: passed
- **Trainer**: What you found in 'see_merge' is what people call addition, seen.
- **Trainer**: What you found in 'see_take' is what people call subtraction, seen.

## Lesson 21

- **Trainer**: Lesson 21: Watching motion
- Ultron _reflect_: I practised measuring with my eyes: accelerations wobble by about ±0.5%, spring stretches by about ±1.5%; heights and speeds I'll judge picture by picture
- Ultron _meet_: new kind of experience: see_push
- Ultron _meet_: new kind of experience: see_stretch
- Ultron _meet_: new kind of experience: see_roll
- Ultron _stuck_: see_push: nothing stays constant yet (1 experiences)
- Ultron _stuck_: see_stretch: nothing stays constant yet (1 experiences)
- Ultron _stuck_: see_roll: nothing stays constant yet (1 experiences)
- Ultron _revise_: see_push: F / (a·m) = 1.00248 [dimensionless] in every experiment (7 candidates searched; tentative until it predicts 3 new experiences)
- Ultron _stuck_: see_stretch: nothing stays constant yet (2 experiences)
- Ultron _stuck_: see_roll: nothing stays constant yet (2 experiences)
- Ultron _stuck_: see_stretch: nothing stays constant yet (3 experiences)
- Ultron _stuck_: see_roll: nothing stays constant yet (3 experiences)
- Ultron _stuck_: see_stretch: nothing stays constant yet (4 experiences)
- Ultron _stuck_: see_roll: nothing stays constant yet (4 experiences)
- Ultron _stuck_: see_stretch: nothing stays constant yet (5 experiences)
- Ultron _stuck_: see_roll: nothing stays constant yet (5 experiences)
- Ultron _stuck_: see_stretch: nothing stays constant yet (6 experiences)
- Ultron _stuck_: see_roll: nothing stays constant yet (6 experiences)
- Ultron _stuck_: see_stretch: nothing stays constant yet (7 experiences)
- Ultron _stuck_: see_roll: nothing stays constant yet (7 experiences)
- Ultron _stuck_: see_stretch: nothing stays constant yet (8 experiences)
- Ultron _stuck_: see_roll: nothing stays constant yet (8 experiences)
- Ultron _revise_: see_stretch: W / x is constant for each spring but differs between them: a hidden property of each spring [the data's own units] (20 candidates searched; tentative until it predicts 3 new experiences)
- Ultron _stuck_: see_roll: nothing stays constant yet (9 experiences)
- Ultron _stuck_: see_roll: nothing stays constant yet (10 experiences)
- Ultron _revise_: see_roll: Along each run, none of y, v^2 stays the same, but y + 0.0512375·v^2 does. Each run has its own amount of this hidden quantity: whatever y is lost turns up as v^2, and the total never changes. (The coefficient of v^2 is one over 19.52 m/s²: the same units as 'a' in my 'lab_push' experiences.)
- Ultron _invent_: Along each run, none of y, v^2 stays the same, but y + 0.0512375·v^2 does. Each run has its own amount of this hidden quantity: whatever y is lost turns up as v^2, and the total never changes. (The coefficient of v^2 is one over 19.52 m/s²: the same units as 'a' in my 'lab_push' experiences.)
- Ultron _stuck_: see_roll: nothing stays constant yet (19 experiences)
- Ultron _measure_: see_roll: new run Hill3; its hidden amount is 2.50845
- Ultron _measure_: see_roll: new run Hill3; its hidden amount is 2.49881
- Ultron _measure_: see_roll: new run Hill3; its hidden amount is 2.5082
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 21, attempt 1: passed
- **Trainer**: What you found in 'see_push' is what people call Newton's second law, seen on video.
- **Trainer**: What you found in 'see_stretch' is what people call stiffness (Hooke's law), seen on video.
- **Trainer**: What you found in 'see_roll' is what people call conservation of energy, seen on video.

## Lesson 22

- **Trainer**: Lesson 22: Cooling cups
- Ultron _meet_: new kind of experience: cool
- Ultron _stuck_: cool: no product or sum of the readings stays the same; none of the kinds of explanation I was born with fits
- Ultron _invent_: None of the kinds of explanation I was born with fits 'cool': no product and no sum of the readings stays the same. So I searched a new space: things I can compute along a sequence of readings, shortest first. ρ(Δ(T)) stays the same for each cup (3 cups). That is a new KIND of explanation, not just a new law: the steps between readings shrink (or grow) by the same fraction each time: it settles toward a resting value. I'll keep it and try it first next time.
- Ultron _revise_: cool: ρ(Δ(T)) stays the same for each cup (kind 1: the steps between readings shrink (or grow) by the same fraction each time: it settles toward a resting value)
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 22, attempt 1: passed
- **Trainer**: What you found in 'kind:cool' is what people call exponential decay toward equilibrium (Newton's law of cooling).
- **Trainer**: What you found in 'cool' is what people call Newton's law of cooling.

## Lesson 23

- **Trainer**: Lesson 23: Bouncing, charging, hanging, burning, wandering
- Ultron _meet_: new kind of experience: bounces
- Ultron _meet_: new kind of experience: charge
- Ultron _meet_: new kind of experience: hang
- Ultron _meet_: new kind of experience: burn
- Ultron _meet_: new kind of experience: wander
- Ultron _stuck_: hang: no product or sum of the readings stays the same; none of the kinds of explanation I was born with fits
- Ultron _invent_: None of the kinds of explanation I was born with fits 'hang': no product and no sum of the readings stays the same. So I searched a new space: things I can compute along a sequence of readings, shortest first. Δ(L)/Δ(F) stays the same for each spring (3 springs). That is a new KIND of explanation, not just a new law: equal steps in what I change give equal steps in what I read. I'll keep it and try it first next time.
- Ultron _revise_: hang: Δ(L)/Δ(F) stays the same for each spring (kind 2: equal steps in what I change give equal steps in what I read)
- Ultron _stuck_: bounces: no product or sum of the readings stays the same; none of the kinds of explanation I was born with fits
- Ultron _reuse_: bounces: nothing I was born with explains it, but a kind of explanation I invented does: the steps between readings shrink (or grow) by the same fraction each time: it settles toward a resting value (ρ(Δ(h)) stays the same for each ball); 36 steps of checking
- Ultron _revise_: bounces: ρ(Δ(h)) stays the same for each ball (kind 1: the steps between readings shrink (or grow) by the same fraction each time: it settles toward a resting value)
- Ultron _stuck_: charge: no product or sum of the readings stays the same; none of the kinds of explanation I was born with fits
- Ultron _reuse_: charge: nothing I was born with explains it, but a kind of explanation I invented does: the steps between readings shrink (or grow) by the same fraction each time: it settles toward a resting value (ρ(Δ(q)) stays the same for each battery); 48 steps of checking
- Ultron _revise_: charge: ρ(Δ(q)) stays the same for each battery (kind 1: the steps between readings shrink (or grow) by the same fraction each time: it settles toward a resting value)
- Ultron _stuck_: burn: no product or sum of the readings stays the same; none of the kinds of explanation I was born with fits
- Ultron _reuse_: burn: nothing I was born with explains it, but a kind of explanation I invented does: equal steps in what I change give equal steps in what I read (Δ(H)/Δ(t) stays the same for each candle); 40 steps of checking
- Ultron _revise_: burn: Δ(H)/Δ(t) stays the same for each candle (kind 2: equal steps in what I change give equal steps in what I read)
- Ultron _stuck_: wander: no product or sum of the readings stays the same; none of the kinds of explanation I was born with fits
- Ultron _stuck_: wander: nothing I can express stays the same (3 walkers, 24 readings)
- Ultron _stuck_: wander: nothing I can express stays the same (4 walkers, 31 readings)
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 23, attempt 1: passed
- **Trainer**: What you found in 'kind:hang' is what people call a linear relationship (a constant rate of change).
- **Trainer**: What you found in 'bounces' is what people call coefficient of restitution (geometric decay).
- **Trainer**: What you found in 'charge' is what people call exponential approach to a limit.
- **Trainer**: What you found in 'hang' is what people call Hooke's law with an unstretched length.
- **Trainer**: What you found in 'burn' is what people call constant rate.

## Lesson 24

- **Trainer**: Lesson 24: Using what it knows
- Ultron _meet_: new kind of experience: slide
- Ultron _stuck_: slide: nothing stays constant yet (1 experiences)
- Ultron _revise_: slide: d / u^2 = 0.172769 [m^-1·s^2] in every experiment (6 candidates searched; tentative until it predicts 3 new experiences)
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 24, attempt 1: passed
- **Trainer**: What you found in 'slide' is what people call sliding friction (stopping distance ∝ speed²).

## Lesson 25

- **Trainer**: Lesson 25: Phase 3 exam: seeing, inventing, acting
- **Trainer**: No teaching today. Show me what you can do.
- **Trainer**: Exam for lesson 25, attempt 1: passed

## Lesson 27

- **Trainer**: Lesson 27: Swinging, dying down, growing, emptying
- Ultron _meet_: new kind of experience: swings
- Ultron _meet_: new kind of experience: bumps
- Ultron _meet_: new kind of experience: yeast
- Ultron _meet_: new kind of experience: funnel_h
- Ultron _stuck_: swings: no product or sum of the readings stays the same; none of the kinds of explanation I was born with fits
- Ultron _stuck_: swings: nothing I can express stays the same (3 pendulums, 20 readings)
- Ultron _invent_: None of the kinds of explanation I was born with fits 'swings': no product and no sum of the readings stays the same. So I searched a new space: things I can compute along a sequence of readings, shortest first. angle[n] = a1·angle[n-1] + a2·angle[n-2] stays the same for each pendulum (3 pendulums). That is a new KIND of explanation, not just a new law: the next reading is the same mix of the last 2: how the state changes is a law of the state (it swings, or swings and dies down). I'll keep it and try it first next time.
- Ultron _revise_: swings: angle[n] = a1·angle[n-1] + a2·angle[n-2] stays the same for each pendulum (kind 3: the next reading is the same mix of the last 2: how the state changes is a law of the state (it swings, or swings and dies down))
- Ultron _stuck_: bumps: no product or sum of the readings stays the same; none of the kinds of explanation I was born with fits
- Ultron _stuck_: bumps: nothing I can express stays the same (3 cars, 20 readings)
- Ultron _reuse_: bumps: nothing I was born with explains it, but a kind of explanation I invented does: the next reading is the same mix of the last 2: how the state changes is a law of the state (it swings, or swings and dies down) (z[n] = a1·z[n-1] + a2·z[n-2] stays the same for each car); 138 steps of checking
- Ultron _revise_: bumps: z[n] = a1·z[n-1] + a2·z[n-2] stays the same for each car (kind 3: the next reading is the same mix of the last 2: how the state changes is a law of the state (it swings, or swings and dies down))
- Ultron _stuck_: yeast: no product or sum of the readings stays the same; none of the kinds of explanation I was born with fits
- Ultron _invent_: None of the kinds of explanation I was born with fits 'yeast': no product and no sum of the readings stays the same. So I searched a new space: things I can compute along a sequence of readings, shortest first. ρ(Δ(cells^-1)) stays the same for each jar (3 jars). That is a new KIND of explanation, not just a new law: not the reading itself but its power -1: the steps between readings shrink (or grow) by the same fraction each time: it settles toward a resting value. I'll keep it and try it first next time.
- Ultron _revise_: yeast: ρ(Δ(cells^-1)) stays the same for each jar (kind 4: not the reading itself but its power -1: the steps between readings shrink (or grow) by the same fraction each time: it settles toward a resting value)
- Ultron _stuck_: funnel_h: no product or sum of the readings stays the same; none of the kinds of explanation I was born with fits
- Ultron _invent_: None of the kinds of explanation I was born with fits 'funnel_h': no product and no sum of the readings stays the same. So I searched a new space: things I can compute along a sequence of readings, shortest first. Δ(Δ(h)) stays the same for each funnel (3 funnels). That is a new KIND of explanation, not just a new law: the steps between readings change by the same amount each time. I'll keep it and try it first next time.
- Ultron _revise_: funnel_h: Δ(Δ(h)) stays the same for each funnel (kind 5: the steps between readings change by the same amount each time)
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 27, attempt 1: passed

## Lesson 28

- **Trainer**: Lesson 28: Rows of things
- Ultron _meet_: new kind of experience: basket
- Ultron _meet_: new kind of experience: tall
- Ultron _meet_: new kind of experience: rise
- Ultron _meet_: new kind of experience: two_rows
- Ultron _revise_: basket: surprised; new best explanation is 2 (was nothing; 1 experiences, 29 programs searched)
- Ultron _revise_: tall: surprised; new best explanation is 0 (was nothing; 1 experiences, 25 programs searched)
- Ultron _revise_: rise: surprised; new best explanation is [succ] each of prices (was nothing; 1 experiences, 5684 programs searched)
- Ultron _revise_: two_rows: surprised; new best explanation is merge pair by pair of row_a and row_b (was nothing; 1 experiences, 6128 programs searched)
- Ultron _revise_: basket: surprised; new best explanation is start at 1 and groups in each of prices (was 2; 2 experiences, 5875 programs searched)
- Ultron _revise_: basket: surprised; my other idea start at 0 and merge in each of prices fits everything (was start at 1 and groups in each of prices)
- Ultron _revise_: tall: surprised; new best explanation is spend_notes(mark, 3) (was 0; 3 experiences, 2606 programs searched)
- Ultron _revise_: tall: surprised; new best explanation is spend_notes(mark, how many in heights) (was spend_notes(mark, 3); 4 experiences, 26275 programs searched)
- Ultron _revise_: tall: surprised; new best explanation is how many in those of heights above mark (was spend_notes(mark, how many in heights); 6 experiences, 740532 programs searched)
- Ultron _confirm_: rise: [succ] each of prices predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: two_rows: merge pair by pair of row_a and row_b predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: basket: start at 0 and merge in each of prices predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _confirm_: tall: how many in those of heights above mark predicted 8 new experiences in a row; added to my library of building blocks
- Ultron _bored_: nothing here is teaching me anything new any more
- **Trainer**: Exam for lesson 28, attempt 1: passed
