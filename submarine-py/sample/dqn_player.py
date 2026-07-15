from __future__ import annotations

from submarine_py import Player, play_game
from submarine_py.rl.action_space import action_to_json, decode_action, legal_action_mask
from submarine_py.rl.belief import BeliefState
from submarine_py.rl.config import DQNConfig, SHIP_TYPES
from submarine_py.rl.network import DQNNetwork, masked_argmax, select_device
from submarine_py.rl.state_encoder import encode_state
import argparse
import json
import random

try:
    import torch
except ModuleNotFoundError:  # pragma: no cover - exercised in torch-less envs
    torch = None


class DQNPlayer(Player):
    def __init__(self, model_path: str, *, device: str = "auto", seed: int = 0):
        if torch is None:
            raise RuntimeError("PyTorch is required for DQNPlayer")
        super().__init__()
        self.config = DQNConfig()
        self.device = select_device(device)
        self.network = DQNNetwork(self.config).to(self.device)
        checkpoint = torch.load(model_path, map_location=self.device)
        state_dict = checkpoint.get("online_network", checkpoint)
        self.network.load_state_dict(state_dict)
        self.network.eval()
        self.rng = random.Random(seed)
        self.belief: BeliefState | None = None
        self._last_move_delta: tuple[str, list[int]] | None = None

    def name(self):
        return "dqn-player"

    def place_ship(self):
        assert self.field
        self.belief = BeliefState(self.field)
        positions = self.rng.sample(self.field.squares, len(SHIP_TYPES))
        return {
            ship_type: list(position)
            for ship_type, position in zip(SHIP_TYPES, positions)
        }

    def _observation(self):
        if self.last_msg:
            return self.last_msg["observation"]
        return {
            "me": {
                ship_type: {
                    "hp": ship.hp,
                    "position": ship.position,
                }
                for ship_type, ship in self.ships.items()
            },
            "opponent": {
                "w": {"hp": 3},
                "c": {"hp": 2},
                "s": {"hp": 1},
            },
        }

    def action(self):
        assert self.field and self.belief
        obs = self._observation()
        state = encode_state(self.belief, obs["me"], obs["opponent"])
        mask = legal_action_mask(self.field, self.ships)
        with torch.no_grad():
            state_tensor = torch.as_tensor(
                state, dtype=torch.float32, device=self.device
            ).unsqueeze(0)
            mask_tensor = torch.as_tensor(
                mask, dtype=torch.bool, device=self.device
            ).unsqueeze(0)
            action_index = int(masked_argmax(self.network(state_tensor), mask_tensor).item())

        decoded = decode_action(action_index)
        if decoded.kind == "attack":
            self._last_move_delta = None
            return json.dumps(self.attack([decoded.x, decoded.y]))

        assert decoded.ship_type is not None
        ship = self.ships[decoded.ship_type]
        old_position = list(ship.position)
        to = [decoded.x, decoded.y]
        self._last_move_delta = (
            decoded.ship_type,
            [to[0] - old_position[0], to[1] - old_position[1]],
        )
        return json.dumps(self.move(decoded.ship_type, to))

    def update(self, json_str, turn_info) -> None:
        super().update(json_str, turn_info)
        assert self.belief
        info = self.last_msg or {}
        result = info.get("result", {})
        if turn_info == "your turn":
            if "attacked" in result:
                self.belief.update_from_own_attack(
                    result["attacked"],
                    list(info["observation"]["opponent"].keys()),
                )
            elif self._last_move_delta is not None:
                ship_type, distance = self._last_move_delta
                self.belief.shift("self", ship_type, distance)
            self._last_move_delta = None
        elif turn_info == "waiting":
            if "moved" in result and result["moved"]:
                moved = result["moved"]
                self.belief.shift("opponent", moved["ship"], moved["distance"])
            elif "attacked" in result and result["attacked"]:
                attacked = result["attacked"]
                self.belief.update_opponent_attack_position(
                    attacked["position"], list(info["observation"]["opponent"].keys())
                )
                self.belief.update_self_from_opponent_attack(
                    attacked, list(info["observation"]["me"].keys())
                )


def main():
    parser = argparse.ArgumentParser(description="DQN player for Submarine Game")
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    parser.add_argument("--model", required=True)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    play_game(args.host, args.port, DQNPlayer(args.model, device=args.device, seed=args.seed))


if __name__ == "__main__":
    main()
