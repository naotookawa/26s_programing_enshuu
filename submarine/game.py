"""Game orchestration and rule handling."""

from __future__ import annotations

import random
from typing import Iterable

from . import cli
from .board import (
    BOARD_SIZE,
    Position,
    can_attack_from,
    format_position,
    get_neighbors_9,
    is_in_bounds,
    move_position,
    render_own_board,
)
from .player import Player
from .ship import SHIP_NAMES, SHIP_ORDER, Ship


class Game:
    def __init__(
        self,
        random_setup: bool = False,
        auto_play: bool = False,
        seed: int | None = None,
        max_turns: int = 200,
        first_player: str = "random",
    ) -> None:
        self.players = [Player("Player A"), Player("Player B")]
        self.current_index = 0
        self.turn_number = 1
        self.auto_play = auto_play
        self.random_setup = random_setup or auto_play
        self.max_turns = max_turns
        self.first_player = first_player
        self.rng = random.Random(seed)

    def setup(self) -> None:
        print("=== 潜水艦ゲーム ===")
        print("5×5 の盤面に、戦艦・巡洋艦・潜水艦を1隻ずつ配置します。")
        for player in self.players:
            if self.random_setup:
                self._setup_player_randomly(player)
            else:
                self._setup_player_manually(player)
            if not self.auto_play:
                cli.wait_for_next_player()
        self._decide_first_player()

    def run(self) -> None:
        self.setup()
        while True:
            current = self.current_player
            opponent = self.opponent_player

            self._show_turn_header(current, opponent)
            if self.auto_play:
                self.handle_auto_turn(current, opponent)
            else:
                action = cli.prompt_action()
                if action == "attack":
                    self.handle_attack(current, opponent)
                else:
                    self.handle_move(current, opponent)

            if opponent.all_sunk():
                self._show_winner(current, opponent)
                return

            if self.auto_play and self.turn_number >= self.max_turns:
                self._show_turn_limit_reached()
                return

            self._advance_turn()
            if not self.auto_play:
                cli.wait_for_next_player()

    @property
    def current_player(self) -> Player:
        return self.players[self.current_index]

    @property
    def opponent_player(self) -> Player:
        return self.players[1 - self.current_index]

    def handle_attack(self, attacker: Player, defender: Player) -> None:
        ship = self._prompt_alive_ship(attacker, "攻撃に使う艦を選択してください [B/C/S]: ")
        target = self._prompt_attack_target(ship)
        self._resolve_attack(attacker, defender, ship, target)

    def _resolve_attack(self, attacker: Player, defender: Player, ship: Ship, target: Position) -> None:
        hit_ship = self._find_alive_ship_at(defender, target)
        if hit_ship is None:
            result_text = "外れ"
            print("\n外れました。")
        else:
            hit_ship.take_damage()
            if hit_ship.sunk:
                result_text = f"命中: {hit_ship.name} 撃沈"
                print(f"\n命中！ 敵の{hit_ship.name}を撃沈しました。")
            else:
                result_text = f"命中: {hit_ship.name} 耐久 {hit_ship.hp}/{hit_ship.max_hp}"
                print(f"\n命中！ 敵の{hit_ship.name}に1ダメージを与えました。")

        splash_kinds = self._splash_info(defender, target)
        self._print_splash_info(splash_kinds)

        splash_text = cli.format_ship_kinds(splash_kinds)
        target_text = format_position(target)
        attacker.hints.append(
            f"Turn {self.turn_number}: 攻撃 {target_text} -> {result_text} / 周囲報告: {splash_text}"
        )
        attacker.logs.append(
            f"Turn {self.turn_number}: {ship.name}で {target_text} を攻撃。結果: {result_text}。"
        )
        defender.incoming_events.append(
            f"Turn {self.turn_number}: 相手が {target_text} を攻撃。結果: {result_text}。周囲報告: {splash_text}。"
        )

    def handle_auto_turn(self, player: Player, opponent: Player) -> None:
        hit_options = self._auto_attack_options(player, opponent, hits_only=True)
        if hit_options:
            ship, target = self.rng.choice(hit_options)
            print(f"自動選択: {ship.name}で {format_position(target)} を攻撃します。")
            self._resolve_attack(player, opponent, ship, target)
            return

        move_options = self._best_auto_moves(player, opponent)
        if move_options:
            ship, direction, distance = self.rng.choice(move_options)
            print(f"自動選択: {ship.name}を {direction} に {distance} マス移動します。")
            self._resolve_move(player, opponent, ship, direction, distance)
            return

        attack_options = self._auto_attack_options(player, opponent, hits_only=False)
        ship, target = self.rng.choice(attack_options)
        print(f"自動選択: {ship.name}で {format_position(target)} を攻撃します。")
        self._resolve_attack(player, opponent, ship, target)

    def handle_move(self, player: Player, opponent: Player) -> None:
        ship = self._prompt_alive_ship(player, "移動する艦を選択してください [B/C/S]: ")
        while True:
            direction = cli.prompt_direction()
            distance = cli.prompt_distance()
            destination = move_position(ship.position, direction, distance)
            if not is_in_bounds(destination):
                print("その移動では盤面外に出ます。別の移動を入力してください。")
                continue
            if player.occupied_by_alive_ship(destination, exclude_kind=ship.kind):
                print("移動後の座標に自分の未撃沈艦があります。別の移動を入力してください。")
                continue
            break
        self._resolve_move(player, opponent, ship, direction, distance)

    def _resolve_move(
        self,
        player: Player,
        opponent: Player,
        ship: Ship,
        direction: str,
        distance: int,
    ) -> None:
        destination = move_position(ship.position, direction, distance)
        if not is_in_bounds(destination):
            raise ValueError("移動先が盤面外です。")
        if player.occupied_by_alive_ship(destination, exclude_kind=ship.kind):
            raise ValueError("移動先に自分の未撃沈艦があります。")
        old_position = ship.position
        ship.position = destination
        move_public_text = f"{ship.name} {direction} {distance}"
        print(
            f"\n{ship.name}を {direction} に {distance} マス移動しました。"
            f" ({format_position(old_position)} -> {format_position(destination)})"
        )
        player.logs.append(
            f"Turn {self.turn_number}: {ship.name}を {direction} に {distance} マス移動。"
        )
        opponent.hints.append(f"Turn {self.turn_number}: 相手移動 -> {move_public_text}")
        opponent.incoming_events.append(
            f"Turn {self.turn_number}: 相手は {ship.name} を {direction} に {distance} マス移動しました。"
        )

    def check_winner(self) -> Player | None:
        for player in self.players:
            if player.all_sunk():
                return self.players[1 - self.players.index(player)]
        return None

    def _setup_player_manually(self, player: Player) -> None:
        print(f"\n--- {player.name} の初期配置 ---")
        placed: set[Position] = set()
        for kind in SHIP_ORDER:
            name = SHIP_NAMES[kind]
            while True:
                position = cli.prompt_position(f"{player.name}: {name}の位置を入力してください: ")
                if position in placed:
                    print("その座標にはすでに自分の艦があります。別の座標を入力してください。")
                    continue
                player.ships[kind] = Ship(kind=kind, position=position)
                placed.add(position)
                break
        print(f"{player.name} の配置が完了しました。")

    def _setup_player_randomly(self, player: Player) -> None:
        print(f"\n--- {player.name} の初期配置 ---")
        positions = [
            Position(row=row, col=col)
            for row in range(BOARD_SIZE)
            for col in range(BOARD_SIZE)
        ]
        for kind, position in zip(SHIP_ORDER, self.rng.sample(positions, len(SHIP_ORDER))):
            player.ships[kind] = Ship(kind=kind, position=position)
        print(f"{player.name} の艦をランダムに配置しました。")

    def _decide_first_player(self) -> None:
        if self.first_player == "A":
            self.current_index = 0
        elif self.first_player == "B":
            self.current_index = 1
        else:
            self.current_index = self.rng.randrange(len(self.players))
        print(f"\n先攻: {self.current_player.name}")

    def _show_turn_header(self, current: Player, opponent: Player) -> None:
        print(f"\n=== Turn {self.turn_number}: {current.name} のターン ===\n")
        print("自分の盤面:")
        print(render_own_board(current.ships.values()))
        print()
        cli.print_ship_legend()
        print()
        print("自分の艦状態:")
        for kind in SHIP_ORDER:
            ship = current.ships[kind]
            status = (
                "撃沈済み"
                if ship.sunk
                else f"位置 {format_position(ship.position)}, 耐久 {ship.hp}/{ship.max_hp}"
            )
            print(f"- {ship.name}: {status}")
        print()
        print(f"相手の残機: {opponent.alive_count()} / {len(SHIP_ORDER)}")
        self._print_list("これまで得られたヒント", current.hints)
        self._print_list("直近の相手行動", current.incoming_events[-3:])
        self._print_list("自分の過去行動ログ", current.logs)

    def _prompt_alive_ship(self, player: Player, prompt: str) -> Ship:
        while True:
            kind = cli.prompt_ship(prompt)
            ship = player.get_ship(kind)
            if ship.sunk:
                print("その艦は撃沈済みです。別の艦を選択してください。")
                continue
            return ship

    def _prompt_attack_target(self, ship: Ship) -> Position:
        while True:
            target = cli.prompt_position("攻撃する座標を入力してください: ")
            if not can_attack_from(ship.position, target):
                print("その座標は攻撃可能範囲外です。")
                continue
            return target

    def _find_alive_ship_at(self, player: Player, position: Position) -> Ship | None:
        for ship in player.ships.values():
            if not ship.sunk and ship.position == position:
                return ship
        return None

    def _auto_attack_options(
        self,
        attacker: Player,
        defender: Player,
        hits_only: bool,
    ) -> list[tuple[Ship, Position]]:
        options: list[tuple[Ship, Position]] = []
        for ship in attacker.alive_ships():
            for target in get_neighbors_9(ship.position):
                hit_ship = self._find_alive_ship_at(defender, target)
                if hits_only and hit_ship is None:
                    continue
                options.append((ship, target))
        return options

    def _valid_moves_for_ship(self, player: Player, ship: Ship) -> list[tuple[Ship, str, int]]:
        options: list[tuple[Ship, str, int]] = []
        for direction in ("north", "south", "east", "west"):
            for distance in range(1, BOARD_SIZE):
                destination = move_position(ship.position, direction, distance)
                if not is_in_bounds(destination):
                    continue
                if player.occupied_by_alive_ship(destination, exclude_kind=ship.kind):
                    continue
                options.append((ship, direction, distance))
        return options

    def _best_auto_moves(self, player: Player, opponent: Player) -> list[tuple[Ship, str, int]]:
        enemy_positions = [ship.position for ship in opponent.alive_ships()]
        if not enemy_positions:
            return []

        scored_moves: list[tuple[int, Ship, str, int]] = []
        for ship in player.alive_ships():
            for _, direction, distance in self._valid_moves_for_ship(player, ship):
                destination = move_position(ship.position, direction, distance)
                score = min(self._attack_distance(destination, enemy) for enemy in enemy_positions)
                scored_moves.append((score, ship, direction, distance))

        if not scored_moves:
            return []

        best_score = min(score for score, _, _, _ in scored_moves)
        return [
            (ship, direction, distance)
            for score, ship, direction, distance in scored_moves
            if score == best_score
        ]

    def _attack_distance(self, origin: Position, target: Position) -> int:
        return max(abs(origin.row - target.row), abs(origin.col - target.col))

    def _splash_info(self, defender: Player, target: Position) -> list[str]:
        neighbor_cells = {position for position in get_neighbors_9(target) if position != target}
        kinds = [
            ship.kind
            for ship in defender.ships.values()
            if not ship.sunk and ship.position in neighbor_cells
        ]
        return self._ordered_unique_ship_kinds(kinds)

    def _print_splash_info(self, kinds: list[str]) -> None:
        if kinds:
            print(f"周囲報告: 攻撃座標の周囲1マスに {cli.format_ship_kinds(kinds)} がいます。")
        else:
            print("周囲報告: 攻撃座標の周囲1マスに敵艦はいません。")

    def _ordered_unique_ship_kinds(self, kinds: Iterable[str]) -> list[str]:
        present = set(kinds)
        return [kind for kind in SHIP_ORDER if kind in present]

    def _advance_turn(self) -> None:
        self.current_index = 1 - self.current_index
        self.turn_number += 1

    def _show_winner(self, winner: Player, loser: Player) -> None:
        self._print_victory_celebration(winner)
        print(f"{loser.name} のすべての艦が撃沈されました。")
        print("\n=== 最終盤面 ===")
        for player in self.players:
            print(f"\n{player.name}:")
            print(render_own_board(player.ships.values()))
            self._print_list("行動ログ", player.logs)
            self._print_list("ヒント履歴", player.hints)

    def _print_victory_celebration(self, winner: Player) -> None:
        width = 60
        lines = [
            "",
            "=" * width,
            " " * 20 + "V I C T O R Y",
            "-" * width,
            f"{winner.name} の勝利！".center(width),
            "全敵艦撃沈。作戦成功です。".center(width),
            "勝者に盛大な拍手を！".center(width),
            "=" * width,
        ]
        print("\n".join(lines))

    def _show_turn_limit_reached(self) -> None:
        print(f"\nターン上限 {self.max_turns} に達したため、自動対戦を終了します。")
        print("\n=== 現在の盤面 ===")
        for player in self.players:
            print(f"\n{player.name}:")
            print(render_own_board(player.ships.values()))
            self._print_list("行動ログ", player.logs)
            self._print_list("ヒント履歴", player.hints)

    def _print_list(self, title: str, entries: list[str]) -> None:
        print(f"\n{title}:")
        if not entries:
            print("なし")
            return
        for entry in entries:
            print(f"- {entry}")
