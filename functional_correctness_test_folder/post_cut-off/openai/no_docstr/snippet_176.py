
import torch
from typing import List, Optional


class CircularBuffer:
    def __init__(self, size: int, device: torch.device | None = None) -> None:
        if size <= 0:
            raise ValueError("size must be a positive integer")
        self.size: int = size
        self.device: Optional[torch.device] = device
        self.buffer: List[Optional[torch.Tensor]] = [None] * size
        self.next_idx: int = 0
        self.count: int = 0
        self._elem_shape: Optional[torch.Size] = None

    def append(self, value: torch.Tensor) -> None:
        if self.device is not None:
            value = value.to(self.device)
        if self._elem_shape is None:
            self._elem_shape = value.shape
        elif value.shape != self._elem_shape:
            raise ValueError(
                f"All elements must have the same shape. "
                f"Expected {self._elem_shape}, got {value.shape}"
            )
        self.buffer[self.next_idx] = value
        self.next_idx = (self.next_idx + 1) % self.size
        if self.count < self.size:
            self.count += 1

    def get_array(self) -> torch.Tensor:
        if self.count == 0:
            return torch.empty((0, *self._elem_shape), device=self.device)
        if self.count < self.size:
            elems = self.buffer[: self.count]
        else:
            elems = self.buffer[self.next_idx:] + self.buffer[: self.next_idx]
        return torch.stack(elems, dim=0)

    @property
    def is_full(self) -> bool:
        return self.count == self.size
