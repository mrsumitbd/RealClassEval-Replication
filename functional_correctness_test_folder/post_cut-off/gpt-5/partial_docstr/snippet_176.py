import torch
from typing import Optional, List


class CircularBuffer:

    def __init__(self, size: int, device: Optional[torch.device] = None) -> None:
        '''Initialize a circular buffer.
        Args:
            size: Maximum number of elements to store
            device: Device for tensor storage (CPU or GPU)
        '''
        if size <= 0:
            raise ValueError("size must be a positive integer")
        self.size = int(size)
        self.device: Optional[torch.device] = device
        self._buffer: List[Optional[torch.Tensor]] = [None] * self.size
        self._write_idx: int = 0
        self._count: int = 0
        self._shape: Optional[torch.Size] = None

    def append(self, value: torch.Tensor) -> None:
        if not isinstance(value, torch.Tensor):
            raise TypeError("value must be a torch.Tensor")
        if self.device is None:
            self.device = value.device
        if value.device != self.device:
            value = value.to(self.device)
        if self._shape is None:
            self._shape = value.shape
        elif value.shape != self._shape:
            raise ValueError(
                f"Inconsistent tensor shape. Expected {self._shape}, got {value.shape}")
        self._buffer[self._write_idx] = value
        self._write_idx = (self._write_idx + 1) % self.size
        if self._count < self.size:
            self._count += 1

    def get_array(self) -> torch.Tensor:
        if self._count == 0:
            dev = self.device if self.device is not None else torch.device(
                "cpu")
            return torch.empty((0,), device=dev)
        if self._count < self.size:
            elems = [self._buffer[i] for i in range(self._count)]
        else:
            start = self._write_idx
            elems = [self._buffer[(start + i) % self.size]
                     for i in range(self.size)]
        # elems are Optional[Tensor], but should be all filled here
        return torch.stack([e for e in elems if e is not None], dim=0)

    @property
    def is_full(self) -> bool:
        return self._count == self.size
