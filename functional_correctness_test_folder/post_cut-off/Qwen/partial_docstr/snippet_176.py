
import torch


class CircularBuffer:

    def __init__(self, size: int, device: torch.device | None = None) -> None:
        self.size = size
        self.device = device if device is not None else torch.device('cpu')
        self.buffer = torch.empty((size,), device=self.device)
        self.head = 0
        self.count = 0

    def append(self, value: torch.Tensor) -> None:
        self.buffer[self.head] = value.to(self.device)
        self.head = (self.head + 1) % self.size
        if self.count < self.size:
            self.count += 1

    def get_array(self) -> torch.Tensor:
        if self.count == self.size:
            return self.buffer
        else:
            return self.buffer[:self.count]

    @property
    def is_full(self) -> bool:
        return self.count == self.size
