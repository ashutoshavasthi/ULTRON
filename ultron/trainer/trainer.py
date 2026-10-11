"""The Trainer: runs the curriculum, gates each lesson on a held-out exam, and
names concepts only *after* Ultron has shown it understands them.

The Trainer may look at the world's ground truth to grade answers. It never
passes a law, formula or answer into the brain.
"""

import math

from ..brain.language import bind_number, bind_operation, bind_prefix, bind_relation
from ..judge.exams import EXAMS
from .lessons import RealData, all_lessons

MAX_ATTEMPTS = 3


def free_play(brain, lesson, budget, wide=False, names=None):
    """Ultron chooses what to play with, by learning progress."""
    options = names or [s.name for s in lesson.specs()]
    for _ in range(budget):
        # bored of everything? not while an idea is still unconfirmed
        choice = brain.curiosity.choose(options) or brain.unsure(options)
        if choice is None:
            brain.note("bored", "nothing here is teaching me anything new any more")
            break
        brain.log.append({"lesson": brain.lesson, "kind": "choice", "choice": choice,
                          "text": f"chose to play with {choice}"})
        request = brain.propose(choice, lesson.options(choice))
        inputs, outcome = lesson.scene(choice, wide, request)
        brain.experience(choice, inputs, outcome)
    brain.reflect()


def guided(brain, lesson, n, wide=True):
    """The Trainer sets up scenes itself (used when Ultron failed an exam)."""
    options = [s.name for s in lesson.specs()]
    for i in range(n):
        name = options[i % len(options)]
        inputs, outcome = lesson.scene(name, wide)
        brain.experience(name, inputs, outcome)


class Trainer:
    def __init__(self, brain, seed=0):
        self.brain = brain
        self.lessons = {l.number: l for l in all_lessons(seed)}
        self.results = {}

    def say(self, text):
        self.brain.note("trainer", text)

    def run(self, number):
        lesson = self.lessons[number]
        brain = self.brain
        brain.lesson = number
        lesson.brain = brain            # lessons with senses need to know whose eyes look
        self.say(f"Lesson {number}: {lesson.title}")
        for spec in lesson.specs():
            brain.meet(spec)
        result = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            if lesson.kind == "exam":
                self.say("No teaching today. Show me what you can do.")
            elif lesson.number == 4:
                self.teach_names(lesson)
            elif lesson.number == 6:
                self.teach_real_data(lesson)
            elif lesson.number == 8:
                self.teach_owing(lesson)
            elif lesson.number == 9:
                self.teach_sharing(lesson)
            elif lesson.number == 11:
                self.teach_wheel(lesson)
            elif lesson.number == 15:
                self.teach_diagonal(lesson)
            elif lesson.number == 19:
                self.teach_handling(lesson)
            elif lesson.number == 26:
                self.teach_microscope(lesson)
            elif lesson.number == 29:
                self.teach_falling(lesson)
            elif lesson.number == 30:
                self.teach_swinging(lesson)
            elif lesson.number == 31:
                self.teach_words(lesson)
            elif lesson.number == 32:
                self.teach_events(lesson)
            elif lesson.number == 33:
                self.teach_grammar(lesson)
            elif lesson.number == 13 and attempt == 1:
                free_play(brain, lesson, lesson.budget)
                bind_operation(brain, "power", lesson.power_demos())
                self.say("I grew cells and said '3 power 2 equals 9' and so on.")
            elif attempt == 1:
                free_play(brain, lesson, lesson.budget)
            else:
                self.say("You passed nothing new; let me show you some harder cases.")
                guided(brain, lesson, 40, wide=True)
                free_play(brain, lesson, lesson.budget, wide=True)
            result = EXAMS[number](brain)
            result["attempt"] = attempt
            self.say(f"Exam for lesson {number}, attempt {attempt}: "
                     f"{'passed' if result['passed'] else 'not yet'}")
            if result["passed"]:
                self.name_concepts(number)
                break
            if lesson.kind in ("guided", "exam"):
                break
        self.results[number] = result
        return result

    # ----------------------------------------------------------- lesson 4
    def teach_names(self, lesson):
        brain = self.brain
        for token, n in lesson.naming_scenes():
            bind_number(brain, token, lesson.show_pile(n))
        self.say("I pointed at piles and said their names: marks 0-9 and words zero-ten.")
        demos, equals = lesson.operation_demos(brain)
        for word, ds in demos.items():
            bind_operation(brain, word, ds)
        for word in ("equals", "="):
            bind_relation(brain, word, equals)
        self.say("I acted out 'plus', 'minus', 'times' with real piles and said the words.")
        lesson.brain_vocab = brain.vocab
        free_play(brain, lesson, lesson.budget)
        self.say("I wrote two-mark numerals next to piles of 10-99 things.")

    # ----------------------------------------------------------- lesson 6
    def teach_real_data(self, lesson):
        brain = self.brain
        for row in RealData.bodies(RealData.PLANETS_TRAIN):
            brain.experience("orbit", {"r": row["r"], "system": row["system"]}, row["T"])
        self.say("I showed real distances and orbital periods of six planets.")
        train, _ = RealData.gas_split()
        for row in train:
            brain.experience("gas", {"V": row["V"]}, row["P"])
        self.say("I showed Boyle's 1662 measurements for the larger air volumes.")

    # ----------------------------------------------------------- lesson 8
    def teach_owing(self, lesson):
        brain = self.brain
        lesson.brain = brain
        self.say("Here is a purse. You can earn coins and spend coins. If you spend with "
                 "an empty purse, the shop gives you an IOU note. Play.")
        free_play(brain, lesson, lesson.budget)
        if lesson.LINE not in brain.inventions:
            self.say("You haven't found anything new about the purse. The lesson stops here.")
            return
        self.say("You say some purses are 'below zero'. Let's buy and sell with that idea.")
        for spec in lesson.deal_specs():
            brain.meet(spec)
        free_play(brain, lesson, lesson.budget, names=[s.name for s in lesson.deal_specs()])
        marks, words = [], []
        for mark, spoken, purse in lesson.below_zero_names():
            lesson.world.set_purse(*purse)
            pos = lesson.perceive()
            marks.append((mark, pos))
            words.append((spoken, pos))
        bind_prefix(brain, marks)
        bind_prefix(brain, words)
        self.say("People write your below-zero places as -1, -2, -3 and say 'negative one, "
                 "negative two'.")
        for word, ds in lesson.demos().items():
            bind_operation(brain, word, ds)
        self.say("I bought and sold things with you and said 'minus' and 'plus' out loud.")

    # ----------------------------------------------------------- lesson 9
    def teach_sharing(self, lesson):
        from ..brain import amounts
        brain = self.brain
        self.say("Here are cakes, a knife that cuts into equal pieces, and a balance. Play.")
        free_play(brain, lesson, lesson.budget)
        if not amounts.invented(brain):
            self.say("You haven't found anything new about cakes. The lesson stops here.")
            return
        amounts.bind_separator(brain, lesson.notation())
        self.say("People write 'so many pieces of a cake cut into so many' like 2/3.")
        shares = lesson.sharings()
        for word in ("divided", "÷"):
            amounts.bind_division(brain, word, shares)
        self.say("I shared cakes fairly between people and said 'divided' out loud.")

    # ----------------------------------------------------------- lesson 11
    def teach_wheel(self, lesson):
        brain = self.brain
        self.say("Here is a wheel with a pointer. You can make it tick. Play.")
        free_play(brain, lesson, lesson.budget)
        if lesson.CYCLE not in brain.inventions:
            self.say("You haven't found anything new about the wheel. The lesson stops here.")
            return
        self.say("Now spin it as many ticks as you like and watch where it stops.")
        for spec in lesson.spin_specs():
            brain.meet(spec)
        free_play(brain, lesson, lesson.budget, names=["spin"])
        bind_operation(brain, "after", lesson.after_demos())
        self.say("I spun the wheel and said '3 after 5 equals 2' and so on.")

    # ----------------------------------------------------------- lesson 15
    def teach_diagonal(self, lesson):
        from ..brain import amounts, gaps
        from ..brain.perception import count
        brain = self.brain
        self.say("Here are square tiles. Build squares and count the tiles in them.")
        free_play(brain, lesson, lesson.budget)
        if not brain.trusts("square"):
            self.say("You haven't found how many tiles a square takes. The lesson stops here.")
            return
        halves = count(lesson.world.square_on_a_diagonal())
        area = amounts.simplest(brain, (halves, count(["half", "half"])))
        brain.note("reflect", f"the square built on a tile's diagonal is covered by {halves} "
                              f"half-tiles: {amounts.show(brain, area)} tiles")
        if not gaps.invented(brain):
            self.say("You don't have numbers for this yet. The lesson stops here.")
            return
        # a square is a square: the diagonal is the side whose square holds `area` tiles
        gap = gaps.Gap("square", "xy", (0, 1), area, True, one_input=True)
        if gaps.pin(brain, gap, 10) is None:
            self.say("You can't pin that length down. The lesson stops here.")
            return
        brain.quantities["diagonal"] = gap.to_json()
        brain.note("reflect", f"a square is a square: my 'square' law holds for the square on "
                              f"the diagonal too, so the diagonal is the side whose square holds "
                              f"{amounts.show(brain, area)} tiles: a number in a gap of my line, "
                              f"{gaps.describe(brain, gap)[1]}")
        self.say("Now measure the diagonal with rulers. Say what each will read first.")
        brain.meet(lesson.ruler_spec())
        for marks in (1, 2, 3, 5, 7, 10, 12, 20, 30):
            inputs, reading = lesson.ruler(marks)
            brain.experience("ruler", inputs, reading)

    # ----------------------------------------------------------- lesson 19
    def teach_handling(self, lesson):
        from ..senses.eyes import Eyes
        brain = self.brain
        self.say("Pick these things up and put them down. Your hands will tell you where "
                 "they are; watch at the same time.")
        pics, touches = zip(*lesson.handling())
        eyes = Eyes(seed=lesson.seed)
        losses = eyes.learn(list(pics), list(touches), seed=lesson.seed)
        brain.eyes = eyes
        brain.inventions["eyes"] = {
            "shape": "learned perception", "primitives": [], "lesson": brain.lesson,
            "story": (f"I handled things {len(pics)} times while watching. My hands said where "
                      f"each thing was; I trained a small network of 3 layers of 3x3 filters "
                      f"to light up where my hands felt something (error per picture fell from "
                      f"{losses[0]:.1f} to {losses[-1]:.1f}). A spot must be at least "
                      f"{eyes.threshold:.2f} strong to be a thing: that threshold matched my "
                      f"hands best. From now on I see without touching.")}
        brain.note("invent", brain.inventions["eyes"]["story"])
        self.say("Now put your hands behind your back. Only look.")

    # ----------------------------------------------------------- lesson 26
    def teach_microscope(self, lesson, adapt=True):
        from ..env import realvideo
        from ..senses import real, track
        from ..senses.world import Trays
        brain = self.brain
        try:
            film = realvideo.frames()
        except realvideo.Unavailable as e:
            self.say(f"I couldn't get the film ({e}). The lesson stops here.")
            return
        label = realvideo.label()
        fps, ppm = label["fps"], label["pixels_per_micron"]
        learn = film[:lesson.LEARN]
        self.say(f"This is a real film from a laboratory microscope: spheres in water. The "
                 f"label says {fps} pictures a second and {ppm} pixels per micron. Watch the "
                 f"first {len(learn)} pictures.")
        ch, frac, name = real.choose_channel(brain.eyes, learn[:30])
        brain.note("reflect", f"through my retina's {name} channel, {frac:.0%} of what I see "
                              f"lasts from picture to picture; the other channel shows things "
                              f"that come and go. Real things last, so I'll look with {name}")
        dets, tracks, shift = real.follow(brain.eyes, learn, ch)
        before = sum(len(t) for t in tracks) / max(1, sum(len(d) for d in dets))
        if adapt:
            trays = Trays(lesson.seed)
            # its old experience, as it was: things handled in varied sizes and spacings
            replay = [trays.handle(int(trays.rng.integers(0, 20)), varied=True)
                      for _ in range(240)]
            # eyes adapted to the microscope, kept apart: learning a new instrument must not
            # spoil how it sees everything else
            brain.microscope_eyes = real.self_teach(brain.eyes, learn, ch, tracks, replay,
                                                    seed=lesson.seed)
            dets, tracks, shift = real.follow(brain.microscope_eyes, learn, ch)
            after = sum(len(t) for t in tracks) / max(1, sum(len(d) for d in dets))
            brain.note("invent", f"I trained my eyes on these real pictures with no one telling "
                                 f"me what is there: what lasted at least 25 pictures I took as "
                                 f"a real thing, everything else as nothing (and I kept looking "
                                 f"at my old toy scenes so I don't forget them). Before, "
                                 f"{before:.0%} of what I saw lasted; now {after:.0%}.")
        # how far things get in a while: my own careful measure of the jiggling
        half = [tracks[0::2], tracks[1::2]]
        a, _ = track.spread(half[0], 10, shift, 1 / ppm)
        b, _ = track.spread(half[1], 10, shift, 1 / ppm)
        precision = max(0.01, round(abs(a - b) / ((a + b) / 2), 3))
        brain.memory.specs["jiggle"].precision = precision
        brain.note("reflect", f"I followed {len(tracks)} spheres for at least 25 pictures each, "
                              f"after taking out how the whole view drifted. Two halves of them "
                              f"disagree by {precision:.1%} about how far spheres get: that's "
                              f"how precise this measuring is")
        for lag in lesson.LAGS:
            s, n = track.spread(tracks, lag, shift, 1 / ppm)
            brain.experience("jiggle", {"tau": lag / fps}, s)
        # and one sphere at a time: can its path be predicted?
        for i, t in enumerate(sorted(tracks, key=len, reverse=True)[:8]):
            for f in sorted(t):
                brain.experience("one_sphere", {"frame": f, "sphere": f"Sphere{i + 1}"},
                                 (t[f][0] - shift[f][0]) / ppm)
        law = brain.qlaws.get("jiggle")
        brain.inventions["microscope"] = {
            "shape": "the real world", "primitives": [], "lesson": brain.lesson,
            "channel": ch, "precision": precision,
            "story": (f"From a real microscope film: each sphere's path is unpredictable "
                      f"(nothing I can express explains one), but all together "
                      + (f"{law.formula()} stays the same, {law.constant:.4g}: the spread "
                         f"squared grows in proportion to the time." if law else
                         "I found no law.")
                      )}
        brain.note("invent", brain.inventions["microscope"]["story"])

    # ----------------------------------------------------------- lesson 29
    def teach_falling(self, lesson):
        from ..env import footage
        from ..senses import motion
        brain = self.brain
        watched = {}
        for name in lesson.FILMS:
            try:
                pics = footage.frames(name)
            except footage.Unavailable as e:
                self.say(f"I couldn't get the film {name} ({e}).")
                continue
            lab = footage.label(name)
            halves = ", each frame taken as two half-pictures" if lab["interlaced"] else ""
            self.say(f"A real film from a physics lab: {name}. The label says {lab['fps']} "
                     f"pictures a second{halves}; the stick in view is "
                     f"{lab['pixels_per_metre']} pixels to the metre ({lab['scale_from']}).")
            track, per, ch, tracks = motion.watch(brain.eyes, pics, lab["interlaced"])
            if track is None:
                brain.note("reflect", f"{name}: I can't follow anything moving in this film")
                continue
            free = motion.alone(track, tracks, pics[0].shape)
            if len(free) < 6:
                brain.note("reflect", f"{name}: I followed something, but it was never on its "
                                      f"own for long enough to measure")
                continue
            rate = lab["fps"] * per
            watched[name] = (free, rate, lab["pixels_per_metre"])
            brain.note("reflect", f"{name}: comparing each picture with how the room usually "
                                  f"looks, through my {ch} channel, one thing moved further "
                                  f"than anything else: I followed it through {len(track)} "
                                  f"pictures, {len(free)} of them with nothing touching it "
                                  f"and all of it in view")
        if not watched:
            self.say("No film could be watched. The lesson stops here.")
            return
        # how precise is this measuring? the films compared on how much faster the ball
        # goes after the same short while (no law needed for that)
        cmp = []
        for free, rate, ppm in watched.values():
            dv, _ = motion.speed_change(free, round(lesson.COMPARE * rate), rate, ppm)
            if dv is not None:
                cmp.append(dv)
        precision = lesson.precision
        if len(cmp) >= 2:
            precision = max(0.01, round((max(cmp) - min(cmp)) / (2 * abs(sum(cmp) / len(cmp))),
                                        3))
        brain.memory.specs["fall"].precision = precision
        brain.note("reflect", f"after {lesson.COMPARE:.3g} s the ball goes faster by about the "
                              f"same amount in every film, give or take {precision:.1%}: that's "
                              f"how precise this measuring is")
        for name, (free, rate, ppm) in watched.items():
            span = max(free) - min(free) + 1
            for lag in range(1, span // 2 + 1):
                dv, n = motion.speed_change(free, lag, rate, ppm)
                if dv is not None:
                    brain.experience("fall", {"tau": lag / rate, "film": name}, dv)
        law = brain.qlaws.get("fall")
        steady = law is not None and law.powers in ({"dv": 1, "tau": -1}, {"dv": -1, "tau": 1})
        films = {}
        if steady:
            # its law says speed changes steadily: so each film's rate of change, and how
            # sure it is of it, from the line through all its speeds
            for name, (free, rate, ppm) in watched.items():
                g, se = motion.steady_change(free, rate, ppm)
                films[name] = {"g": g, "fit_error": se, "pictures": len(free), "rate": rate}
        brain.inventions["falling"] = {
            "shape": "the real world", "primitives": [], "lesson": brain.lesson,
            "precision": precision, "films": films, "watched": sorted(watched),
            "story": (f"From real films of a falling ball: " +
                      (f"{law.formula()} stays the same, {law.constant:.4g} m/s²: the change "
                       f"of speed grows in proportion to the time, whether the ball was "
                       f"dropped or thrown up or across." if steady else
                       f"I found no steady law ({law.formula() if law else 'nothing'})."))}
        brain.note("invent", brain.inventions["falling"]["story"])

    # ----------------------------------------------------------- lesson 30
    def teach_swinging(self, lesson):
        from ..env import footage
        from ..senses import motion
        brain = self.brain
        timed = {}
        for name in lesson.FILMS:
            try:
                pics = footage.frames(name)
            except footage.Unavailable as e:
                self.say(f"I couldn't get the film {name} ({e}).")
                continue
            lab = footage.label(name)
            self.say(f"A real film of a pendulum: {name}. The label says {lab['fps']} pictures "
                     f"a second, and the string is {lab['length_m']} m long "
                     f"({lab['scale_from']}).")
            _, _, ch, tracks = motion.watch(brain.eyes, pics, lab["interlaced"])
            track = motion.whole_mover(tracks)
            s = motion.swing(track, lab["fps"]) if track else None
            if s is None:
                brain.note("reflect", f"{name}: I couldn't follow anything swinging there and back")
                continue
            timed[name] = {"length_m": lab["length_m"], "period": s["period"],
                           "error": s["error"], "angle_deg": math.degrees(s["angle"]),
                           "half_swings": len(s["half_swings"]), "rate": lab["fps"]}
            brain.note("reflect", f"{name}: through my {ch} channel I followed the bob through "
                                  f"{len(track)} pictures and timed {len(s['half_swings'])} "
                                  f"half swings: one swing there and back takes "
                                  f"{s['period']:.3f} ± {s['error']:.3f} s")
        if not timed:
            self.say("No film could be timed. The lesson stops here.")
            return
        # its own timings say how precise this measuring is: the worst film's error
        precision = max(lesson.precision, round(max(t["error"] / t["period"]
                                                    for t in timed.values()), 3))
        brain.memory.specs["swing"].precision = precision
        brain.note("reflect", f"my timings are good to about {precision:.1%}")
        for name, t in sorted(timed.items(), key=lambda kv: kv[1]["length_m"]):
            brain.experience("swing", {"L": t["length_m"], "film": name}, t["period"])
        law = brain.qlaws.get("swing")
        root = law is not None and law.powers in ({"T": 2, "L": -1}, {"T": -2, "L": 1})
        brain.inventions["swinging"] = {
            "shape": "the real world", "primitives": [], "lesson": brain.lesson,
            "precision": precision, "films": timed,
            "story": (f"From real films of pendulums: " +
                      (f"{law.formula()} stays the same, {law.constant:.4g}: the time of a "
                       f"swing grows as the square root of the length of the string."
                       if root else f"I found no law of the square root "
                                    f"({law.formula() if law else 'nothing'})."))}
        brain.note("invent", brain.inventions["swinging"]["story"])

    # ----------------------------------------------------------- lesson 31
    def teach_words(self, lesson):
        from ..brain import categories
        from ..brain.language import (describe_meaning, heard_as_kinds, learn_lexicon,
                                      lexicon_bits)
        from ..senses.things import look_at_table
        brain = self.brain
        if brain.eyes is None:
            self.say("You have no eyes yet. The lesson stops here.")
            return
        self.say("Here is a table with things on it. Just look, as long as you like.")
        seen = [t for look in lesson.tables() for t in look_at_table(brain.eyes, look)]
        found = categories.discover(seen, lesson.MEASURES)
        brain.categories = found
        grouped = {m: len(c["groups"]) for m, c in found.items() if len(c["groups"]) > 1}
        flat = [m for m, c in found.items() if len(c["groups"]) == 1]
        brain.inventions["kinds of thing"] = {
            "shape": "categories", "primitives": [], "lesson": brain.lesson,
            "groups": grouped,
            "story": (f"I looked at {len(seen)} things on {lesson.LOOKS} tables and measured "
                      f"each one. " + "; ".join(
                          f"{'Their' if i == 0 else 'their'} {m} falls into {k} separate "
                          f"groups ({found[m]['bits'][0]:.0f} bits to describe all of them as "
                          f"one spread, {found[m]['bits'][1]:.0f} as groups)"
                          for i, (m, k) in enumerate(sorted(grouped.items())))
                      + f". Where they are ({', '.join(flat)}) doesn't group: a boundary "
                        f"there would not pay for itself. So things come in kinds.")}
        brain.note("invent", brain.inventions["kinds of thing"]["story"])
        self.say("Now I'll talk about the things on the table, one at a time.")
        for said, look, _, _ in lesson.talks():
            brain.heard.append({"said": said, "things": look_at_table(brain.eyes, look)})
        heard = heard_as_kinds(brain)
        lexicon, rivals = learn_lexicon(heard, found, rivals=True)
        for w, meaning in sorted(lexicon.items()):
            if w in brain.vocab and brain.vocab[w][0] != "look":
                continue                    # a word it already has another meaning for
            brain.bind(w, ("look", [list(p) for p in meaning]))
            others = sorted({r[w] for r in rivals if r[w] != meaning})
            brain.note("word", f"'{w}' means {describe_meaning(brain, meaning)}"
                       + (" (not sure yet: it could also mean "
                          + "; or ".join(describe_meaning(brain, r) for r in others) + ")"
                          if others else ""))
        brain.rival_lexicons = [{w: [list(p) for p in m] for w, m in sorted(r.items())
                                 if m != lexicon[w]} for r in rivals]
        brain.note("reflect", f"the shortest account of the {len(heard)} sentences I heard "
                              f"takes {lexicon_bits(heard, found, lexicon):.0f} bits: what each "
                              f"word means, and nothing more is needed to tell which thing was "
                              f"meant")

    # ----------------------------------------------------------- lesson 32
    def teach_events(self, lesson):
        from ..brain import events
        from ..brain.language import (comparing, learn_lexicon,
                                      learn_relations)
        brain = self.brain
        if brain.eyes is None:
            self.say("You have no eyes yet. The lesson stops here.")
            return
        self.say("Now films of the same things. Watch; I'll say what happens.")
        heard = []
        for said, watch, _, _ in lesson.event_talks():
            film = events.watch(brain, watch())
            film["said"] = said
            brain.films.append(film)
            heard.append((said.split(), [events.kinds_of_thing(brain, t)
                                         for t in film["things"]]))
        found = dict(brain.categories)
        found.update(events.categories(brain))
        known = {w: m[1] for w, m in brain.vocab.items() if m[0] == "look"}
        lexicon, rivals = learn_lexicon(heard, found, rivals=True, known=known)
        kinds = events.motion_kinds(brain)
        new = sorted(w for w in lexicon if w not in known)
        brain.event_words = new             # a word whose meaning it didn't find: it says so
        for w in new:
            if w in brain.vocab:
                continue                    # a word it already has another meaning for
            brain.bind(w, ("look", [list(p) for p in lexicon[w]]))
            others = sorted({r[w] for r in rivals if r[w] != lexicon[w]})
            brain.note("word", f"'{w}' means {self._motion_meaning(lexicon[w], kinds)}"
                       + (" (not sure yet: it could also mean " + "; or ".join(
                           self._motion_meaning(r, kinds) for r in others) + ")"
                          if others else ""))
        brain.rival_lexicons = brain.rival_lexicons + [
            {w: [list(p) for p in r[w]] for w in new if r[w] != lexicon[w]}
            for r in rivals if any(r[w] != lexicon[w] for w in new)]
        brain.inventions["words for events"] = {
            "shape": "words", "primitives": [], "lesson": brain.lesson,
            "words": {w: [list(p) for p in lexicon[w]] for w in brain.event_words if lexicon[w]},
            "story": "Each word for what happens is the kind of motion present every time "
                     "it was said about a thing: " + "; ".join(
                         f"'{w}': {self._motion_meaning(lexicon[w], kinds)}"
                         for w in brain.event_words if lexicon[w])}
        brain.note("invent", brain.inventions["words for events"]["story"])

        self.say("Now I'll compare things in the films.")
        compared = []
        for said, watch, _, _, _, _ in lesson.relation_talks():
            film = events.watch(brain, watch())
            film["said"] = said
            brain.films.append(film)
            got = comparing(brain, said, film)
            if got is not None:
                compared.append((got[0], film, got[1], got[2]))
        best, rivals = learn_relations(compared, rivals=True)
        for w, o in sorted(best.items()):
            meaning = ("order", list(o) if o else None)
            if w in brain.vocab and brain.vocab[w][0] != "order":
                brain.senses[w] = list(meaning)  # lesson 4's 'after' keeps its meaning
            else:
                brain.bind(w, meaning)
            others = sorted({str(r[w]) for r in rivals if r[w] != o})
            brain.note("word", f"'{w}' " + (f"says the first has {'more' if o[1] == '>' else 'less'}"
                                             f" {o[0]} than the second" if o else
                                             "says nothing I can check")
                       + (f" (not sure yet: it could also be {', '.join(others)})"
                          if others else ""))
        brain.rival_relations = [{w: (list(o) if o else None) for w, o in sorted(r.items())
                                  if o != best[w]} for r in rivals]
        brain.inventions["words for comparing"] = {
            "shape": "words", "primitives": [], "lesson": brain.lesson,
            "words": {w: (list(o) if o else None) for w, o in sorted(best.items())},
            "story": "Each comparing word is the quantity I measure, and which way round, "
                     "that holds every time it is said: " + "; ".join(
                         f"'{w}': the first has {'more' if o[1] == '>' else 'less'} {o[0]}"
                         for w, o in sorted(best.items()) if o)
                     + ". I weigh things by my law that m·v adds up to the same before and "
                       "after a knock."}
        brain.note("invent", brain.inventions["words for comparing"]["story"])

    # ----------------------------------------------------------- lesson 33
    def teach_grammar(self, lesson):
        from ..brain import grammar
        brain = self.brain
        if brain.eyes is None:
            self.say("You have no eyes yet. The lesson stops here.")
            return
        self.say("Back to the tables. I'll say longer things now.")
        heard = []
        for said, look, _, _, _ in lesson.talks():
            seen = grammar.see_table(brain, look)
            brain.tables.append({"said": said, "things": seen})
            heard.append(grammar.heard_as(brain, said, seen))
        known = grammar.known_kinds(brain)
        lexicon, rivals = grammar.learn_grammar(heard, brain.categories, known=known,
                                                rivals=True)
        brain.grammar = {w: grammar.to_json(o) for w, o in lexicon.items()}
        brain.rival_grammars = [{w: grammar.to_json(o) for w, o in r.items() if o != lexicon[w]}
                                for r in rivals]
        badly = grammar.doubtful_words(heard, lexicon)
        unsteady = grammar.unsteady_words(heard, brain.categories, known=known)
        brain.grammar_doubts = sorted(set(badly) | set(unsteady))
        for w in badly:
            brain.note("word", f"I'm not sure what '{w}' does: the sentences with it often "
                               f"fit no reading")
        for w in unsteady:
            brain.note("word", f"I'm not sure what '{w}' does: I'd find it differently from "
                               f"each half of what I heard")
        names = grammar.kind_names(brain)
        for w, o in sorted(lexicon.items()):
            if w not in brain.vocab:
                brain.bind(w, ("grammar", grammar.to_json(o)))
            others = sorted({r[w] for r in rivals if r[w] != o})
            brain.note("word", f"'{w}' {grammar.describe_option(o, names)}"
                       + (" (not sure yet: it could also be that it "
                          + "; or ".join(grammar.describe_option(r, names) for r in others)
                          + ")" if others else ""))
        kinds = sorted({o[0] for o in lexicon.values() if o[0] != "nothing"})
        brain.inventions["how words combine"] = {
            "shape": "grammar", "primitives": [], "lesson": brain.lesson,
            "grammar": dict(sorted(brain.grammar.items())),
            "story": ("Each word does one of a few things to the phrase next to it, and the "
                      "words that do the same thing combine the same way: "
                      + "; ".join(f"'{w}' {grammar.describe_option(o, names)}"
                                  for w, o in sorted(lexicon.items()) if o[0] != "nothing")
                      + ". " + ", ".join(f"'{w}'" for w, o in sorted(lexicon.items())
                                          if o[0] == "nothing")
                      + " mean nothing by themselves. A phrase can sit inside another of "
                        "the same kind, as deep as you like, and phrases can be joined "
                        f"({len(kinds)} kinds of word in all).")}
        brain.note("invent", brain.inventions["how words combine"]["story"])

    @staticmethod
    def _motion_meaning(meaning, kinds):
        if not meaning:
            return "nothing: it fits every thing"
        parts = []
        for m, g in meaning:
            if m in ("across", "updown"):
                way = "across" if m == "across" else "up and down"
                name, _, words = kinds[g]
                parts.append(f"its move {way} follows '{name}' ({words})")
            elif m == "turns back":
                parts.append("it comes back the way it went" if g else
                             "it never comes back the way it went")
            else:
                parts.append(f"its {m} is in my group {g + 1}")
        return "things where " + " and ".join(parts)

    # ----------------------------------------------------------- naming
    CONCEPT_NAMES = {
        0: {"peekaboo": "object permanence"},
        1: {"pair_off": "same number (one-to-one correspondence)"},
        2: {"merge": "addition", "take_away": "subtraction"},
        3: {"groups": "multiplication"},
        4: {"numeral": "place value"},
        5: {"push": "Newton's second law", "stretch": "stiffness (Hooke's law)",
            "collide": "conservation of momentum"},
        6: {"orbit": "Kepler's third law", "gas": "Boyle's law"},
        7: {"lab_push": "Newton's second law (measured with noise)",
            "lab_stretch": "stiffness (measured with noise)"},
        8: {"line:earn/spend": "negative numbers (the integers)"},
        9: {"finer:cake_balance": "fractions (the rational numbers)"},
        11: {"cycle:tick": "clock numbers (arithmetic modulo 6)"},
        12: {"hidden:roll": "energy (height + speed²/2g, per unit of weight)",
             "roll": "conservation of energy"},
        13: {"repeated_groups": "powers (exponentiation)", "grow": "exponential growth"},
        14: {"hidden:bounce": "energy: gravitational + kinetic + elastic (spring)",
             "bounce": "conservation of energy with a spring"},
        17: {"why:coil_stretch": "a law about a law: stiffness is inversely proportional "
                                 "to the number of coils"},
        19: {"eyes": "vision (a learned convolutional neural network)"},
        20: {"see_merge": "addition, seen", "see_take": "subtraction, seen"},
        21: {"see_push": "Newton's second law, seen on video",
             "see_stretch": "stiffness (Hooke's law), seen on video",
             "see_roll": "conservation of energy, seen on video"},
        22: {"kind:cool": "exponential decay toward equilibrium (Newton's law of cooling)",
             "cool": "Newton's law of cooling"},
        23: {"kind:hang": "a linear relationship (a constant rate of change)",
             "bounces": "coefficient of restitution (geometric decay)",
             "charge": "exponential approach to a limit", "hang": "Hooke's law with an "
             "unstretched length", "burn": "constant rate"},
        24: {"slide": "sliding friction (stopping distance ∝ speed²)"},
        26: {"jiggle": "Brownian motion: Einstein's law (mean squared displacement = 4·D·t)"},
        29: {"fall": "free fall: the acceleration of gravity, g"},
        30: {"swing": "the period of a pendulum (T = 2π√(L/g))"},
        31: {"kinds of thing": "categories: colours, sizes and shapes"},
        32: {"words for events": "verbs, bound to kinds of motion",
             "words for comparing": "comparatives and before/after, bound to measured "
                                    "quantities (mass through conservation of momentum)"},
        33: {"how words combine": "a categorial grammar: word classes, word order, "
                                  "recursion (nesting) and coordination"},
        15: {"gaps": "irrational numbers (the real numbers)",
             "diagonal": "the square root of 2 (√2), a tile's diagonal"},
    }

    def name_concepts(self, number):
        """Only called after the exam is passed: understanding first, names second."""
        for concept, word in self.CONCEPT_NAMES.get(number, {}).items():
            self.brain.names[concept] = word
            self.say(f"What you found in '{concept}' is what people call {word}.")

    def run_all(self, upto=None):
        if upto is None:
            upto = max(self.lessons)
        for n in sorted(self.lessons):
            if n <= upto:
                self.run(n)
        return self.results
