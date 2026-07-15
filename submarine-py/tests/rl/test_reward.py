from submarine_py import Field
from submarine_py.rl.belief import BeliefState
from submarine_py.rl.config import DQNConfig
from submarine_py.rl.reward import calculate_reward


def test_reward_components():
    before = BeliefState(Field())
    after = before.copy()
    after.set_one_hot("opponent", "w", [0, 0])
    reward = calculate_reward(
        before,
        after,
        damage_dealt=1,
        damage_taken=0,
        outcome=1,
        config=DQNConfig(),
    )
    assert reward.info > 0
    assert reward.hit == 1.0
    assert reward.damage == 0.0
    assert reward.terminal == 10.0
    assert reward.total > 10
