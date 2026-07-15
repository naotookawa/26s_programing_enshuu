from submarine_py.rl.action_space import random_legal_action
from submarine_py.rl.config import DQNConfig
from submarine_py.rl.environment import DQNEnvironment
from submarine_py.rl.replay_buffer import ReplayBuffer, Transition


def test_environment_one_step_adds_transition():
    config = DQNConfig(max_agent_turns_per_episode=5)
    env = DQNEnvironment(config, seed=1)
    state, mask = env.reset()
    action = random_legal_action(mask)
    next_state, reward, done, info = env.step(action)
    assert next_state.shape == (231,)
    assert isinstance(reward, float)
    assert isinstance(done, bool)
    assert "damage_dealt" in info

    replay = ReplayBuffer(10, seed=1)
    replay.append(Transition(state, action, reward, next_state, done, env._state_and_mask()[1]))
    assert len(replay) == 1
