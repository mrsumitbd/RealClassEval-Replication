
import torch


class ResidualConnection:

    def __init__(self, use_residual: bool = False):
        '''
        Initialize the ResidualConnection.
        Args:
            use_residual (bool): If True, apply residual connection.
        '''
        self.use_residual = use_residual
        self._residual = None

    def register(self, x: torch.Tensor):
        '''
        Register the input tensor for residual connection.
        Args:
            x (torch.Tensor): The input tensor to be registered.
        '''
        self._residual = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        if self.use_residual and self._residual is not None:
            return y + self._residual
        return y
