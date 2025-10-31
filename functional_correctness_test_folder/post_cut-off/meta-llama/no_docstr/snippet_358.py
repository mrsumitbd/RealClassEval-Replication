
import torch


class ResidualConnection:

    def __init__(self, use_residual: bool = False):
        self.use_residual = use_residual
        self.registered_input = None

    def register(self, x: torch.Tensor):
        self.registered_input = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        if self.use_residual:
            if self.registered_input is None:
                raise ValueError(
                    "Input not registered for residual connection")
            if self.registered_input.shape != y.shape:
                raise ValueError(
                    "Shape mismatch between registered input and output")
            return self.registered_input + y
        else:
            return y
