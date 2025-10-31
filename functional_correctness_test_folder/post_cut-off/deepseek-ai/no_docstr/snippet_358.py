
import torch


class ResidualConnection:

    def __init__(self, use_residual: bool = False):
        self.use_residual = use_residual
        self.x = None

    def register(self, x: torch.Tensor):
        if self.use_residual:
            self.x = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        if self.use_residual and self.x is not None:
            return y + self.x
        return y
