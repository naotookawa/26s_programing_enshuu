"""Player state for the submarine game."""

from __future__ import annotations

from dataclasses import dataclass, field

from .ship import SHIP_ORDER, Ship


@dataclass
class Player:
    name: str
    ships: dict[str, Ship] = field(default_factory=dict)
    hints: list[str] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)
    incoming_events: list[str] = field(default_factory=list)

    def alive_ships(self) -> list[Ship]:
        return [self.ships[kind] for kind in SHIP_ORDER if not self.ships[kind].sunk]

    def alive_count(self) -> int:
        return len(self.alive_ships())

    def all_sunk(self) -> bool:
        return self.alive_count() == 0

    def get_ship(self, kind: str) -> Ship:
        return self.ships[kind]

    def occupied_by_alive_ship(self, position, exclude_kind: str | None = None) -> bool:
        for kind, ship in self.ships.items():
            if kind == exclude_kind or ship.sunk:
                continue
            if ship.position == position:
                return True
        return False

