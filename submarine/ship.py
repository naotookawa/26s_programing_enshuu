"""Ship data structures."""

from __future__ import annotations

from dataclasses import dataclass

from .board import Position


SHIP_NAMES = {
    "B": "戦艦",
    "C": "巡洋艦",
    "S": "潜水艦",
}

SHIP_MAX_HP = {
    "B": 3,
    "C": 2,
    "S": 1,
}

SHIP_ORDER = ("B", "C", "S")


@dataclass
class Ship:
    kind: str
    position: Position
    hp: int | None = None

    def __post_init__(self) -> None:
        if self.hp is None:
            self.hp = self.max_hp

    @property
    def name(self) -> str:
        return SHIP_NAMES[self.kind]

    @property
    def max_hp(self) -> int:
        return SHIP_MAX_HP[self.kind]

    @property
    def sunk(self) -> bool:
        return self.hp <= 0

    @sunk.setter
    def sunk(self, value: bool) -> None:
        self.hp = 0 if value else self.max_hp

    def take_damage(self, amount: int = 1) -> None:
        self.hp = max(0, self.hp - amount)
