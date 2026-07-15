from submarine_py.rl.config import DQNConfig
from submarine_py.rl.trainer import train, with_overrides
import argparse
import logging


def main():
    parser = argparse.ArgumentParser(description="Train a DQN submarine player")
    parser.add_argument("--episodes", type=int, default=None)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--learning-rate", type=float, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--gamma", type=float, default=None)
    parser.add_argument("--model-dir", default="models")
    parser.add_argument("--resume", default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    config = with_overrides(
        DQNConfig(),
        training_episodes=args.episodes,
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        gamma=args.gamma,
    )
    train(
        config,
        seed=args.seed,
        device=args.device,
        model_dir=args.model_dir,
        resume=args.resume,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    main()
