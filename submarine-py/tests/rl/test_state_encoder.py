import numpy as np

from submarine_py import Field
from submarine_py.rl.belief import BeliefState
from submarine_py.rl.state_encoder import encode_state


def test_state_shape_dtype_and_values():
    belief = BeliefState(Field())
    belief.set_one_hot("opponent", "w", [1, 0])
    state = encode_state(
        belief,
        {
            "w": {"hp": 2, "position": [0, 0]},
            "c": {"hp": 2, "position": [2, 2]},
        },
        {
            "w": {"hp": 3},
            "s": {"hp": 1},
        },
    )
    assert state.shape == (231,)
    assert state.dtype == np.float32
    assert np.all(state >= 0)
    assert np.all(state <= 1)
    assert state[1] == 1.0

    actual_w_offset = 150
    actual_c_offset = 150 + 25
    actual_s_offset = 150 + 50
    assert state[actual_w_offset + 0] == 1.0
    assert state[actual_c_offset + 12] == 1.0
    assert np.all(state[actual_s_offset:actual_s_offset + 25] == 0)

    hp = state[-6:]
    assert np.isclose(hp[0], 2 / 3)
    assert hp[1] == 1.0
    assert hp[2] == 0.0
    assert hp[3] == 1.0
    assert hp[4] == 0.0
    assert hp[5] == 1.0
