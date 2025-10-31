
import torch


class ResidualConnection:

    def __init__(self, use_residual: bool = False):
        self.use_residual = use_residual
        self.registered_x = None

    def register(self, x: torch.Tensor):
        self.registered_x = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        if self.use_residual and self.registered_x is not None:
            return y + self.registered_x
        return y
