import numpy as np
import pytest

torch = pytest.importorskip("torch")

from submarine_py.rl.agent import DQNAgent
from submarine_py.rl.config import DQNConfig
from submarine_py.rl.network import DQNNetwork, masked_argmax
from submarine_py.rl.replay_buffer import ReplayBuffer, Transition


def test_network_output_shape_and_masked_argmax():
    config = DQNConfig(hidden_dims=(16, 16))
    network = DQNNetwork(config)
    output = network(torch.zeros((4, 231), dtype=torch.float32))
    assert output.shape == (4, 100)
    assert not torch.isnan(output).any()

    q_values = torch.arange(100, dtype=torch.float32).unsqueeze(0)
    mask = torch.zeros((1, 100), dtype=torch.bool)
    mask[0, 3] = True
    mask[0, 5] = True
    assert masked_argmax(q_values, mask).item() == 5


def test_train_step_and_checkpoint(tmp_path):
    config = DQNConfig(
        hidden_dims=(16, 16),
        learning_starts=2,
        batch_size=2,
        target_update_interval=1,
    )
    agent = DQNAgent(config, device="cpu", seed=1)
    buffer = ReplayBuffer(10, seed=1)
    state = np.zeros(231, dtype=np.float32)
    next_state = np.ones(231, dtype=np.float32)
    mask = np.ones(100, dtype=np.bool_)
    buffer.append(Transition(state, 0, 1.0, next_state, False, mask))
    assert agent.train_step(buffer) is None
    buffer.append(Transition(next_state, 1, 0.5, state, True, mask))
    before = [p.detach().clone() for p in agent.online_network.parameters()]
    loss = agent.train_step(buffer)
    assert loss is not None
    after = list(agent.online_network.parameters())
    assert any(not torch.equal(a, b) for a, b in zip(after, before))

    path = tmp_path / "checkpoint.pt"
    agent.save(str(path), episode=1, environment_steps=2, epsilon=0.5)
    loaded = DQNAgent(config, device="cpu")
    checkpoint = loaded.load(str(path))
    assert checkpoint["episode"] == 1
