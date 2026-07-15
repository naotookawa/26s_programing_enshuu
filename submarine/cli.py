"""CLI input and display helpers."""

from __future__ import annotations

from typing import Callable, TypeVar

from .board import Position, PositionError, parse_position
from .ship import SHIP_NAMES


T = TypeVar("T")

ACTION_ALIASES = {
    "attack": "attack",
    "a": "attack",
    "魚雷攻撃": "attack",
    "攻撃": "attack",
    "move": "move",
    "m": "move",
    "移動": "move",
}

SHIP_ALIASES = {
    "b": "B",
    "battle": "B",
    "battleship": "B",
    "戦艦": "B",
    "c": "C",
    "cruiser": "C",
    "巡洋艦": "C",
    "s": "S",
    "submarine": "S",
    "潜水艦": "S",
}

DIRECTION_ALIASES = {
    "north": "north",
    "n": "north",
    "北": "north",
    "south": "south",
    "s": "south",
    "南": "south",
    "east": "east",
    "e": "east",
    "東": "east",
    "west": "west",
    "w": "west",
    "西": "west",
}


def prompt_until_valid(prompt: str, parser: Callable[[str], T]) -> T:
    while True:
        raw = input(prompt).strip()
        try:
            return parser(raw)
        except ValueError as exc:
            print(exc)


def prompt_action() -> str:
    return prompt_until_valid(
        "行動を選択してください [attack/move]: ",
        parse_action,
    )


def parse_action(text: str) -> str:
    action = ACTION_ALIASES.get(text.strip().lower())
    if action is None:
        raise ValueError("不正な行動です。attack または move を入力してください。")
    return action


def prompt_ship(prompt: str = "艦を選択してください [B/C/S]: ") -> str:
    return prompt_until_valid(prompt, parse_ship_kind)


def parse_ship_kind(text: str) -> str:
    kind = SHIP_ALIASES.get(text.strip().lower())
    if kind is None:
        raise ValueError("不正な艦です。B, C, S のいずれかを入力してください。")
    return kind


def prompt_direction() -> str:
    return prompt_until_valid(
        "方向を入力してください [north/south/east/west]: ",
        parse_direction,
    )


def parse_direction(text: str) -> str:
    direction = DIRECTION_ALIASES.get(text.strip().lower())
    if direction is None:
        raise ValueError("不正な方向です。north, south, east, west を入力してください。")
    return direction


def prompt_distance() -> int:
    return prompt_until_valid("距離を入力してください [1-4]: ", parse_distance)


def parse_distance(text: str) -> int:
    if not text.strip().isdigit():
        raise ValueError("不正な距離です。1〜4 の整数を入力してください。")
    distance = int(text)
    if not 1 <= distance <= 4:
        raise ValueError("不正な距離です。1〜4 の整数を入力してください。")
    return distance


def prompt_position(prompt: str) -> Position:
    try:
        return prompt_until_valid(prompt, parse_position)
    except PositionError:
        raise


def wait_for_next_player() -> None:
    input("\n相手プレイヤーに交代してください。準備ができたら Enter を押してください。")


def print_ship_legend() -> None:
    print("B: 戦艦")
    print("C: 巡洋艦")
    print("S: 潜水艦")
    print(".: 空きマス")
    print("X: 撃沈済み")


def format_ship_kinds(kinds: list[str]) -> str:
    if not kinds:
        return "なし"
    return ", ".join(SHIP_NAMES[kind] for kind in kinds)
