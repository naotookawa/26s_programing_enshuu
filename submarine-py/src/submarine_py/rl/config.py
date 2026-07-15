from __future__ import annotations

from dataclasses import dataclass

from submarine_py.ship import Ship

SHIP_TYPES = ("w", "c", "s")
SHIP_TO_INDEX = {ship_type: i for i, ship_type in enumerate(SHIP_TYPES)}
MAX_HPS = {ship_type: Ship.MAX_HPS[ship_type] for ship_type in SHIP_TYPES}


@dataclass
class DQNConfig:
    input_dim: int = 231
    output_dim: int = 100
    hidden_dims: tuple[int, int] = (256, 256)
    learning_rate: float = 1e-3
    gamma: float = 0.99
    replay_capacity: int = 50_000
    learning_starts: int = 1_000
    batch_size: int = 64
    target_update_interval: int = 1_000
    epsilon_start: float = 1.0
    epsilon_end: float = 0.05
    epsilon_decay_steps: int = 50_000
    train_frequency: int = 1
    gradient_steps: int = 1
    gradient_clip_norm: float = 10.0
    training_episodes: int = 20_000
    evaluation_interval: int = 500
    evaluation_games: int = 100
    checkpoint_interval: int = 1_000
    max_agent_turns_per_episode: int = 200
    beta_info: float = 0.5
    lambda_leak: float = 1.0
    beta_hit: float = 1.0
    beta_damage: float = 1.0
    beta_terminal: float = 10.0

    def epsilon_at(self, environment_steps: int) -> float:
        if self.epsilon_decay_steps <= 0:
            return self.epsilon_end
        progress = min(1.0, environment_steps / self.epsilon_decay_steps)
        value = self.epsilon_start + progress * (
            self.epsilon_end - self.epsilon_start
        )
        return max(self.epsilon_end, value)
