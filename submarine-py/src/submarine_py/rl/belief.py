from __future__ import annotations

from copy import deepcopy
import logging

import numpy as np

from submarine_py.field import Field

from .config import SHIP_TYPES


class BeliefState:
    """Six belief maps used by the DQN state encoder."""

    def __init__(self, field: Field):
        self.field = field
        self.opponent = {
            ship_type: self._uniform_map()
            for ship_type in SHIP_TYPES
        }
        self.self_belief = {
            ship_type: self._uniform_map()
            for ship_type in SHIP_TYPES
        }

    def copy(self) -> "BeliefState":
        copied = BeliefState(self.field)
        copied.opponent = {k: v.copy() for k, v in self.opponent.items()}
        copied.self_belief = {k: v.copy() for k, v in self.self_belief.items()}
        return copied

    def _empty_map(self) -> np.ndarray:
        return np.zeros((self.field.height, self.field.width), dtype=np.float32)

    def _uniform_map(self, positions: list[list[int]] | None = None) -> np.ndarray:
        positions = positions if positions is not None else self.field.squares
        arr = self._empty_map()
        if not positions:
            return arr
        prob = 1.0 / len(positions)
        for x, y in positions:
            arr[y, x] = prob
        return arr

    def _maps_for(self, side: str) -> dict[str, np.ndarray]:
        if side == "opponent":
            return self.opponent
        if side == "self":
            return self.self_belief
        raise ValueError(f"unknown belief side: {side}")

    def region(self, position: list[int]) -> list[list[int]]:
        x0, y0 = position
        cells = []
        for y in range(y0 - 1, y0 + 2):
            for x in range(x0 - 1, x0 + 2):
                if self.field.passable([x, y]):
                    cells.append([x, y])
        return cells

    def _normalize(
        self,
        arr: np.ndarray,
        fallback_positions: list[list[int]] | None = None,
    ) -> np.ndarray:
        total = float(arr.sum())
        if total > 0.0:
            return (arr / total).astype(np.float32)
        logging.warning("belief normalization failed; falling back to uniform map")
        positions = fallback_positions or self.field.squares
        if not positions:
            positions = self.field.squares
        return self._uniform_map(positions)

    def _constrain(
        self,
        side: str,
        ship_type: str,
        positions: list[list[int]],
        inside: bool,
    ) -> None:
        maps = self._maps_for(side)
        source = maps[ship_type]
        allowed = {tuple(position) for position in positions}
        arr = self._empty_map()
        fallback = []
        for x, y in self.field.squares:
            in_allowed = (x, y) in allowed
            if in_allowed == inside:
                arr[y, x] = source[y, x]
                fallback.append([x, y])
        maps[ship_type] = self._normalize(arr, fallback)

    def constrain_in(self, side: str, ship_type: str, positions: list[list[int]]) -> None:
        self._constrain(side, ship_type, positions, True)

    def constrain_out(self, side: str, ship_type: str, positions: list[list[int]]) -> None:
        self._constrain(side, ship_type, positions, False)

    def set_one_hot(self, side: str, ship_type: str, position: list[int]) -> None:
        arr = self._empty_map()
        if self.field.passable(position):
            x, y = position
            arr[y, x] = 1.0
        else:
            arr = self._uniform_map()
        self._maps_for(side)[ship_type] = arr

    def shift(self, side: str, ship_type: str, distance: list[int]) -> None:
        dx, dy = distance
        source = self._maps_for(side)[ship_type]
        arr = self._empty_map()
        fallback = []
        for x, y in self.field.squares:
            nx, ny = x + dx, y + dy
            if self.field.passable([nx, ny]):
                arr[ny, nx] += source[y, x]
                fallback.append([nx, ny])
        self._maps_for(side)[ship_type] = self._normalize(arr, fallback)

    def update_from_own_attack(
        self,
        attacked: dict | bool,
        alive_ship_types: list[str],
    ) -> None:
        if not attacked:
            return
        position = attacked["position"]
        region = self.region(position)
        hit = attacked.get("hit")
        near = set(attacked.get("near", []))
        if hit:
            self.set_one_hot("opponent", hit, position)
        for ship_type in alive_ship_types:
            if ship_type == hit:
                continue
            if ship_type in near:
                self.constrain_in("opponent", ship_type, region)
            else:
                self.constrain_out("opponent", ship_type, region)

    def update_self_from_opponent_attack(
        self,
        attacked: dict | bool,
        alive_ship_types: list[str],
    ) -> None:
        if not attacked:
            return
        position = attacked["position"]
        region = self.region(position)
        hit = attacked.get("hit")
        near = set(attacked.get("near", []))
        if hit:
            self.set_one_hot("self", hit, position)
        for ship_type in alive_ship_types:
            if ship_type == hit:
                continue
            if ship_type in near:
                self.constrain_in("self", ship_type, region)
            else:
                self.constrain_out("self", ship_type, region)

    def update_opponent_attack_position(
        self,
        position: list[int],
        alive_ship_types: list[str],
    ) -> None:
        region = {tuple(cell) for cell in self.region(position)}
        if not alive_ship_types:
            return

        q = {}
        for ship_type in alive_ship_types:
            belief = self.opponent[ship_type]
            q[ship_type] = sum(
                float(belief[y, x]) for x, y in region
            )
        p_event = 1.0
        for value in q.values():
            p_event *= (1.0 - value)
        p_event = 1.0 - p_event
        if p_event <= 0.0:
            logging.warning("opponent attack update contradicted current beliefs")
            for ship_type in alive_ship_types:
                self.constrain_in("opponent", ship_type, [list(cell) for cell in region])
            return

        for ship_type in alive_ship_types:
            source = self.opponent[ship_type]
            others_not_in_region = 1.0
            for other_type, value in q.items():
                if other_type != ship_type:
                    others_not_in_region *= (1.0 - value)
            other_event = 1.0 - others_not_in_region
            arr = self._empty_map()
            for x, y in self.field.squares:
                if (x, y) in region:
                    arr[y, x] = source[y, x] / p_event
                else:
                    arr[y, x] = source[y, x] * other_event / p_event
            self.opponent[ship_type] = self._normalize(arr)

    def concentration(self, side: str) -> float:
        maps = self._maps_for(side)
        return float(sum(np.square(maps[ship_type]).sum() for ship_type in SHIP_TYPES))

    def as_maps(self) -> list[np.ndarray]:
        return [
            deepcopy(self.opponent[ship_type])
            for ship_type in SHIP_TYPES
        ] + [
            deepcopy(self.self_belief[ship_type])
            for ship_type in SHIP_TYPES
        ]
