from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import random

import numpy as np


@dataclass(frozen=True)
class Transition:
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray
    done: bool
    next_legal_mask: np.ndarray


class ReplayBuffer:
    def __init__(self, capacity: int, seed: int | None = None):
        self.capacity = capacity
        self._items: deque[Transition] = deque(maxlen=capacity)
        self._rng = random.Random(seed)

    def __len__(self) -> int:
        return len(self._items)

    def append(self, transition: Transition) -> None:
        self._items.append(transition)

    def sample(self, batch_size: int) -> list[Transition]:
        if batch_size > len(self._items):
            raise ValueError("batch size exceeds replay buffer length")
        return self._rng.sample(list(self._items), batch_size)
