# Stage 3: language

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

### WP4: grammar by MDL (L3, L4)

A grammar is a program that maps a word sequence to a meaning. The shortest grammar
that explains every sentence heard, with the meanings checked in the world, wins. The
same learner, with no dataset-specific rules, runs on SCAN and COGS (both on GitHub,
reachable from this environment, checked 2026-10-11).

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
| L1 | ✅ **met** (2026-10-11), lesson 29. On 200 sentences about new tables, each with a word pair never heard together: **200/200**, and 200 right of 200 answers given. Baselines: co-occurrence counter 78/200 (39%), memoriser 41/200 (20%): 61 points above the better one. Words never taught: 30/30 refused (baselines 0/30 and 3/30). Every word settled after at most 20 sentences that used it (most 2–11). 120 sentences heard in all |
| L2–L10 | not started |

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
