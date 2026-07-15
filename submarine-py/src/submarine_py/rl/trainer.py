from __future__ import annotations

from dataclasses import replace
import logging
from pathlib import Path
import random

import numpy as np
try:
    import torch
except ModuleNotFoundError:  # pragma: no cover - exercised in torch-less envs
    torch = None
try:
    from tqdm import tqdm
except ModuleNotFoundError:  # pragma: no cover - exercised in tqdm-less envs
    tqdm = None

from .agent import DQNAgent
from .config import DQNConfig
from .environment import DQNEnvironment
from .replay_buffer import ReplayBuffer, Transition


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    if torch is None:
        return
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def train(
    config: DQNConfig,
    *,
    seed: int = 0,
    device: str = "auto",
    model_dir: str = "models",
    resume: str | None = None,
    quiet: bool = False,
) -> dict:
    set_seed(seed)
    model_path = Path(model_dir)
    model_path.mkdir(parents=True, exist_ok=True)
    agent = DQNAgent(config, device=device, seed=seed)
    replay = ReplayBuffer(config.replay_capacity, seed=seed)
    start_episode = 0
    environment_steps = 0
    if resume:
        checkpoint = agent.load(resume)
        start_episode = int(checkpoint.get("episode", 0))
        environment_steps = int(checkpoint.get("environment_steps", 0))

    losses: list[float] = []
    last_stats = {}
    episode_range = range(start_episode + 1, config.training_episodes + 1)
    progress = episode_range
    if tqdm is not None:
        progress = tqdm(
            episode_range,
            total=max(0, config.training_episodes - start_episode),
            desc="training",
            unit="episode",
            disable=quiet,
        )
    for episode in progress:
        env = DQNEnvironment(config, seed=seed + episode)
        state, legal_mask = env.reset()
        done = False
        episode_reward = 0.0
        episode_loss = []
        outcome = 0
        damage_dealt = 0
        damage_taken = 0
        while not done:
            epsilon = config.epsilon_at(environment_steps)
            action = agent.select_action(state, legal_mask, epsilon)
            next_state, reward, done, info = env.step(action)
            next_mask = env._state_and_mask()[1]
            replay.append(
                Transition(state, action, reward, next_state, done, next_mask)
            )
            state, legal_mask = next_state, next_mask
            environment_steps += 1
            episode_reward += reward
            outcome = info.get("outcome", outcome)
            damage_dealt += info.get("damage_dealt", 0)
            damage_taken += info.get("damage_taken", 0)
            if environment_steps % config.train_frequency == 0:
                for _ in range(config.gradient_steps):
                    loss = agent.train_step(replay)
                    if loss is not None:
                        losses.append(loss)
                        episode_loss.append(loss)

        last_stats = {
            "episode": episode,
            "environment_steps": environment_steps,
            "gradient_steps": agent.gradient_steps,
            "epsilon": config.epsilon_at(environment_steps),
            "reward": episode_reward,
            "outcome": outcome,
            "turns": env.agent_turns,
            "loss": float(np.mean(episode_loss)) if episode_loss else None,
            "damage_dealt": damage_dealt,
            "damage_taken": damage_taken,
        }
        if not quiet and hasattr(progress, "set_postfix"):
            progress.set_postfix(
                reward=f"{episode_reward:.2f}",
                epsilon=f"{config.epsilon_at(environment_steps):.3f}",
                steps=environment_steps,
                gradients=agent.gradient_steps,
                loss=(
                    f"{last_stats['loss']:.4f}"
                    if last_stats["loss"] is not None else "warmup"
                ),
            )
        elif not quiet:
            logging.info(last_stats)

        if episode % config.checkpoint_interval == 0:
            agent.save(
                str(model_path / f"dqn_episode_{episode:06d}.pt"),
                episode=episode,
                environment_steps=environment_steps,
                epsilon=config.epsilon_at(environment_steps),
            )
        agent.save(
            str(model_path / "dqn_latest.pt"),
            episode=episode,
            environment_steps=environment_steps,
            epsilon=config.epsilon_at(environment_steps),
        )

    last_stats["losses"] = losses
    return last_stats


def with_overrides(config: DQNConfig, **kwargs) -> DQNConfig:
    values = {key: value for key, value in kwargs.items() if value is not None}
    return replace(config, **values)
