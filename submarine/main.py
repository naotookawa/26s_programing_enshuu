"""Entry point for the submarine game."""

from __future__ import annotations

import argparse

from .game import Game


def main() -> None:
    parser = argparse.ArgumentParser(description="潜水艦ゲーム")
    parser.add_argument(
        "--random-setup",
        action="store_true",
        help="艦を手入力せずランダム配置する",
    )
    parser.add_argument(
        "--auto-play",
        action="store_true",
        help="CPU同士で自動対戦する",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="ランダム配置・自動行動の乱数シード",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=200,
        help="自動対戦の最大ターン数",
    )
    parser.add_argument(
        "--first-player",
        choices=("A", "B", "random"),
        default="random",
        help="先攻プレイヤーを指定する",
    )
    args = parser.parse_args()
    if args.max_turns < 1:
        parser.error("--max-turns は 1 以上の整数を指定してください。")

    Game(
        random_setup=args.random_setup,
        auto_play=args.auto_play,
        seed=args.seed,
        max_turns=args.max_turns,
        first_player=args.first_player,
    ).run()


if __name__ == "__main__":
    main()
