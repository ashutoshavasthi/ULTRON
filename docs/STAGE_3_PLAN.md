# Stage 3: language

> **No longer the main line (2026-10-15).** The plan was rebuilt around growing up
> from a newborn ([MASTER_PLAN.md](MASTER_PLAN.md), [ROADMAP.md](ROADMAP.md)). This plan is
> kept as a record and its results are banked: words (L1, L2) are re-hosted with the caregiver at Age 2 (toddler), and grammar and conversation (L3–L10, with SCAN and COGS) belong to Age 3 (preschool). See
> [DEVELOPMENT_MAP.md](DEVELOPMENT_MAP.md).

**Mission.** Ultron knows 37 grounded words, all about numbers and arithmetic (lesson 4
and its follow-ups). It cannot understand a sentence, say one, or ask a question.
Stage 3 gives it language the way it got numbers: words attached to things it already
sees and laws it already knows, then a grammar it finds itself as the shortest account
of how words combine, then understanding, speaking, asking and being told.

Language comes **before** the reader (stage 5): text read from the internet can only be
checked as a claim once Ultron can understand what the text says.

## How this stage went missing (traced 2026-10-11)

| Date | Commit | What happened to language |
|---|---|---|
| 2026-06-17 | `bdd802d` | The PRDs plan a "linguistic foundation" early (PRD v2, v3.6): spaCy, WordNet, AllenNLP and a hand-written table of connectors |
| 2026-09-30 | `a0394c4` | The first roadmap replaces that with **Phase 5, grounded language → English**: "words by pointing, then grammar, then conversation. Only then reading." The rule: language after the concepts it names, reading after language |
| 2026-09-30 | `a0394c4` | Lesson 4 (names): the only language ever built. Number words and marks, `plus`, `minus`, `times`, `equals`, place value. Later lessons add `after`, `power`, `divided`, `negative` |
| 2026-10-09 | `375c5c5` | Stages A–H. Reading is split out of language into its own stage C and placed **before** language (D). The "only then reading" rule is lost |
| 2026-10-09 | `854f4e7` | Master plan: the reader becomes stage 3, language stage 4 |
| 2026-10-09 | `5ec50ac` | Interactive worlds inserted as stage 3: the reader moves to 4, language to 5 |

So the language phase was never deleted. It was **pushed back** each time a stage was
inserted ahead of it, and the reader, which needs language, was put in front of it. It
never had a stage plan, its exit test never had numbers, and no language work has been
done since September 30.

The PRD's linguistic layer is not restored. A hand-written connector table and a
pretrained parser are the answer written in by hand, which design law 5 forbids. The
grounded route of the first roadmap is the one restored here.

## Exit test (fixed now, before the work)

Every test runs on held-out material made by a generator Ultron never sees: new
scenes, new combinations of words, longer sentences than any it heard. Every row
reports **precision** (answers right of answers given) as well as score, and how many
sentences Ultron heard to get there.

| # | Criterion |
|---|---|
| L1 | **Words by pointing.** In scenes with several things, the Trainer speaks about one of them and never says which word means what. On 200 held-out scenes whose word combinations it never heard (for example "red cube" when it heard only "red ball" and "blue cube"), Ultron picks the thing named ≥ 95% of the time. Each word is learned from ≤ 20 scenes. For words it was never taught it says it doesn't know them, every time (no guessing). It beats two baselines fixed in advance, a word–thing co-occurrence counter and a nearest-neighbour memoriser, by ≥ 20 points on the unseen-combination split |
| L2 | **Words for its own laws.** Verbs and relation words (falls, bounces, rolls, stops, faster, heavier, more, fewer, before, after) are bound to laws and kinds it already has, as `plus` was bound to its addition law. On held-out films it names the event right ≥ 90% of the time, including objects it never saw doing that thing |
| L3 | **Grammar, found by MDL.** Ultron finds how words combine (order, nesting, agreement) as the shortest grammar that maps what it hears to meanings it can check in its worlds. On held-out splits of its own worlds' language (a word heard only alone, now inside sentences; sentences with more clauses than any it heard; deeper nesting) it gets the exact meaning ≥ 95% of the time |
| L4 | **Grammar against public tests.** No rule written for these datasets. SCAN (Lake and Baroni, 2018): ≥ 95% exact match on the "add primitive jump" and "length" splits. COGS (Kim and Linzen, 2020): ≥ 90% on the generalisation set. Baselines are the published sequence-to-sequence scores (about 1% on SCAN jump and about 14–21% on SCAN length; about 35% for a Transformer on COGS), confirmed from the papers and recorded before the work starts, plus our own lookup baseline |
| L5 | **Understanding.** Statements about held-out scenes, its laws and its numbers ("the blue ball bounces higher than the red one", "seven times six is forty-two", "a heavier ball falls faster"): true or false right ≥ 95%; on statements its experience cannot decide it says "I can't tell" ≥ 90% of the time; precision ≥ 98% on the answers it gives; planted false statements caught ≥ 95% |
| L6 | **Answering questions.** Who, what, which, how many, when, and "what will happen", the last answered by running its own laws forward: ≥ 90% right on held-out questions, precision ≥ 98%, beating an answer-frequency baseline and a lookup baseline |
| L7 | **Speaking.** It describes held-out scenes and states its own laws in sentences ("the force is the mass times the acceleration"). An independent listener (a parser the examiner writes from the Trainer's grammar, not Ultron's) recovers the meaning of ≥ 90% of them; ≥ 98% of what it says is true |
| L8 | **Asking.** In a guessing game (one hidden thing among many, or one unknown law) it finds the answer in ≤ 1.2× the fewest questions possible, on average, beating a random-question baseline. Given a word it doesn't know, it asks about it instead of guessing |
| L9 | **Being told.** Told something in words ("a glim is a small red ball", "springs with more coils stretch more"), it keeps it as a **claim** and checks it against its world before believing it: true claims adopted and false ones refused ≥ 95% of the time on held-out claims. A word it learned only from being told is used right in held-out scenes ≥ 90% of the time. A sentence is never an instruction |
| L10 | **Blind test.** From a public syllabus of what it was taught, examiners who never saw the code write sentences and questions: ≥ 90% right on first sight, and a human's blind test |

Efficiency: L1, L2, L3, L5 and L6 together are reached with **≤ 10,000** Trainer
sentences in all. The number heard per criterion is reported against the baselines.

Everything Stages 1 and 2 passed must still pass: the curriculum (every lesson on the
first attempt), every exam, every failure-lab row, the blind tests and the full test
suite. A retrain stays byte-for-byte identical. Lesson 4's words keep their meanings.

## Rules for this stage

- **The Trainer speaks; it never explains.** The Trainer's English comes from a
  generator (a small grammar of its own) that Ultron cannot read. Ultron gets only the
  sentence and the scene, film or world it is about.
- **No pretrained language.** No word vectors, parsers, taggers or language models,
  neither as a component nor as a teacher. Baselines may use them, clearly labelled.
- **Meanings are programs in the brain's own language,** checked against the world, so a
  meaning can be wrong and found wrong.
- **The failure lab gets a language experiment**: misheard words, a Trainer who mislabels
  some scenes, sentences longer than any heard, words with two meanings. Its breakpoints
  are recorded and only move outward.

## Work packages

### WP1: a world to talk about

A scene world built on the Stage 2 eyes: things of several shapes, colours and sizes,
at places, that roll, fall, bounce and stop. Plus the existing worlds (piles, physics,
sequences). The Trainer's speech generator lives in the Trainer, with held-out splits
fixed in advance and stored with their seeds.

### WP2: words by pointing (L1)

Cross-situational learning, extending `brain/language.py`: a word's meaning is the
shortest description of a thing that is present every time the word is said and rarely
otherwise. Unknown words stay unknown.

### WP3: verbs and relations from its own laws (L2)

As `bind_operation` binds `plus` to the addition law, bind event words to laws and kinds
of change, and comparison words to orderings it can measure.

**L2's exam, fixed in code before the real run (2026-10-11, `judge/exams.py`,
`exam_events`, seed 1030, never used during the work).** Films of 30 pictures of things
on a floor, seen from the side (`senses/floor.py`). Two parts, both must reach 90%:
- *Naming what happens.* 200 new films. The Trainer says "the yellow box ..." and
  Ultron says what that thing does: falls, bounces, rolls or stops. Every film is about
  a thing whose colour, size or shape was never seen doing that in teaching (box
  bounces, bar rolls, ball stops, green falls, yellow bounces, big rolls). Right means
  the word the Trainer would have said; saying nothing is wrong.
- *Comparing.* 120 new films. The Trainer's sentence has its comparing word left out
  ("the red ball rolls ___ the box"); Ultron fills it in. Every sentence pairs a word
  with a kind of thing never heard together in teaching (bar faster, box heavier,
  yellow before, red after, green more, blue fewer). Right means it says the Trainer's
  word, and every word it says is true of the film (the Trainer's truth, from the
  simulator: "heavier" by the hidden masses, "before" by when each thing really starts).
- Baselines, fixed before measuring: a memoriser (the word of the remembered sentence
  sharing most words) and a co-occurrence counter (the word most often heard with the
  kind of thing, or the ordering, in the film), both given Ultron's own kinds and
  measurements.

### WP4: grammar by MDL (L3, L4)

A grammar is a program that maps a word sequence to a meaning. The shortest grammar
that explains every sentence heard, with the meanings checked in the world, wins. The
same learner, with no dataset-specific rules, runs on SCAN and COGS (both on GitHub,
reachable from this environment, checked 2026-10-11).

**L3's exam, fixed before the work (2026-10-11, `judge/exams.py`, `exam_grammar`, seed
1031, never used during the work).** Tables of coloured things like L1's, with up to 10
things. The Trainer speaks its own small grammar, which Ultron never reads: a noun
phrase is "the [size] [colour] shape", maybe followed by "left of", "right of", "above"
or "below" (sometimes "that is left of" ...) and another noun phrase; noun phrases are
joined by "and". It says a sentence only when, of every way its own grammar could put
the words together, exactly one picks out something on the table (it speaks to be
understood). Ultron says which thing or things are meant. 200 new tables, in three
held-out splits:
- *Deeper nesting* (70): 3 or 4 noun phrases inside one another ("the ball left of the
  box above the bar right of the ball"). Teaching has at most 2.
- *More joined phrases* (60): 3 or 4 noun phrases joined by "and". Teaching has at
  most 2.
- *Words in new places* (70): "bar", heard in teaching only alone ("the bar"), and
  "below", heard only between two bare shapes ("the box below the ball"), now inside
  longer sentences, with sizes, colours, nesting and "and".
- Right means exactly the things meant; saying it can't tell counts as wrong. It must
  reach **95% on each split**, and precision is reported.
- Baselines, fixed before measuring: *bag of words* (the things that fit every word it
  knows, relations ignored) and *first phrase* (the one thing that fits the first noun
  phrase, the rest of the sentence ignored).

**L4's published baselines, confirmed from the papers (2026-10-11), before any L4 work:**
- SCAN (Lake and Baroni 2018, arXiv:1711.00350v3). "Add jump": the best model got
  **1.2%** (an LSTM with attention, one layer of 100 units, dropout 0.1); the model best
  overall got 0.08%. Length: the best got **20.8%** (a GRU with attention, one 50-unit
  layer, dropout 0.5, mean of 5 runs); the model best overall got 13.8%.
- COGS (Kim and Linzen 2020, arXiv:2010.05465v1, Table 2). Generalisation set:
  Transformer **35%** (± 6), one-way LSTM 32% (± 6), two-way LSTM 16% (± 8); the
  in-distribution test set 96–99%.
- The exam files are the published ones, as fetched on 2026-10-11 (SHA-256):
  - SCAN `add_prim_split/tasks_test_addprim_jump.txt` (7,706):
    `8147ae2651422c701162e174d9d66158daa57858a26b30317ac61797118ac7a5`
  - SCAN `length_split/tasks_test_length.txt` (3,920):
    `0760752ed34a75116ae11dcc1ee17526b7500060da1366540730fa24894d7db3`
  - COGS `data/gen.tsv` (21,000):
    `d013d9eee0bafc153f8decc85f42814ac97260f84964d980e1e2b84577b82361`

  Of them only the format was looked at (a few lines, COGS's list of generalisation
  cases with two examples of each, and how its facts are ordered); no score has been
  measured on them.

### WP5: understanding and answering (L5, L6)

Turn a sentence's meaning into a check (a statement) or a search (a question) over its
world model and laws. "I can't tell" when nothing it knows decides it.

### WP6: speaking (L7)

Run the grammar backwards: from a meaning to the shortest sentence that says it.

### WP7: asking (L8)

Curiosity's information gain, applied to questions: ask the question whose answer
splits the remaining possibilities most evenly.

### WP8: being told (L9)

A told sentence becomes a claim with its source, checked like any other evidence. This is
the first piece of the safety rule the reader needs: untrusted text is a claim, never an
instruction.

### WP9: blind syllabus and test (L10)

A public syllabus of the words and kinds of sentence taught, as `blind/SYLLABUS.md` did
for numbers and physics.

## Order

WP1, then WP2 and WP3, then WP4 (the heart of the stage), then WP5 to WP8, then WP9.

## Status

| # | Status |
|---|---|
| L1 | ✅ **met** (2026-10-11), lesson 29 (lesson 31 in the combined curriculum). On 200 sentences about new tables, each with a word pair never heard together: **200/200**, and 200 right of 200 answers given. Baselines: co-occurrence counter 78/200 (39%), memoriser 41/200 (20%): 61 points above the better one. Words never taught: 30/30 refused (baselines 0/30 and 3/30). Every word settled after at most 20 sentences that used it (most 2–11). 120 sentences heard in all |
| L2 | ✅ **met** (2026-10-11), lesson 30 (lesson 32 in the combined curriculum). Naming what happens in 200 new films, each about a thing whose colour, size or shape never did that in teaching: **200/200**, 200 right of 200 answers. Filling in the comparing word in 120 new films, each pairing a word with a kind of thing never heard together: **113/120** (94%), and every one of its 113 answers wholly true; it said it couldn't tell 7 times. Baselines: co-occurrence counter 200/200 and 100/120, memoriser 6/200 and 16/120. Each word for what happens settled after at most 10 sentences that used it. 220 sentences heard |
| L3 | ✅ **met** (2026-10-11), lesson 31 (lesson 33 in the combined curriculum). On 200 new tables of up to 10 things, the things meant: **69/70** with noun phrases nested 3–4 deep (teaching: at most 2), **59/60** with 3–4 phrases joined by "and" (teaching: at most 2), **70/70** with "bar" and "below" in places it never heard them; 198 right of 198 answers, and it said it couldn't tell twice. Baselines: a bag of words 0/70, 0/60, 16/70; the first noun phrase alone 0/70, 0/60, 16/70. Grammar found from 300 sentences |
| L4 | ⏸ **paused** (2026-10-11, the owner's decision: language waits until the coding work passes). The published baselines were confirmed from the papers and are recorded under WP4. Nothing for L4 is in the repository yet |
| L5–L10 | not started |

How L1 was met (`senses/tabletop.py`, `senses/things.py`, `brain/categories.py`,
`brain/language.py`, `trainer/language_lessons.py`):
- **A table to talk about.** A colour camera over things of 4 colours, 2 sizes and 3
  shapes. Its eyes say where things are; around each place, what stands out from the
  table is the thing. It measures each thing itself: hue, size, how long it is, how much
  of its outline box it fills, and where it is. 60 tables, 0 things missed.
- **Kinds before words.** Looking at 60 tables with nothing said, it asks of each measure
  whether the values fall into groups that pay for their boundaries (MDL). Hue: 4
  groups, size: 2, elongation: 2, fill: 2. Where things lie: no groups.
- **Words from overheard sentences.** The Trainer says "the big red ball" and never
  says which word means what, or which thing it means. The lexicon kept is the
  shortest account of all it heard: the bits to state each meaning, plus the bits still
  needed to say which thing each sentence was about, minus the coincidences a meaning
  explains (a word said only about blue things, if it meant nothing, would be chance).
  The Trainer speaks to be understood, so an account in which its sentences were often
  ambiguous is an unlikely one. Combining words is "fits every word"; a word means one
  measure unless picking things out needs two ("box": not long, and filling its box).
  These are the assumptions given; the meanings are found.
- **Not sure yet.** Accounts nearly as short as the best are kept as rivals. When they
  would pick different things, Ultron says it isn't sure what a word means instead of
  guessing.

Baselines, fixed in code before the first measurement (`judge/exams.py`): a co-occurrence
counter (how much more often each kind of thing is on the table when a word is said) and
a nearest-example memoriser (the thing whose kind was most often on the tables of the
remembered sentences sharing the most words). Both see Ultron's own kinds of thing.

**The failure lab found two weaknesses, now fixed** (`python -m ultron stress`, "words by
pointing", taught on other tables than lesson 29). With the first lexicon learner, on the
lab's tables, a word that was only ever said as an extra ("blue", 4 times) was never
learned (53/60), and with 60 sentences or fewer it gave wrong answers. Fixes, kept because
no row got worse: the coincidence term, the cooperative speaker, a wider search (started
again from each word holding each kind; the first search stopped at an account 28 bits
longer than the best), and rivals. Lesson 29's exam was 200/200 before and after.

| Failure lab (60 sentences about new tables) | Right | Answers given |
|---|---|---|
| 0%, 5%, 10% of sentences name the wrong thing | 60 | 60 |
| 20% name the wrong thing | 37 | 37 (it refuses the rest) |
| 30% name the wrong thing | 60 | 60 |
| 60 or 40 sentences heard | 40 | 40 |
| 20 or 10 sentences heard | 0 | 0 |

It gives **no wrong answer in any row**. It breaks (fewer than 57/60 answered) at 20% of
sentences misnamed and at 60 sentences heard. The 30% row passing where 20% does not is
chance in which sentences were spoiled, not a trend.

**Limits, said plainly.** The world is small and clean: four well-separated colours, two
sizes, three shapes, things never touching. The exam's tables were looked at several
times during the work (Ultron scored 200/200 on them each time); the changes were made
for the failure lab's tables, not for the exam's. Speech is one fixed sentence shape
("the [size] [colour] [shape]"); grammar is L3.

How L2 was met (`senses/floor.py`, `senses/things.py`, `brain/events.py`,
`brain/language.py`, `trainer/language_lessons.py`, lesson 30):
- **Films to talk about.** The same coloured things, now filmed from the side for 30
  pictures: they fall, bounce, roll, slide to a stop, knock into each other, or stay
  still on shelves. The simulator keeps the true gravity, springiness, masses and start
  times; Ultron gets only the pictures.
- **Following things.** Its eyes find the things in the first picture; then it follows
  each to the nearby region of the same colour and size, where it expected it from how
  it was moving. While two things touch it can't tell them apart and skips those
  pictures. What each thing looks like is measured as on the table: from 8 pictures cut
  out around it, lined up and averaged, using pictures where nothing else is near it.
- **Motion in its own kinds of law.** Each thing's path across and up-down is described
  as the shortest run of pieces (MDL, at the camera's own noise), each piece a kind of law
  it already had: nothing changes, equal steps, and the kinds it found itself in Phase 3
  (steps changing by the same amount, steps shrinking by the same fraction). From the
  pieces it reads which kind of law each move followed, whether it came back the way it
  went, when it started, and how fast it went (and how sure it is of each).
- **Weighing by its momentum law.** When two things knock and both change speed, its
  lesson-5 law (Σ m·v stays the same) says how heavy one is compared with the other.
- **Words for what happens.** Overheard sentences ("the red ball bounces") are learned
  with the same shortest-account learner as L1, keeping the words it already has:
  bounces = it comes back the way it went, falls = its move up and down follows "steps
  changing by the same amount", rolls = its move across follows "equal steps", stops =
  its move across follows "steps shrinking by the same fraction". To name what a thing
  did it says the word that fits and is rarest among what it has watched.
- **Comparing words.** Each comparing word means the measured quantity, and which way
  round, that holds in every sentence it was heard in (MDL over the options; "is",
  "than", "there", "are" mean nothing it can check): faster = more speed, heavier = more
  mass, before / after = earlier / later start, more / fewer = more / fewer things. It
  says a comparing word only when the measured difference is more than twice its
  uncertainty, and only when no rival account would disagree.
- **Saying it can't tell.** It doesn't name what a thing did when it didn't see it move,
  when it heard a word for what happens whose meaning it hasn't found, or when two of its
  words seem to mean the same.

Baselines, fixed in code before the first measurement (`judge/exams.py`): a memoriser
(the word of the remembered sentence sharing most words) and a co-occurrence counter
(the word most often heard with the kinds of thing, or the orderings, in the film). Both
were given Ultron's own kinds of thing and of motion and its own measurements. **The
counter matches Ultron on naming what happens (200/200):** once motion is seen as its own
kinds of law, counting which kind goes with which word is enough. The hard part of L2
was in the seeing. On comparing it is 13 points behind (100/120).

**Found on practice films before the real exam** (other seeds than the exam's): a thing
nudged too slowly to see seemed to start late, so "after" was said falsely; a thing
named in a sentence but not found was compared as "none"; how fast a bouncing thing went
was reported surer than it was; things 3 pixels apart merged in its eyes. Fixed: the
Trainer's knocks start at a speed anyone would notice, comparing needs both things
found and distinct, the uncertainty of a speed includes not knowing to the picture when
moving began and ended, things stand a pixel further apart than the closest on the
table, and a thing's look is taken from pictures where nothing else is near it.

**The failure lab found wrong answers, now fixed** (`python -m ultron stress`, "words
for what happens", taught and tested on other films than lesson 30). With 20% of event
sentences saying the wrong word, it learned "rolls" as "small" (in teaching, big things
never roll) and "bounces" as the same as "falls", and answered wrong 26 times; through a
camera 3 times as noisy it learned "falls" as "doesn't move across" and named a still
thing. Fixed by the three ways of saying it can't tell, above. Lesson 30's exam was the
same before and after (200/200 and 113/120); no old row of the lab moved.

| Failure lab (60 new films each) | Right | Answers given |
|---|---|---|
| 0% or 10% of event sentences say the wrong word | 60 | 60 |
| 20% or 30% say the wrong word | 0 | 0 (it can't find what some words mean, and says so) |
| 50 or 25 event sentences heard | 60 | 60 |
| 12 event sentences heard | 33 | 33 |
| camera 2 times as noisy | 50 | 50 (its eyes misjudge some shapes and sizes, so it can't find the thing named) |
| camera 3 times as noisy | 33 | 33 |
| 0% or 10% of comparing sentences say the wrong word | 60 | 60 |
| 20% of comparing sentences say the wrong word | 15 | 15 |

It gives **no wrong answer in any row**. It breaks (fewer than 54/60 right) at 20% of
sentences saying the wrong word, at 12 sentences heard and at twice the camera noise.

**Limits, said plainly.** The films are clean: one camera that never moves, things that
never hide one another and touch only when they knock. "Heavier" can be decided only for
two things that knocked into each other; otherwise it says it can't tell. The exam's
films were watched twice: once at the real run, and again after the failure-lab fixes
(the same scores both times). Speech is a few fixed sentence shapes; grammar is L3.

How L3 was met (`brain/grammar.py`, `trainer/grammar_lessons.py`, lesson 31):
- **Longer sentences about the same tables.** The Trainer now says things like "the red
  ball left of the big box", "the ball that is above the box right of the ball" and "the
  green box and the small ball". Its grammar lives in the Trainer, which Ultron never
  reads: a noun phrase is "the [size] [colour] shape", maybe followed by a relation and
  another noun phrase, and noun phrases are joined by "and". It says a sentence only when,
  of all the ways its grammar could read it, exactly one picks out something on the
  table, and each relation it says is needed to tell the thing apart. Ultron gets the
  words and the picture; nobody says which thing is meant or what any word does.
- **What a word can do.** Each word does one of a few things to the phrase next to it:
  nothing; keep the things of one of its own kinds (from L1); pick out the one thing
  ("the": if the phrase names several, the phrase fails); keep the things that are
  further one way, on a quantity it measures (place across, height, size), than one of
  the things of another phrase; put two phrases' things together; or keep what two
  phrases share. How it combines is a category, as in a categorial grammar: it takes the
  phrase before or after it, or one on each side. Phrases are put together by the
  categories alone, so a phrase can sit inside another of the same kind as deep as you
  like.
- **The shortest account.** The grammar is what makes everything heard shortest: the
  bits to say what each word does and how it combines, plus, for each sentence, the bits
  still needed to say which things it meant (no reading at all costs most; several
  readings cost more than one). Categories are counted per kind of word, so words that do
  the same thing share a way of combining unless what was heard pays for a difference.
  The search changes one word at a time, and also holds each word at its next best
  meanings and at "nothing" while the others settle, because words can be tied together
  ("that" and "is" only make sense as a pair). Grammars nearly as short are kept as
  rivals; where they read a sentence differently it says it isn't sure.
- **What it found**, from 300 sentences: "the" picks out the one thing the phrase after
  it names; sizes and colours keep things of the phrase after them; shapes name things;
  left, right, above and below take the phrase after them and keep the things of the
  phrase before them that are further left, further right, higher or lower than one of
  them; "and" puts the two phrases' things together; "of", "that" and "is" mean nothing by
  themselves (4 kinds of word in all).
- **Saying it isn't sure.** It doubts a word when the sentences with that word go
  unexplained far more often than sentences do in general (chance below 1 in 1,000), and
  when the grammar it finds from every other sentence and from the rest disagree on that
  word. It doesn't answer a sentence with a doubted word.

Baselines, fixed in code before the first measurement (`judge/exams.py`): a bag of words
(the things that fit every word it knows a kind for, whatever the order) and the first
noun phrase alone (the one thing that fits the words before the first word that names no
kind). Both get none of the nested or joined sentences right, and 16/70 where a held-out
word is in a new place.

**Found on practice tables before the real exam** (other seeds than the exam's): "below"
took the reverse way of combining from "above" (fixed by counting categories per kind of
word); "that" and "is" stuck as a pair meaning something (fixed by holding words at
"nothing" during the search); learning took 453 s (now about 70 s, by first screening
each word's meanings on a few sentences). On practice tables it got 70/70, 59/60 and
68/70; the misses were its eyes (a thin bar missed, small balls seen as boxes).

**The failure lab found wrong answers, now fixed** (`python -m ultron stress`, "how
words combine", taught and tested on other tables than lesson 31). With "left" also said
for "above" half the time, it answered wrongly 8 times; with 40% of sentences about
another table, 21 times. Fixed by the two doubts above. Lesson 31's exam was first
run after the fixes.

| Failure lab (60 new tables each) | Right | Answers given |
|---|---|---|
| no word misheard | 60 | 60 |
| 20% of sentences with a word misheard | 34 | 34 |
| 40% with a word misheard | 19 | 19 |
| 20% of sentences about another table | 60 | 60 |
| 40% about another table | 0 | 0 (it doubts every relation word) |
| "left" also said for "above", half the time | 35 | 35 (it doubts "left") |
| 75 sentences heard | 25 | 25 |
| 30 sentences heard | 0 | 0 |

It gives **no wrong answer in any row**. It breaks (fewer than 57/60 right) at 20% of
sentences with a word misheard and at 75 sentences heard.

**Limits, said plainly.** The second doubt is cautious: on less or noisier teaching, the
grammars found from the two halves often differ, so it refuses sentences it would have
got right (without that doubt it got 60/60 with 20% misheard and with 75 sentences, but
answered wrongly 21 times with 40% about another table). That is not a search failure:
with 40% about another table, the wrong grammar it found is genuinely shorter than the
right one (1,228 bits against 1,254), so the shortest account alone can't tell; and on
half of 75 sentences a wrong grammar is shorter too. The language is the Trainer's small
grammar about tables. Relations are about where things lie in one picture; agreement,
verbs and clauses come with the public tests (L4).
