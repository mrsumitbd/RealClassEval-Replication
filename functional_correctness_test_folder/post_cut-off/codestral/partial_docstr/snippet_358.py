
import torch


class ResidualConnection:

    def __init__(self, use_residual: bool = False):
        '''
        Initialize the ResidualConnection.
        Args:
            use_residual (bool): If True, apply residual connection.
        '''
        self.use_residual = use_residual
        self.x = None

    def register(self, x: torch.Tensor):
        '''
        Register the input tensor for residual connection.
        Args:
            x (torch.Tensor): The input tensor to be registered.
        '''
        self.x = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        '''
        Apply the residual connection to the input tensor.
        Args:
            y (torch.Tensor): The input tensor to which the residual connection is applied.
        Returns:
            torch.Tensor: The output tensor after applying the residual connection.
        '''
        if self.use_residual and self.x is not None:
            return y + self.x
        return y
