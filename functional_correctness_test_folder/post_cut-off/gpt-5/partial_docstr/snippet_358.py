import torch
from typing import Optional


class ResidualConnection:

    def __init__(self, use_residual: bool = False):
        '''
        Initialize the ResidualConnection.
        Args:
            use_residual (bool): If True, apply residual connection.
        '''
        self.use_residual = use_residual
        self._residual: Optional[torch.Tensor] = None

    def register(self, x: torch.Tensor):
        '''
        Register the input tensor for residual connection.
        Args:
            x (torch.Tensor): The input tensor to be registered.
        '''
        if not isinstance(x, torch.Tensor):
            raise TypeError("x must be a torch.Tensor")
        self._residual = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        if not isinstance(y, torch.Tensor):
            raise TypeError("y must be a torch.Tensor")
        if not self.use_residual:
            return y
        if self._residual is None:
            raise RuntimeError(
                "No residual tensor registered. Call register(x) before apply(y).")
        res = self._residual
        if res.shape != y.shape:
            raise ValueError(
                f"Shape mismatch for residual connection: {res.shape} vs {y.shape}")
        if res.device != y.device or res.dtype != y.dtype:
            res = res.to(device=y.device, dtype=y.dtype)
        out = y + res
        self._residual = None
        return out
