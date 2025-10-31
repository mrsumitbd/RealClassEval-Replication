
import torch


class CircularBuffer:

    def __init__(self, size: int, device: torch.device | None = None) -> None:
        self.size = size
        self.buffer = torch.empty((size,), device=device)
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
