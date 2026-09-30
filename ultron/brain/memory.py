"""Episodic memory: every experience is kept exactly, so any new idea can be
checked against everything Ultron has ever seen."""


class Spec:
    """What Ultron can perceive about one kind of experiment.

    kind:
      "measure"       a ruler reading of a length Ultron holds an idea about
      "program"       discrete inputs -> discrete outcome; law = small program
      "quantity"      measured numbers; law = invariant combination
      "conservation"  objects before/after an event; law = conserved total
    """

    def __init__(self, name, kind, inputs=None, target=None, out_type=None, group_by=None,
                 units=None, tol=1e-9, surprise=1e-6, precision=0.0, action=None,
                 state_var=None):
        self.name = name
        self.kind = kind
        self.inputs = dict(inputs or {})    # var -> type (program) or var -> dims (quantity)
        self.target = target
        self.out_type = out_type
        self.group_by = group_by
        self.units = dict(units or {})      # var -> (M, L, T) dimension exponents
        self.tol = tol                      # how constant an invariant must be
        self.surprise = surprise            # prediction error that counts as a surprise
        self.precision = precision          # instruments' stated relative precision (±)
        self.action = action                # for state changes: which action ("earn")
        self.state_var = state_var          # ... and which part of the state it predicts

    def to_json(self):
        return {k: (list(v) if isinstance(v, tuple) else v) for k, v in self.__dict__.items()}

    @classmethod
    def from_json(cls, d):
        d = dict(d)
        d["units"] = {k: tuple(v) for k, v in d.get("units", {}).items()}
        return cls(**d)


class Memory:
    def __init__(self):
        self.episodes = {}      # spec name -> list of experiences
        self.specs = {}

    def know(self, spec):
        self.specs.setdefault(spec.name, spec)
        self.episodes.setdefault(spec.name, [])

    def store(self, name, episode):
        self.episodes[name].append(episode)

    def of(self, name):
        return self.episodes.get(name, [])

    def to_json(self):
        return {"specs": {k: s.to_json() for k, s in sorted(self.specs.items())},
                "episodes": {k: v for k, v in sorted(self.episodes.items())}}

    @classmethod
    def from_json(cls, d):
        m = cls()
        m.specs = {k: Spec.from_json(v) for k, v in d.get("specs", {}).items()}
        m.episodes = {k: list(v) for k, v in d.get("episodes", {}).items()}
        return m
