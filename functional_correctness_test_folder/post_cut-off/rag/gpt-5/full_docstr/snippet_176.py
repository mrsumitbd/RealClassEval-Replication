import torch
from typing import Optional


class CircularBuffer:
    '''Circular buffer for storing time series data.
    Provides a fixed-size circular buffer optimized for storing
    and retrieving time series data, with minimal memory allocation.
    Attributes:
        size: Maximum number of elements to store
        buffer: Storage for the data
        head: Current write position
        count: Number of elements currently stored
        device: Device where the buffer is stored
    '''

    def __init__(self, size: int, device: torch.device | None = None) -> None:
        '''Initialize a circular buffer.
        Args:
            size: Maximum number of elements to store
            device: Device for tensor storage (CPU or GPU)
        '''
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be a positive integer")
        self.size: int = int(size)
        self.device: Optional[torch.device] = device
        self.buffer: Optional[torch.Tensor] = None
        self.head: int = 0
        self.count: int = 0

    def append(self, value: torch.Tensor) -> None:
        '''Append a new value to the buffer.
        Args:
            value: New tensor to store
        '''
        if not isinstance(value, torch.Tensor):
            raise TypeError("value must be a torch.Tensor")

        # Lazy allocation on first append to avoid unnecessary memory allocation.
        if self.buffer is None:
            dev = self.device if self.device is not None else value.device
            self.buffer = torch.empty(
                (self.size,) + tuple(value.shape),
                dtype=value.dtype,
                device=dev,
            )
            # Set device attribute to actual storage device
            self.device = self.buffer.device
        else:
            if value.dtype != self.buffer.dtype:
                raise ValueError(
                    f"dtype mismatch: expected {self.buffer.dtype}, got {value.dtype}")
            if value.device != self.buffer.device:
                raise ValueError(
                    f"device mismatch: expected {self.buffer.device}, got {value.device}")
            if tuple(value.shape) != tuple(self.buffer.shape[1:]):
                raise ValueError(
                    f"shape mismatch: expected {tuple(self.buffer.shape[1:])}, got {tuple(value.shape)}"
                )

        # Write value into current head position
        self.buffer[self.head].copy_(value)
        # Advance head and update count
        self.head = (self.head + 1) % self.size
        if self.count < self.size:
            self.count += 1

    def get_array(self) -> torch.Tensor:
        '''Get the current buffer contents as a tensor.
        Returns:
            Tensor containing the buffered data in chron. order
        '''
        if self.count == 0 or self.buffer is None:
            dev = self.device if self.device is not None else torch.device(
                'cpu')
            return torch.empty((0,), device=dev)

        start = (self.head - self.count) % self.size
        end = (start + self.count)
        if end <= self.size:
            return self.buffer[start:end]
        else:
            first = self.buffer[start:]
            second = self.buffer[: (end % self.size)]
            return torch.cat((first, second), dim=0)

    @property
    def is_full(self) -> bool:
        '''Check if the buffer is full.'''
        return self.count == self.size
