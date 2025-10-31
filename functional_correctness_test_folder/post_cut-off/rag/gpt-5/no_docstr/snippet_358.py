from typing import Optional
import torch


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
        self._x: Optional[torch.Tensor] = None

    def register(self, x: torch.Tensor):
        '''
        Register the input tensor for residual connection.
        Args:
            x (torch.Tensor): The input tensor to be registered.
        '''
        if not self.use_residual:
            self._x = None
            return
        if not isinstance(x, torch.Tensor):
            raise TypeError("x must be a torch.Tensor")
        self._x = x

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
        if not self.use_residual:
            return y
        if self._x is None:
            raise RuntimeError(
                "No tensor registered for residual connection. Call register(x) before apply(y).")
        x = self._x
        self._x = None
        try:
            return y + x
        except RuntimeError as e:
            raise ValueError(
                f"Incompatible shapes for residual addition: x shape {tuple(x.shape)}, y shape {tuple(y.shape)}") from e
