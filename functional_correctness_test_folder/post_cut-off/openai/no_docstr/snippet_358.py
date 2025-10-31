
import torch


class ResidualConnection:
    def __init__(self, use_residual: bool = False):
        self.use_residual = use_residual
        self._x = None

    def register(self, x: torch.Tensor):
        if not isinstance(x, torch.Tensor):
            raise TypeError("x must be a torch.Tensor")
        self._x = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        if not isinstance(y, torch.Tensor):
            raise TypeError("y must be a torch.Tensor")
        if self.use_residual:
            if self._x is None:
                raise RuntimeError("Residual tensor not registered")
            if self._x.shape != y.shape:
                raise ValueError(
                    "Shape mismatch between residual and input tensors")
            return y + self._x
        return y
