from __future__ import annotations

import numpy as np

from .belief import BeliefState
from .config import MAX_HPS, SHIP_TYPES


def _flatten_map(arr: np.ndarray) -> np.ndarray:
    return arr.astype(np.float32, copy=False).reshape(-1)


def encode_state(
    belief: BeliefState,
    self_observation: dict,
    opponent_observation: dict,
) -> np.ndarray:
    parts = []
    for arr in belief.as_maps():
        parts.append(_flatten_map(arr))

    height = belief.field.height
    width = belief.field.width
    for ship_type in SHIP_TYPES:
        arr = np.zeros((height, width), dtype=np.float32)
        ship = self_observation.get(ship_type)
        if ship and "position" in ship:
            x, y = ship["position"]
            arr[y, x] = 1.0
        parts.append(arr.reshape(-1))

    hp_values = []
    for ship_type in SHIP_TYPES:
        hp = self_observation.get(ship_type, {}).get("hp", 0)
        hp_values.append(hp / MAX_HPS[ship_type])
    for ship_type in SHIP_TYPES:
        hp = opponent_observation.get(ship_type, {}).get("hp", 0)
        hp_values.append(hp / MAX_HPS[ship_type])
    parts.append(np.asarray(hp_values, dtype=np.float32))

    state = np.concatenate(parts).astype(np.float32)
    if state.shape != (231,):
        raise ValueError(f"expected 231-dimensional state, got {state.shape}")
    return state
