from __future__ import annotations

try:
    import torch
    from torch import nn
except ModuleNotFoundError:  # pragma: no cover - exercised in torch-less envs
    torch = None
    nn = None

from .config import DQNConfig


def _require_torch() -> None:
    if torch is None or nn is None:
        raise RuntimeError("PyTorch is required for DQNNetwork")


_BaseModule = nn.Module if nn is not None else object


class DQNNetwork(_BaseModule):
    def __init__(self, config: DQNConfig):
        _require_torch()
        super().__init__()
        h1, h2 = config.hidden_dims
        self.layers = nn.Sequential(
            nn.Linear(config.input_dim, h1),
            nn.ReLU(),
            nn.Linear(h1, h2),
            nn.ReLU(),
            nn.Linear(h2, config.output_dim),
        )

    def forward(self, x):
        return self.layers(x)


def select_device(device: str = "auto") -> torch.device:
    _require_torch()
    if device != "auto":
        return torch.device(device)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def masked_argmax(q_values: torch.Tensor, legal_mask: torch.Tensor) -> torch.Tensor:
    _require_torch()
    masked = q_values.masked_fill(~legal_mask, float("-inf"))
    return masked.argmax(dim=-1)
