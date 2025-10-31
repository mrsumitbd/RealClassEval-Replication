
import torch
from typing import Optional


class ResidualConnection:
    """
    A simple helper for applying residual connections in neural network modules.
    """

    def __init__(self, use_residual: bool = False):
        """
        Initialize the ResidualConnection.

        Args:
            use_residual (bool): If True, apply residual connection.
        """
        self.use_residual = use_residual
        self._x: Optional[torch.Tensor] = None

    def register(self, x: torch.Tensor):
        """
        Register the input tensor for residual connection.

        Args:
            x (torch.Tensor): The input tensor to be registered.
        """
        if not isinstance(x, torch.Tensor):
            raise TypeError(f"Expected torch.Tensor, got {type(x).__name__}")
        self._x = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        """
        Apply the residual connection to the output tensor `y`.

        If `use_residual` is False, `y` is returned unchanged.
        If `use_residual` is True, `y` is added to the previously registered
        input tensor `x`.  The tensors must be broadcastable.

        Args:
            y (torch.Tensor): The output tensor to which the residual will be added.

        Returns:
            torch.Tensor: The tensor after applying the residual connection.
        """
        if not isinstance(y, torch.Tensor):
            raise TypeError(f"Expected torch.Tensor, got {type(y).__name__}")

        if not self.use_residual:
            return y

        if self._x is None:
            raise RuntimeError(
                "ResidualConnection.apply called before register()")

        # Ensure the tensors are on the same device and dtype
        if y.device != self._x.device:
            raise RuntimeError(
                f"Device mismatch: y is on {y.device}, but registered x is on {self._x.device}"
            )
        if y.dtype != self._x.dtype:
            raise RuntimeError(
                f"Dtype mismatch: y is {y.dtype}, but registered x is {self._x.dtype}"
            )

        return y + self._x
