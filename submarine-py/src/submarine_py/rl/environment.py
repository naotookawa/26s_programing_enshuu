from __future__ import annotations

import json
import random

import numpy as np

from submarine_py.field import Field
from submarine_py.server import GameControl

from .action_space import action_to_json, legal_action_mask, random_legal_action
from .belief import BeliefState
from .config import DQNConfig, SHIP_TYPES
from .reward import calculate_reward
from .state_encoder import encode_state


class DQNEnvironment:
    """Synchronous DQN environment backed by the existing GameControl."""

    def __init__(
        self,
        config: DQNConfig | None = None,
        *,
        field: Field | None = None,
        seed: int | None = None,
    ):
        self.config = config or DQNConfig()
        self.field = field or Field()
        self.rng = random.Random(seed)
        self.game: GameControl | None = None
        self.belief: BeliefState | None = None
        self.current_info: dict | None = None
        self.agent_turns = 0

    def _random_placement(self) -> dict[str, list[int]]:
        positions = self.rng.sample(self.field.squares, len(SHIP_TYPES))
        return {
            ship_type: list(position)
            for ship_type, position in zip(SHIP_TYPES, positions)
        }

    def reset(self) -> tuple[np.ndarray, np.ndarray]:
        self.game = GameControl(self.field)
        self.game.initialize(
            json.dumps(self._random_placement()),
            json.dumps(self._random_placement()),
        )
        self.belief = BeliefState(self.field)
        self.agent_turns = 0
        self.current_info = json.loads(self.game.initial_condition(0)[0])
        return self._state_and_mask()

    def _state_and_mask(self) -> tuple[np.ndarray, np.ndarray]:
        assert self.game is not None and self.belief is not None
        assert self.current_info is not None
        obs = self.current_info["observation"]
        state = encode_state(self.belief, obs["me"], obs["opponent"])
        mask = legal_action_mask(self.field, self.game.clients[0].ships)
        return state, mask

    def _hp(self, side: int) -> dict[str, int]:
        assert self.game is not None
        ships = self.game.clients[side].ships
        return {
            ship_type: ships[ship_type].hp if ship_type in ships else 0
            for ship_type in SHIP_TYPES
        }

    @staticmethod
    def _damage(before: dict[str, int], after: dict[str, int]) -> int:
        return sum(max(0, before[k] - after[k]) for k in SHIP_TYPES)

    def _opponent_random_action(self) -> int:
        assert self.game is not None
        mask = legal_action_mask(self.field, self.game.clients[1].ships)
        return random_legal_action(mask, self.rng)

    def step(self, action_index: int) -> tuple[np.ndarray, float, bool, dict]:
        assert self.game is not None and self.belief is not None
        before_belief = self.belief.copy()
        before_self_hp = self._hp(0)
        before_opp_hp = self._hp(1)
        before_self_alive = [k for k, hp in before_self_hp.items() if hp > 0]
        before_opp_alive = [k for k, hp in before_opp_hp.items() if hp > 0]

        action_payload = action_to_json(action_index)
        move_delta = None
        if "move" in action_payload:
            ship_type = action_payload["move"]["ship"]
            to = action_payload["move"]["to"]
            current = list(self.game.clients[0].ships[ship_type].position)
            move_delta = [to[0] - current[0], to[1] - current[1], ship_type]

        first_results = self.game.action(0, json.dumps(action_payload))
        agent_info = json.loads(first_results[0])

        if "attack" in action_payload:
            self.belief.update_from_own_attack(
                agent_info.get("result", {}).get("attacked"),
                before_opp_alive,
            )
        elif move_delta and "outcome" not in agent_info:
            dx, dy, ship_type = move_delta
            self.belief.shift("self", ship_type, [dx, dy])

        terminated = "outcome" in agent_info
        outcome = 0
        if terminated:
            outcome = 1 if agent_info["outcome"] else -1
            self.current_info = agent_info
            after_self_hp = self._hp(0)
            after_opp_hp = self._hp(1)
            reward = calculate_reward(
                before_belief,
                self.belief,
                self._damage(before_opp_hp, after_opp_hp),
                self._damage(before_self_hp, after_self_hp),
                outcome,
                self.config,
            )
            state, mask = self._state_and_mask()
            return state, reward.total, True, {
                "reward": reward,
                "outcome": outcome,
                "damage_dealt": self._damage(before_opp_hp, after_opp_hp),
                "damage_taken": self._damage(before_self_hp, after_self_hp),
            }

        before_self_hp_second = self._hp(0)
        before_opp_hp_second = self._hp(1)
        before_self_alive_second = [k for k, hp in before_self_hp_second.items() if hp > 0]
        before_opp_alive_second = [k for k, hp in before_opp_hp_second.items() if hp > 0]

        opponent_action = self._opponent_random_action()
        second_results = self.game.action(1, json.dumps(action_to_json(opponent_action)))
        passive_info = json.loads(second_results[1])
        opponent_result = passive_info.get("result", {})
        if "moved" in opponent_result and opponent_result["moved"]:
            moved = opponent_result["moved"]
            self.belief.shift("opponent", moved["ship"], moved["distance"])
        elif "attacked" in opponent_result and opponent_result["attacked"]:
            attacked = opponent_result["attacked"]
            self.belief.update_opponent_attack_position(
                attacked["position"], before_opp_alive_second
            )
            self.belief.update_self_from_opponent_attack(
                attacked, before_self_alive_second
            )

        self.agent_turns += 1
        terminated = "outcome" in passive_info
        if terminated:
            outcome = 1 if passive_info["outcome"] else -1
        elif self.agent_turns >= self.config.max_agent_turns_per_episode:
            terminated = True
            outcome = 0

        self.current_info = passive_info
        after_self_hp = self._hp(0)
        after_opp_hp = self._hp(1)
        reward = calculate_reward(
            before_belief,
            self.belief,
            self._damage(before_opp_hp, after_opp_hp),
            self._damage(before_self_hp, after_self_hp),
            outcome,
            self.config,
        )
        state, mask = self._state_and_mask()
        return state, reward.total, terminated, {
            "reward": reward,
            "outcome": outcome,
            "damage_dealt": self._damage(before_opp_hp, after_opp_hp),
            "damage_taken": self._damage(before_self_hp, after_self_hp),
            "opponent_action": opponent_action,
            "turns": self.agent_turns,
        }
