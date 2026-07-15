"""Non-interactive rule checks for the submarine game."""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO

from .board import Position, can_attack_from, format_position, get_neighbors_9, move_position, parse_position
from .game import Game
from .ship import Ship


def main() -> None:
    assert parse_position("A1") == Position(0, 0)
    assert parse_position("E5") == Position(4, 4)
    assert format_position(Position(2, 2)) == "C3"
    assert Position(1, 1) in get_neighbors_9(Position(0, 0))
    assert can_attack_from(Position(2, 2), Position(3, 3))
    assert not can_attack_from(Position(2, 2), Position(4, 4))
    assert move_position(Position(2, 2), "north", 2) == Position(0, 2)

    game = Game()
    attacker, defender = game.players
    attacker.ships["B"] = Ship("B", Position(0, 0))
    attacker.ships["C"] = Ship("C", Position(2, 2))
    attacker.ships["S"] = Ship("S", Position(4, 4))
    defender.ships["B"] = Ship("B", Position(1, 1))
    defender.ships["C"] = Ship("C", Position(4, 4))
    defender.ships["S"] = Ship("S", Position(0, 4))

    assert game._splash_info(defender, Position(0, 0)) == ["B"]
    defender.ships["B"].sunk = True
    assert game._splash_info(defender, Position(0, 0)) == []
    assert attacker.occupied_by_alive_ship(Position(2, 2), exclude_kind="B")
    assert not attacker.occupied_by_alive_ship(Position(0, 1), exclude_kind="B")

    miss_game = Game()
    miss_attacker, miss_defender = miss_game.players
    miss_attacker.ships["B"] = Ship("B", Position(0, 0))
    miss_attacker.ships["C"] = Ship("C", Position(2, 2))
    miss_attacker.ships["S"] = Ship("S", Position(4, 4))
    miss_defender.ships["B"] = Ship("B", Position(4, 0))
    miss_defender.ships["C"] = Ship("C", Position(4, 2))
    miss_defender.ships["S"] = Ship("S", Position(4, 4))
    miss_game._prompt_alive_ship = lambda player, prompt: miss_attacker.ships["B"]
    miss_game._prompt_attack_target = lambda ship: Position(0, 1)
    with redirect_stdout(StringIO()):
        miss_game.handle_attack(miss_attacker, miss_defender)
    assert miss_attacker.logs == ["Turn 1: 戦艦で B1 を攻撃。結果: 外れ。"]
    assert miss_defender.logs == []
    assert miss_defender.incoming_events == ["Turn 1: 相手が B1 を攻撃。結果: 外れ。周囲報告: なし。"]

    hit_game = Game()
    hit_attacker, hit_defender = hit_game.players
    hit_attacker.ships["B"] = Ship("B", Position(0, 0))
    hit_attacker.ships["C"] = Ship("C", Position(2, 2))
    hit_attacker.ships["S"] = Ship("S", Position(4, 4))
    hit_defender.ships["B"] = Ship("B", Position(0, 1))
    hit_defender.ships["C"] = Ship("C", Position(4, 2))
    hit_defender.ships["S"] = Ship("S", Position(4, 4))
    hit_game._prompt_alive_ship = lambda player, prompt: hit_attacker.ships["B"]
    hit_game._prompt_attack_target = lambda ship: Position(0, 1)
    with redirect_stdout(StringIO()):
        hit_game.handle_attack(hit_attacker, hit_defender)
    assert hit_defender.ships["B"].hp == 2
    assert not hit_defender.ships["B"].sunk
    assert hit_attacker.logs == ["Turn 1: 戦艦で B1 を攻撃。結果: 命中: 戦艦 耐久 2/3。"]
    assert hit_defender.logs == []
    assert hit_defender.incoming_events == [
        "Turn 1: 相手が B1 を攻撃。結果: 命中: 戦艦 耐久 2/3。周囲報告: なし。"
    ]

    sink_game = Game()
    sink_attacker, sink_defender = sink_game.players
    sink_attacker.ships["B"] = Ship("B", Position(0, 0))
    sink_attacker.ships["C"] = Ship("C", Position(2, 2))
    sink_attacker.ships["S"] = Ship("S", Position(4, 4))
    sink_defender.ships["B"] = Ship("B", Position(4, 0))
    sink_defender.ships["C"] = Ship("C", Position(4, 2))
    sink_defender.ships["S"] = Ship("S", Position(0, 1))
    sink_game._prompt_alive_ship = lambda player, prompt: sink_attacker.ships["B"]
    sink_game._prompt_attack_target = lambda ship: Position(0, 1)
    with redirect_stdout(StringIO()):
        sink_game.handle_attack(sink_attacker, sink_defender)
    assert sink_defender.ships["S"].sunk
    assert sink_attacker.logs == ["Turn 1: 戦艦で B1 を攻撃。結果: 命中: 潜水艦 撃沈。"]
    assert sink_defender.incoming_events == [
        "Turn 1: 相手が B1 を攻撃。結果: 命中: 潜水艦 撃沈。周囲報告: なし。"
    ]

    auto_game = Game(auto_play=True, seed=0)
    auto_attacker, auto_defender = auto_game.players
    auto_attacker.ships["B"] = Ship("B", Position(0, 0))
    auto_attacker.ships["C"] = Ship("C", Position(2, 2))
    auto_attacker.ships["S"] = Ship("S", Position(4, 4))
    auto_defender.ships["B"] = Ship("B", Position(0, 1))
    auto_defender.ships["C"] = Ship("C", Position(4, 2))
    auto_defender.ships["S"] = Ship("S", Position(4, 0))
    with redirect_stdout(StringIO()):
        auto_game.handle_auto_turn(auto_attacker, auto_defender)
    assert auto_defender.ships["B"].hp == 2
    assert auto_attacker.logs == ["Turn 1: 戦艦で B1 を攻撃。結果: 命中: 戦艦 耐久 2/3。"]
    assert auto_defender.logs == []

    print("smoke tests passed")


if __name__ == "__main__":
    main()
