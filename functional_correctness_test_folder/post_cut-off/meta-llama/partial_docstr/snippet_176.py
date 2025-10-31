
import torch


class CircularBuffer:

    def __init__(self, size: int, device: torch.device | None = None) -> None:
        '''Initialize a circular buffer.
        Args:
            size: Maximum number of elements to store
            device: Device for tensor storage (CPU or GPU)
        '''
        self.size = size
        self.device = device if device is not None else torch.device('cpu')
        self.buffer = torch.zeros(
            (size, *torch.tensor([]).shape), device=self.device)
        self.index = 0
        self.full = False

    def append(self, value: torch.Tensor) -> None:
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size
        if self.index == 0:
            self.full = True

    def get_array(self) -> torch.Tensor:
        if self.full:
            return self.buffer
        else:
            return self.buffer[:self.index]

    @property
    def is_full(self) -> bool:
        return self.full
