import numpy as np

from submarine_py.rl.replay_buffer import ReplayBuffer, Transition


def test_replay_buffer_sample():
    buffer = ReplayBuffer(3, seed=1)
    state = np.zeros(231, dtype=np.float32)
    mask = np.ones(100, dtype=np.bool_)
    for action in range(4):
        buffer.append(Transition(state, action, float(action), state, False, mask))
    assert len(buffer) == 3
    sample = buffer.sample(2)
    assert len(sample) == 2
    assert all(item.state.shape == (231,) for item in sample)
