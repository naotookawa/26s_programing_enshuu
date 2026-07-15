"""Board and coordinate utilities for the submarine game."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


BOARD_SIZE = 5
COLUMNS = "ABCDE"


class PositionError(ValueError):
    """Raised when a CLI coordinate cannot be parsed."""


@dataclass(frozen=True, order=True)
class Position:
    """A board position using zero-based row and column indexes."""

    row: int
    col: int


def is_in_bounds(position: Position) -> bool:
    return 0 <= position.row < BOARD_SIZE and 0 <= position.col < BOARD_SIZE


def parse_position(text: str) -> Position:
    """Parse a coordinate such as A1 or E5 into a Position."""

    value = text.strip().upper()
    if len(value) < 2:
        raise PositionError("不正な座標です。A1〜E5 の形式で入力してください。")

    col_text = value[0]
    row_text = value[1:]
    if col_text not in COLUMNS or not row_text.isdigit():
        raise PositionError("不正な座標です。A1〜E5 の形式で入力してください。")

    position = Position(row=int(row_text) - 1, col=COLUMNS.index(col_text))
    if not is_in_bounds(position):
        raise PositionError("不正な座標です。A1〜E5 の形式で入力してください。")
    return position


def format_position(position: Position) -> str:
    """Format a Position into a coordinate such as A1."""

    if not is_in_bounds(position):
        raise PositionError("盤面外の座標です。")
    return f"{COLUMNS[position.col]}{position.row + 1}"


def get_neighbors_9(position: Position) -> list[Position]:
    """Return in-board cells around a position, including the center cell."""

    cells: list[Position] = []
    for row_delta in (-1, 0, 1):
        for col_delta in (-1, 0, 1):
            candidate = Position(position.row + row_delta, position.col + col_delta)
            if is_in_bounds(candidate):
                cells.append(candidate)
    return cells


def can_attack_from(origin: Position, target: Position) -> bool:
    """Return True if target is in the 3x3 area around origin."""

    return target in get_neighbors_9(origin)


def move_position(position: Position, direction: str, distance: int) -> Position:
    """Calculate the destination from a direction and distance."""

    deltas = {
        "north": (-1, 0),
        "south": (1, 0),
        "east": (0, 1),
        "west": (0, -1),
    }
    if direction not in deltas:
        raise ValueError("方向が不正です。")
    row_delta, col_delta = deltas[direction]
    return Position(
        row=position.row + row_delta * distance,
        col=position.col + col_delta * distance,
    )


def render_own_board(ships: Iterable[object]) -> str:
    """Render a player's own board.

    The ship objects are intentionally duck-typed so board.py does not need to
    import Ship and create a circular dependency.
    """

    grid = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    ordered_ships = sorted(ships, key=lambda ship: 0 if ship.sunk else 1)
    for ship in ordered_ships:
        marker = "X" if ship.sunk else ship.kind
        grid[ship.position.row][ship.position.col] = marker

    lines = ["   " + " ".join(COLUMNS)]
    for row_index, row in enumerate(grid, start=1):
        lines.append(f"{row_index}  " + " ".join(row))
    return "\n".join(lines)
