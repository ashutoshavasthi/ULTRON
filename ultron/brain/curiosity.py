"""Curiosity driven by learning progress, not by raw error.

For each kind of experiment Ultron remembers its recent prediction errors.
Learning progress = (average error a while ago) - (average error recently).

  * errors falling            -> progress > 0  -> "I'm learning here", keep going
  * errors already ~0         -> progress = 0  -> mastered, boring
  * errors high, not falling  -> progress ~ 0  -> unlearnable noise, give up

Chasing raw error instead would trap the agent in front of pure noise forever
(the "noisy TV" problem).
"""

WINDOW = 8
NOVELTY_TRIES = 2 * WINDOW      # every new thing gets a fair look first
PROGRESS_THRESHOLD = 0.2


class Curiosity:
    def __init__(self):
        self.errors = {}

    def record(self, etype, error):
        self.errors.setdefault(etype, []).append(error)

    def progress(self, etype):
        errs = self.errors.get(etype, [])
        if len(errs) < NOVELTY_TRIES:
            return 1.0      # still novel
        older = errs[-2 * WINDOW:-WINDOW]
        recent = errs[-WINDOW:]
        return sum(older) / WINDOW - sum(recent) / WINDOW

    def recent_error(self, etype):
        errs = self.errors.get(etype, [])[-WINDOW:]
        return sum(errs) / len(errs) if errs else 1.0

    def choose(self, options):
        """Pick the experiment with the most learning progress; None if every
        option is boring (mastered) or hopeless (no progress)."""
        best, best_key = None, None
        for etype in options:       # options are in a fixed order: deterministic
            score = self.progress(etype)
            key = (score, -len(self.errors.get(etype, [])))
            if score > PROGRESS_THRESHOLD and (best_key is None or key > best_key):
                best, best_key = etype, key
        return best

    def to_json(self):
        return {"errors": self.errors}

    @classmethod
    def from_json(cls, d):
        c = cls()
        c.errors = {k: list(v) for k, v in d.get("errors", {}).items()}
        return c
