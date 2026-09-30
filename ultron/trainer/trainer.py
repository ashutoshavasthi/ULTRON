"""The Trainer: runs the curriculum, gates each lesson on a held-out exam, and
names concepts only *after* Ultron has shown it understands them.

The Trainer may look at the world's ground truth to grade answers. It never
passes a law, formula or answer into the brain.
"""

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
        9: {"amounts:cake": "fractions (the rational numbers)"},
        11: {"cycle:tick": "clock numbers (arithmetic modulo 6)"},
    }

    def name_concepts(self, number):
        """Only called after the exam is passed: understanding first, names second."""
        for concept, word in self.CONCEPT_NAMES.get(number, {}).items():
            self.brain.names[concept] = word
            self.say(f"What you found in '{concept}' is what people call {word}.")

    def run_all(self, upto=11):
        for n in range(upto + 1):
            self.run(n)
        return self.results
