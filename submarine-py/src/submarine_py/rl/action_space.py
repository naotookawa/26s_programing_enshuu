from __future__ import annotations

from dataclasses import dataclass
import random

import numpy as np

from submarine_py.field import Field

from .config import SHIP_TO_INDEX, SHIP_TYPES

BOARD_WIDTH = 5
BOARD_HEIGHT = 5
ATTACK_ACTIONS = BOARD_WIDTH * BOARD_HEIGHT
ACTION_SIZE = ATTACK_ACTIONS + len(SHIP_TYPES) * ATTACK_ACTIONS


@dataclass(frozen=True)
class Action:
    kind: str
    x: int
    y: int
    ship_type: str | None = None


def cell_index(x: int, y: int) -> int:
    if not (0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT):
        raise ValueError(f"cell out of range: {(x, y)}")
    return y * BOARD_WIDTH + x


def encode_attack(x: int, y: int) -> int:
    return cell_index(x, y)


def encode_move(ship_type: str, x: int, y: int) -> int:
    if ship_type not in SHIP_TO_INDEX:
        raise ValueError(f"unknown ship type: {ship_type}")
    return ATTACK_ACTIONS + ATTACK_ACTIONS * SHIP_TO_INDEX[ship_type] + cell_index(x, y)


def decode_action(action_index: int) -> Action:
    if not (0 <= action_index < ACTION_SIZE):
        raise ValueError(f"action index out of range: {action_index}")
    if action_index < ATTACK_ACTIONS:
        y, x = divmod(action_index, BOARD_WIDTH)
        return Action("attack", x, y)
    offset = action_index - ATTACK_ACTIONS
    ship_index, cell = divmod(offset, ATTACK_ACTIONS)
    y, x = divmod(cell, BOARD_WIDTH)
    return Action("move", x, y, SHIP_TYPES[ship_index])


def _position_of(ship) -> list[int]:
    return list(ship.position)


def legal_action_mask(field: Field, ships: dict) -> np.ndarray:
    mask = np.zeros(ACTION_SIZE, dtype=np.bool_)

    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            to = [x, y]
            if not field.passable(to):
                continue
            if any(ship.in_attack_range(to) for ship in ships.values()):
                mask[encode_attack(x, y)] = True

    occupied = {
        tuple(_position_of(ship)): ship_type
        for ship_type, ship in ships.items()
    }
    for ship_type in SHIP_TYPES:
        ship = ships.get(ship_type)
        if ship is None:
            continue
        current = _position_of(ship)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                to = [x, y]
                if to == current:
                    continue
                if not field.passable(to):
                    continue
                if current[0] != x and current[1] != y:
                    continue
                occupant = occupied.get((x, y))
                if occupant is not None and occupant != ship_type:
                    continue
                mask[encode_move(ship_type, x, y)] = True

    return mask


def random_legal_action(mask: np.ndarray, rng: random.Random | None = None) -> int:
    legal = np.flatnonzero(mask)
    if len(legal) == 0:
        raise ValueError("no legal actions available")
    chooser = rng if rng is not None else random
    return int(chooser.choice(legal.tolist()))


def action_to_json(action_index: int) -> dict:
    action = decode_action(action_index)
    if action.kind == "attack":
        return {"attack": {"to": [action.x, action.y]}}
    assert action.ship_type is not None
    return {"move": {"ship": action.ship_type, "to": [action.x, action.y]}}
