
import torch


class CircularBuffer:

    def __init__(self, size: int, device: torch.device | None = None) -> None:
        self.size = size
        self.device = device
        self.buffer = None
        self.start = 0
        self.count = 0
        self.shape = None

    def append(self, value: torch.Tensor) -> None:
        if self.buffer is None:
            self.shape = value.shape
            self.buffer = torch.empty(
                (self.size,) + self.shape,
                dtype=value.dtype,
                device=self.device if self.device is not None else value.device
            )
        idx = (
            self.start + self.count) % self.size if self.count < self.size else self.start
        self.buffer[idx].copy_(value)
        if self.count < self.size:
            self.count += 1
        else:
            self.start = (self.start + 1) % self.size

    def get_array(self) -> torch.Tensor:
        if self.count == 0:
            return torch.empty((0,) + self.shape, device=self.device, dtype=self.buffer.dtype)
        if self.count < self.size:
            return self.buffer[:self.count]
        else:
            idxs = torch.arange(self.start, self.start + self.size) % self.size
            return self.buffer[idxs]

    @property
    def is_full(self) -> bool:
        return self.count == self.size
