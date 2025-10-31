
import torch


class ResidualConnection:

    def __init__(self, use_residual: bool = False):
        '''
        Initialize the ResidualConnection.
        Args:
            use_residual (bool): If True, apply residual connection.
        '''
        self.use_residual = use_residual
        self.registered_input = None

    def register(self, x: torch.Tensor):
        '''
        Register the input tensor for residual connection.
        Args:
            x (torch.Tensor): The input tensor to be registered.
        '''
        self.registered_input = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        '''
        Apply residual connection if enabled.
        Args:
            y (torch.Tensor): The output tensor to be added to the registered input.
        Returns:
            torch.Tensor: The output tensor with residual connection applied if enabled.
        '''
        if self.use_residual and self.registered_input is not None:
            return y + self.registered_input
        return y
