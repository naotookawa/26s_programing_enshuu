import numpy as np

from submarine_py import Field
from submarine_py.rl.belief import BeliefState


def test_initial_beliefs_are_uniform_and_normalized():
    belief = BeliefState(Field())
    for maps in (belief.opponent, belief.self_belief):
        for arr in maps.values():
            assert np.isclose(arr.sum(), 1.0)
            assert np.isclose(arr[0, 0], 1 / 25)


def test_region_updates_and_zero_preservation():
    belief = BeliefState(Field())
    region = belief.region([0, 0])
    belief.constrain_in("opponent", "w", region)
    assert np.isclose(belief.opponent["w"].sum(), 1.0)
    assert belief.opponent["w"][4, 4] == 0.0
    belief.constrain_out("opponent", "w", belief.region([4, 4]))
    assert np.isclose(belief.opponent["w"].sum(), 1.0)
    assert belief.opponent["w"][4, 4] == 0.0


def test_hit_and_shift_updates():
    belief = BeliefState(Field())
    belief.set_one_hot("opponent", "c", [1, 1])
    assert belief.opponent["c"][1, 1] == 1.0
    belief.shift("opponent", "c", [2, 0])
    assert np.isclose(belief.opponent["c"].sum(), 1.0)
    assert belief.opponent["c"][1, 3] == 1.0


def test_attack_updates_and_or_condition_normalize():
    belief = BeliefState(Field())
    belief.update_from_own_attack(
        {"position": [2, 2], "hit": "w", "near": ["c"]},
        ["w", "c", "s"],
    )
    assert belief.opponent["w"][2, 2] == 1.0
    assert np.isclose(belief.opponent["c"].sum(), 1.0)
    assert np.isclose(belief.opponent["s"].sum(), 1.0)

    belief.update_opponent_attack_position([0, 0], ["w", "c", "s"])
    for ship_type in ["w", "c", "s"]:
        assert np.isclose(belief.opponent[ship_type].sum(), 1.0)


def test_normalization_fallback():
    belief = BeliefState(Field())
    belief.constrain_in("self", "s", [])
    assert np.isclose(belief.self_belief["s"].sum(), 1.0)
