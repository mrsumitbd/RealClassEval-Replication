
import torch


class ResidualConnection:

    def __init__(self, use_residual: bool = False):
        self.use_residual = use_residual
        self._x = None

    def register(self, x: torch.Tensor):
        self._x = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        if self.use_residual and self._x is not None:
            return y + self._x
        return y
