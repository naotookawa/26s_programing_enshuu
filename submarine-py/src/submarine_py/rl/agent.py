from __future__ import annotations

from dataclasses import asdict
import random

import numpy as np
try:
    import torch
    import torch.nn.functional as F
except ModuleNotFoundError:  # pragma: no cover - exercised in torch-less envs
    torch = None
    F = None

from .action_space import random_legal_action
from .config import DQNConfig
from .network import DQNNetwork, masked_argmax, select_device
from .replay_buffer import ReplayBuffer


def _require_torch() -> None:
    if torch is None or F is None:
        raise RuntimeError("PyTorch is required for DQNAgent")


class DQNAgent:
    def __init__(
        self,
        config: DQNConfig | None = None,
        *,
        device: str = "auto",
        seed: int | None = None,
    ):
        _require_torch()
        self.config = config or DQNConfig()
        self.device = select_device(device)
        self.rng = random.Random(seed)
        self.online_network = DQNNetwork(self.config).to(self.device)
        self.target_network = DQNNetwork(self.config).to(self.device)
        self.target_network.load_state_dict(self.online_network.state_dict())
        self.optimizer = torch.optim.Adam(
            self.online_network.parameters(),
            lr=self.config.learning_rate,
        )
        self.gradient_steps = 0

    def select_action(
        self,
        state: np.ndarray,
        legal_mask: np.ndarray,
        epsilon: float,
    ) -> int:
        if self.rng.random() < epsilon:
            return random_legal_action(legal_mask, self.rng)
        with torch.no_grad():
            state_tensor = torch.as_tensor(
                state, dtype=torch.float32, device=self.device
            ).unsqueeze(0)
            mask_tensor = torch.as_tensor(
                legal_mask, dtype=torch.bool, device=self.device
            ).unsqueeze(0)
            q_values = self.online_network(state_tensor)
            return int(masked_argmax(q_values, mask_tensor).item())

    def train_step(self, replay_buffer: ReplayBuffer) -> float | None:
        _require_torch()
        if len(replay_buffer) < self.config.learning_starts:
            return None
        if len(replay_buffer) < self.config.batch_size:
            return None

        batch = replay_buffer.sample(self.config.batch_size)
        states = torch.as_tensor(
            np.stack([item.state for item in batch]),
            dtype=torch.float32,
            device=self.device,
        )
        actions = torch.as_tensor(
            [item.action for item in batch],
            dtype=torch.long,
            device=self.device,
        )
        rewards = torch.as_tensor(
            [item.reward for item in batch],
            dtype=torch.float32,
            device=self.device,
        )
        next_states = torch.as_tensor(
            np.stack([item.next_state for item in batch]),
            dtype=torch.float32,
            device=self.device,
        )
        dones = torch.as_tensor(
            [item.done for item in batch],
            dtype=torch.bool,
            device=self.device,
        )
        next_masks = torch.as_tensor(
            np.stack([item.next_legal_mask for item in batch]),
            dtype=torch.bool,
            device=self.device,
        )

        predicted_q = self.online_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        with torch.no_grad():
            next_q = self.target_network(next_states).masked_fill(
                ~next_masks, float("-inf")
            )
            next_max = next_q.max(dim=1).values
            next_max = torch.where(torch.isfinite(next_max), next_max, torch.zeros_like(next_max))
            target_q = rewards + (~dones).float() * self.config.gamma * next_max

        loss = F.smooth_l1_loss(predicted_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            self.online_network.parameters(),
            max_norm=self.config.gradient_clip_norm,
        )
        self.optimizer.step()
        self.gradient_steps += 1
        if self.gradient_steps % self.config.target_update_interval == 0:
            self.update_target_network()
        return float(loss.item())

    def update_target_network(self) -> None:
        self.target_network.load_state_dict(self.online_network.state_dict())

    def checkpoint(
        self,
        *,
        episode: int,
        environment_steps: int,
        epsilon: float,
    ) -> dict:
        return {
            "online_network": self.online_network.state_dict(),
            "target_network": self.target_network.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "config": asdict(self.config),
            "episode": episode,
            "environment_steps": environment_steps,
            "gradient_steps": self.gradient_steps,
            "epsilon": epsilon,
        }

    def save(
        self,
        path: str,
        *,
        episode: int,
        environment_steps: int,
        epsilon: float,
    ) -> None:
        torch.save(
            self.checkpoint(
                episode=episode,
                environment_steps=environment_steps,
                epsilon=epsilon,
            ),
            path,
        )

    def load(self, path: str) -> dict:
        _require_torch()
        checkpoint = torch.load(path, map_location=self.device)
        self.online_network.load_state_dict(checkpoint["online_network"])
        target_state = checkpoint.get("target_network", checkpoint["online_network"])
        self.target_network.load_state_dict(target_state)
        if "optimizer" in checkpoint:
            self.optimizer.load_state_dict(checkpoint["optimizer"])
        self.gradient_steps = int(checkpoint.get("gradient_steps", 0))
        return checkpoint
