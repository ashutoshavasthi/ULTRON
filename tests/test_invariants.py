from ultron.brain.invariants import search_conservation, search_invariant
from ultron.env import dataworld
from ultron.env.physics import PhysicsSandbox


def test_finds_newtons_second_law():
    w = PhysicsSandbox(1)
    eps = [{"F": F, "m": m, "a": w.push(m, F)} for F, m in [(3, 2), (10, 4), (7, 1.5), (2, 5)]]
    law = search_invariant("push", eps, ["F", "m", "a"], 1e-9).law
    assert law.kind == "global" and law.powers == {"F": 1, "a": -1, "m": -1}
    assert abs(law.constant - 1) < 1e-9


def test_invents_a_per_spring_property():
    w = PhysicsSandbox(2)
    eps = [{"x": x, "spring": s, "F": w.stretch(s, x)}
           for s in w.springs[:3] for x in (0.1, 0.2, 0.35)]
    law = search_invariant("stretch", eps, ["x", "F"], 1e-9, group_by="spring").law
    assert law.kind == "grouped" and law.powers == {"F": 1, "x": -1}
    for s in w.springs[:3]:
        assert abs(law.properties[s] - w.secret_stiffness(s)) < 1e-6


def test_keplers_third_law_from_real_data():
    rows = [r for r in dataworld.orbits() if r["system"] == "Sun"]
    law = search_invariant("orbit", rows, ["r", "T"], 0.02, group_by="system").law
    assert law.powers == {"T": 2, "r": -3}


def test_momentum_always_energy_only_for_bouncy():
    w = PhysicsSandbox(3)
    events = []
    for m1, v1, m2, v2, kind in [(1, 3, 2, -1, "clay"), (2, 4, 1, 0, "steel"),
                                 (3, 1, 1, -2, "steel"), (1, 5, 4, 1, "clay")]:
        u1, u2 = w.collide(m1, v1, m2, v2, kind)
        events.append({"before": [(m1, v1), (m2, v2)], "after": [(m1, u1), (m2, u2)],
                       "kind": kind})
    laws, _ = search_conservation("collide", events)
    found = {l.formula(): l.scope for l in laws}
    assert found["m·v"] == "all"
    assert found["m·v^2"] == ["steel"]
