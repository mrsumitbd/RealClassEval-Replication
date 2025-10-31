
import torch


class CircularBuffer:

    def __init__(self, size: int, device: torch.device | None = None) -> None:
        self.size = size
        self.device = device
        self.buffer = None
        self.index = 0
        self.full = False

    def append(self, value: torch.Tensor) -> None:
        if self.buffer is None:
            self.buffer = torch.zeros(
                (self.size, *value.shape), dtype=value.dtype, device=self.device)
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size
        if self.index == 0:
            self.full = True

    def get_array(self) -> torch.Tensor:
        if not self.full and self.index == 0:
            return torch.tensor([], device=self.device)
        if self.full:
            return torch.cat((self.buffer[self.index:], self.buffer[:self.index]))
        else:
            return self.buffer[:self.index]

    @property
    def is_full(self) -> bool:
        return self.full
