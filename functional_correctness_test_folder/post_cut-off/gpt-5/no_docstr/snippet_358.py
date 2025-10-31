import torch
from typing import Optional


class ResidualConnection:

    def __init__(self, use_residual: bool = False):
        self.use_residual = use_residual
        self._residual: Optional[torch.Tensor] = None

    def register(self, x: torch.Tensor):
        if self.use_residual:
            self._residual = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        if not self.use_residual:
            return y
        if self._residual is None:
            return y
        try:
            return y + self._residual
        except RuntimeError as e:
            raise ValueError(
                f"Incompatible shapes for residual addition: {tuple(y.shape)} and {tuple(self._residual.shape)}") from e
