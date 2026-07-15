from __future__ import annotations

from dataclasses import dataclass

from .belief import BeliefState
from .config import DQNConfig


@dataclass
class RewardBreakdown:
    total: float
    info: float
    hit: float
    damage: float
    terminal: float


def calculate_reward(
    before: BeliefState,
    after: BeliefState,
    damage_dealt: int,
    damage_taken: int,
    outcome: int,
    config: DQNConfig,
) -> RewardBreakdown:
    opp_delta = after.concentration("opponent") - before.concentration("opponent")
    self_delta = after.concentration("self") - before.concentration("self")
    info = config.beta_info * (opp_delta - config.lambda_leak * self_delta)
    hit = config.beta_hit * damage_dealt
    damage = -config.beta_damage * damage_taken
    terminal = config.beta_terminal * outcome
    total = info + hit + damage + terminal
    return RewardBreakdown(total, info, hit, damage, terminal)
