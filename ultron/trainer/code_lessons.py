"""Code lessons (numbered from 100): programs are the world (docs/STAGE_CODE_PLAN.md).

Lesson 100 (C1): reading Engc expressions. The Trainer runs one-line programs and
Ultron watches what they print; then Ultron writes and runs programs of its own, to
pin down what each word means and how words group. It never sees Engc's compiler or
grammar. At most RUNS programs are run in all (the Trainer's and its own).
"""

import random

from ..code.reading import Reader
from . import engc_programs as P
from .lessons import Lesson

WORDS = ["PLUS", "MINUS", "TIMES", "MODULO", "RAISED TO", "IS GREATER THAN", "IS LESS THAN",
         "IS EQUAL TO", "IS AT LEAST", "IS AT MOST", "IS NOT"]
SYMBOLS = ["+", "-", "*", "%", "**", ">", "<", "==", ">=", "<=", "!="]
UNARY = ["MINUS", "-"]
LOGIC = [("AND", 2), ("OR", 2), ("NOT", 1)]


class ReadingEngc(Lesson):
    number, title = 100, "Reading Engc: what expressions mean"
    goal = ("The Trainer runs one-line Engc programs (PRINT <expression> .) and Ultron "
            "watches what they print. Can it find what each word and mark means, as one of "
            "its own laws, and how words group, from at most 400 runs, then say what "
            "expressions far longer than any it saw will print, without running them?")
    kind = "guided"
    RUNS = 400
    SHOWN = 3            # the Trainer's demonstrations of each word
    PER_WORD = 14        # runs Ultron may spend on one word (stepping may need more)
    TWO_OPS = 20         # the Trainer's two-operator programs
    BRACKETS = 6         # the Trainer's programs with brackets

    def __init__(self, seed=0):
        super().__init__(seed)
        self.rng = random.Random(seed)

    def teach(self, trainer):
        from ..code import sandbox
        brain = trainer.brain
        rng = self.rng
        reader = Reader(brain, {"seed": self.seed})
        reader.world = _world(sandbox)

        def show(text, printed):
            reader.watch(text, printed)

        trainer.say("These are programs in a language called Engc. I'll run some and you "
                    "watch what each one prints. Later you can write and run your own.")
        first = [P.one_op(rng, WORDS[0]) for _ in range(self.SHOWN)]
        reader.find_frame([t for t, _ in first])
        # words, then their symbol twins, then a word before a number
        for i, words in enumerate(WORDS + SYMBOLS):
            self._word(reader, rng, words, 2, trainer, first if i == 0 else None)
        for words in UNARY:
            self._word(reader, rng, words, 1, trainer)
        reader.decide_symbols()
        trainer.say("Now words that join whole statements.")
        for words, arity in LOGIC:
            self._word(reader, rng, words, arity, trainer)
        trainer.say("Now programs with two operators.")
        for _ in range(self.TWO_OPS):
            show(*P.program(rng, 2, 20))
        reader.learn_grammar(self._left(reader, 60))
        trainer.say("Now programs with brackets.")
        for _ in range(self.BRACKETS):
            show(*P.bracketed(rng))
        reader.learn_marks()
        reader.learn_grammar(self._left(reader, 0))
        brain.code = reader.to_json()
        trainer.say(f"That's all: {reader.total_runs} programs run "
                    f"({reader.stats.get('trainer', 0)} by me, {reader.stats.get('own', 0)} "
                    f"by you).")

    def _left(self, reader, keep):
        return max(0, self.RUNS - reader.total_runs - keep)

    def _word(self, reader, rng, words, arity, trainer, shown=None):
        demos = []
        for i in range(self.SHOWN):
            text, printed = shown[i] if shown else P.one_op(rng, words, unary=arity == 1)
            reader.watch(text, printed)
            got = reader.demo_from(text, printed)
            if got is not None:
                demos.append((got[2], got[3]))
        if not demos:
            reader.note("stuck", f"I couldn't tell what '{words}' joins")
            return
        budget = min(self.PER_WORD, self._left(reader, 120))
        reader.study(tuple(words.split()), arity, demos, budget)


class ReadingStatements(Lesson):
    number, title = 101, "Reading Engc: what statements do"
    goal = ("The Trainer runs Engc programs with statements (names, tests, loops, rows, "
            "routines that call themselves) and Ultron watches each one run line by line. "
            "Can it find what every kind of line does to memory, from at most 1,000 runs, "
            "then say what longer, more deeply nested programs print, without running them?")
    kind = "guided"
    RUNS = 1000
    ROUNDS = 2           # rounds of the Trainer's short first programs
    MIXED = 60           # then programs mixing everything
    OWN = 40             # runs Ultron may spend on its own experiments at a time
    CONFIRM = 10         # fresh programs predicted right in a row before it is trusted

    def __init__(self, seed=0):
        super().__init__(seed)
        self.rng = random.Random(seed)

    def teach(self, trainer):
        from ..code import sandbox
        from ..code.reading import Reader
        from ..code.statements import Machine
        from . import engc_statements as S
        brain = trainer.brain
        rng = self.rng
        reader = Reader(brain, brain.code)
        m = Machine(brain, reader, (brain.code or {}).get("statements"))
        m.world = sandbox.trace

        def show(text):
            m.watch(text, sandbox.trace(text))

        trainer.say("Now programs with many lines. I'll run each one and you can watch it "
                    "line by line: which line runs next, and what every name holds.")
        for _ in range(self.ROUNDS):
            for text, _ in S.first_programs(rng):
                show(text)
        for _ in range(self.MIXED):
            show(S.program(rng, S.LESSON)[0])
        m.learn()
        m.experiment(self.OWN)
        m.learn()
        trainer.say("Now tell me what each new program prints before I run it.")
        streak = 0
        while streak < self.CONFIRM and m.total_runs < self.RUNS:
            text, printed = S.program(rng, S.LESSON)
            guess = m.predict(text)
            show(text)
            if guess == printed:
                streak += 1
                continue
            streak = 0
            m.note("code", "I didn't know what that program prints" if guess is None else
                           f"I expected {guess[:4]}, it printed {printed[:4]}: I think again")
            m.learn()
            if m.wanting:
                m.experiment(min(self.OWN, self.RUNS - m.total_runs))
                m.learn()
        if streak >= self.CONFIRM:
            m.note("code", f"{self.CONFIRM} new programs in a row predicted right")
        code = dict(brain.code or {})
        code["statements"] = m.to_json()
        brain.code = code
        trainer.say(f"That's all: {m.total_runs} programs run "
                    f"({m.stats.get('trainer', 0)} by me, {m.stats.get('own', 0)} by you).")


class SecondLanguage(Lesson):
    """C3: a language it has never seen, learned to the level of lessons 100 and 101
    with at most a third of the runs Engc took, by carrying over what it knows."""
    kind = "guided"
    RUNS = 141           # one third of the 425 runs Engc took (328 + 97)
    SHOWN = 1            # the Trainer's demonstration of each word
    PER_WORD = 6
    TWO_OPS = 6
    BRACKETS = 3
    GRAMMAR_CONFIRM = 5
    MIXED = 20
    OWN = 10
    CONFIRM = 10
    store = None

    def __init__(self, seed=0):
        super().__init__(seed)
        self.rng = random.Random(seed)

    def language(self):
        raise NotImplementedError

    def words(self):
        """(Engc words the Trainer uses, arity) in the order it shows them."""
        return [(w, 2) for w in WORDS + SYMBOLS] + [(w, 1) for w in UNARY] + LOGIC

    def teach(self, trainer):
        from ..code.reading import Reader
        from ..code.statements import Machine
        from . import engc_statements as S
        brain = trainer.brain
        rng = self.rng
        lang = self.language()
        engc = Reader(brain, brain.code)
        reader = Reader(brain, {"seed": self.seed})
        reader.borrow(engc)

        def world(text):
            out = lang.run(text)
            return out["printed"] if out["ok"] else None
        reader.world = world

        def tr(text):
            return lang.from_engc(text).strip()

        trainer.say("A language you have never seen. I'll run some programs in it.")
        first = [P.one_op(rng, "PLUS") for _ in range(2)]
        reader.find_frame([tr(t) for t, _ in first])
        spent_words = set()
        for engc_words, arity in self.words():
            words = self.spell(engc_words, arity)
            if words is None or (words, arity) in spent_words:
                continue
            spent_words.add((words, arity))
            shown = first if engc_words == "PLUS" else \
                [P.one_op(rng, engc_words, unary=arity == 1) for _ in range(self.SHOWN)]
            demos = []
            for text, printed in shown:
                text = tr(text)
                reader.watch(text, printed)
                got = reader.demo_from(text, printed)
                if got is not None:
                    demos.append((got[2], got[3]))
            if not demos:
                reader.note("stuck", f"I couldn't tell what '{words}' joins")
                continue
            reader.study_known(tuple(words.split()), arity, demos,
                               min(self.PER_WORD, self.RUNS - reader.total_runs - 60))
        reader.borrow_grammar()
        if reader.prior:
            reader.levels, reader.assoc = reader.prior
        for _ in range(self.TWO_OPS):
            text, printed = P.program(rng, 2, 20)
            reader.watch(tr(text), printed)
        for _ in range(self.BRACKETS):
            text, printed = P.bracketed(rng)
            reader.watch(tr(text), printed)
        reader.learn_marks()
        reader.learn_grammar(max(0, self.RUNS - reader.total_runs - 45),
                             confirm=self.GRAMMAR_CONFIRM)
        code = dict(brain.code or {})
        code[self.store] = reader.to_json()
        brain.code = code

        # statements: films, carrying over what it knows about lines
        m = Machine(brain, reader)
        m.world = lang.trace

        def left():
            return self.RUNS - reader.total_runs - m.total_runs

        def show(text):
            m.watch(text, lang.trace(text))
        for text, _ in S.first_programs(rng):
            try:
                show(lang.from_engc(text))
            except ValueError:
                pass        # something this language has no way of saying
        for _ in range(self.MIXED):
            show(lang.from_engc(S.program(rng, S.LESSON, self.features)[0]))
        m.learn()
        m.experiment(min(self.OWN, left()))
        m.learn()
        streak = 0
        while streak < self.CONFIRM and left() > 0:
            text = lang.from_engc(S.program(rng, S.LESSON, self.features)[0])
            film = lang.trace(text)
            guess = m.predict(text)
            m.watch(text, film)
            if film["ok"] and guess == film["printed"]:
                streak += 1
                continue
            streak = 0
            m.learn()
            if m.wanting and left() > 0:
                m.experiment(min(self.OWN, left()))
                m.learn()
        code = dict(brain.code)
        state = dict(code[self.store])
        state["reader"] = reader.to_json()
        state["statements"] = m.to_json()
        code[self.store] = state
        brain.code = code
        trainer.say(f"That's all: {reader.total_runs + m.total_runs} programs run in this "
                    f"language ({reader.total_runs} with one line, {m.total_runs} with many).")


class InventedLanguage(SecondLanguage):
    number, title = 102, "A language never seen: the same ideas, every word new"
    goal = ("Every Engc word and mark is replaced by a fresh one. Can Ultron read its "
            "expressions and its statements as well as Engc's, from a third of the runs?")
    store = "invented"
    features = ("lists", "routines", "added")

    def language(self):
        from .languages import Invented
        return Invented()

    def spell(self, engc_words, arity):
        lang = self.language()
        return " ".join(lang.out[w] for w in engc_words.split())


class PythonSubset(SecondLanguage):
    number, title = 103, "A language never seen: a small part of Python"
    goal = ("Python's own words and marks, blocks shown only by how far a line is pushed "
            "in. Can Ultron read its expressions and its statements as well as Engc's, "
            "from a third of the runs?")
    store = "python"
    features = ("lists", "routines")

    def language(self):
        from .languages import Python
        return Python()

    def spell(self, engc_words, arity):
        from .languages import PY_OPS
        if engc_words == "MINUS" and arity == 1:
            return "-"
        return PY_OPS.get(tuple(engc_words.split()), engc_words if not
                          engc_words.isalpha() else None)


class OwnCodeWatched(Lesson):
    number, title = 104, "Its own code, watched from outside"
    goal = ("Ultron runs ten of its own functions (from dsl.py and amounts.py) on inputs "
            "it chooses, at most 20 times each. Can it find a law in its own program "
            "language for at least eight of them that holds far beyond the inputs it ran?")
    kind = "guided"

    def __init__(self, seed=0):
        super().__init__(seed)

    def teach(self, trainer):
        from ..code.own import OwnCode
        from . import own_code as O
        brain = trainer.brain
        oc = OwnCode(brain, (brain.code or {}).get("own"))
        trainer.say("These are some of your own functions. Run each one on inputs you "
                    "choose, at most 20 times, and tell me what it does.")
        for i, f in enumerate(O.FUNCTIONS):
            oc.study(O.name(f), lambda args, f=f: O.run(brain, f, args),
                     lambda rng, f=f: O.lesson_range(f, rng),
                     lambda args, f=f: O.allowed(f, args), self.seed * 100 + i, O.RUNS)
        code = dict(brain.code or {})
        code["own"] = oc.to_json()
        brain.code = code
        trainer.say(f"That's all: laws for {len(oc.found)} of {len(O.FUNCTIONS)} functions.")


def _world(sandbox):
    def run(text):
        out = sandbox.run(text)
        return out["printed"] if out["ok"] else None
    return run


def code_lessons(seed):
    """Code lessons need Engc in the sandbox; without it they are left out."""
    from ..code import sandbox
    if not sandbox.available():
        return []
    return [ReadingEngc(seed + 100), ReadingStatements(seed + 101),
            InventedLanguage(seed + 102), PythonSubset(seed + 103), OwnCodeWatched(seed + 104)]
