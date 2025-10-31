
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
        self._buffer = None
        self._next_idx = 0
        self._count = 0
        self._shape = None
        self._dtype = None

    def append(self, value: torch.Tensor) -> None:
        value = value.detach().to(self.device)
        if self._buffer is None:
            self._shape = value.shape
            self._dtype = value.dtype
            self._buffer = torch.empty(
                (self.size, *self._shape), dtype=self._dtype, device=self.device)
        self._buffer[self._next_idx].copy_(value)
        self._next_idx = (self._next_idx + 1) % self.size
        if self._count < self.size:
            self._count += 1

    def get_array(self) -> torch.Tensor:
        if self._buffer is None or self._count == 0:
            return torch.empty((0,), device=self.device)
        if self._count < self.size:
            return self._buffer[:self._count].clone()
        else:
            idx = self._next_idx
            return torch.cat((self._buffer[idx:], self._buffer[:idx]), dim=0).clone()

    @property
    def is_full(self) -> bool:
        return self._count == self.size
