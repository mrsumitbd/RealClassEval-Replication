
import torch


class CircularBuffer:

    def __init__(self, size: int, device: torch.device | None = None) -> None:
        if device is None:
            device = torch.device('cpu')
        self.size = size
        self.device = device
        self.buffer = torch.zeros((size, ), device=device)
        self.index = 0
        self.is_buffer_full = False

    def append(self, value: torch.Tensor) -> None:
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size
        if not self.is_buffer_full and self.index == 0:
            self.is_buffer_full = True

    def get_array(self) -> torch.Tensor:
        if self.is_buffer_full:
            return self.buffer
        else:
            return self.buffer[:self.index]

    @property
    def is_full(self) -> bool:
        return self.is_buffer_full
