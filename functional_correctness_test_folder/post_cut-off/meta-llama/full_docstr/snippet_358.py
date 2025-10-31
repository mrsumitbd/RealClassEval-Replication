
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
        Apply the residual connection.
        The residual connection is only applied if it was instantiated with `use_residual=True`.
        Args:
            y (torch.Tensor): The output tensor to which the residual connection is applied.
        Returns:
            torch.Tensor: The output tensor after applying the residual connection.
        '''
        if self.use_residual:
            if self.registered_input is None:
                raise ValueError(
                    "Input tensor is not registered for residual connection.")
            return y + self.registered_input
        else:
            return y
