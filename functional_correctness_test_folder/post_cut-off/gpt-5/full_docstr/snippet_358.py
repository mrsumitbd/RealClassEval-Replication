import torch
from typing import Optional


class ResidualConnection:
    '''
    A utility class for applying residual connections in neural networks.
    '''

    def __init__(self, use_residual: bool = False):
        '''
        Initialize the ResidualConnection.
        Args:
            use_residual (bool): If True, apply residual connection.
        '''
        self.use_residual = bool(use_residual)
        self._residual: Optional[torch.Tensor] = None

    def register(self, x: torch.Tensor):
        '''
        Register the input tensor for residual connection.
        Args:
            x (torch.Tensor): The input tensor to be registered.
        '''
        if not isinstance(x, torch.Tensor):
            raise TypeError("x must be a torch.Tensor")
        if self.use_residual:
            self._residual = x
        else:
            self._residual = None

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        '''
        Apply the residual connection.
        The residual connection is only applied if it was instantiated with `use_residual=True`.
        Args:
            y (torch.Tensor): The output tensor to which the residual connection is applied.
        Returns:
            torch.Tensor: The output tensor after applying the residual connection.
        '''
        if not isinstance(y, torch.Tensor):
            raise TypeError("y must be a torch.Tensor")

        if not self.use_residual or self._residual is None:
            return y

        x = self._residual
        self._residual = None

        if x.shape != y.shape:
            raise ValueError(
                f"Shape mismatch for residual connection: x.shape={x.shape}, y.shape={y.shape}")

        return y + x
