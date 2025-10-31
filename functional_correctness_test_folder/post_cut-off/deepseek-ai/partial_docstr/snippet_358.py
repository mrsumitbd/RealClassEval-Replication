
import torch


class ResidualConnection:

    def __init__(self, use_residual: bool = False):
        '''
        Initialize the ResidualConnection.
        Args:
            use_residual (bool): If True, apply residual connection.
        '''
        self.use_residual = use_residual
        self.registered_x = None

    def register(self, x: torch.Tensor):
        '''
        Register the input tensor for residual connection.
        Args:
            x (torch.Tensor): The input tensor to be registered.
        '''
        if self.use_residual:
            self.registered_x = x

    def apply(self, y: torch.Tensor) -> torch.Tensor:
        '''
        Apply residual connection if registered input exists and use_residual is True.
        Args:
            y (torch.Tensor): The tensor to which residual connection may be applied.
        Returns:
            torch.Tensor: The result after applying residual connection (if applicable).
        '''
        if self.use_residual and self.registered_x is not None:
            # Ensure shapes match for residual connection
            if y.shape == self.registered_x.shape:
                return y + self.registered_x
            else:
                raise ValueError(
                    "Shapes of registered input and output do not match for residual connection.")
        return y
