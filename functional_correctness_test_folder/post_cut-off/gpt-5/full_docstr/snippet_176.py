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

    def __init__(self, size: int, device: Optional[torch.device] = None) -> None:
        '''Initialize a circular buffer.
        Args:
            size: Maximum number of elements to store
            device: Device for tensor storage (CPU or GPU)
        '''
        if size <= 0:
            raise ValueError("size must be a positive integer")
        self.size: int = int(size)
        self.device: Optional[torch.device] = device
        self.buffer: Optional[torch.Tensor] = None
        self.head: int = 0
        self.count: int = 0
        self._value_shape: Optional[torch.Size] = None
        self._dtype: Optional[torch.dtype] = None

    def append(self, value: torch.Tensor) -> None:
        '''Append a new value to the buffer.
        Args:
            value: New tensor to store
        '''
        if not isinstance(value, torch.Tensor):
            raise TypeError("value must be a torch.Tensor")

        # Initialize storage on first append
        if self.buffer is None:
            self._value_shape = value.shape
            self._dtype = value.dtype
            dev = self.device if self.device is not None else value.device
            self.device = dev
            storage_shape = (self.size, *self._value_shape)
            self.buffer = torch.empty(
                storage_shape, dtype=self._dtype, device=dev)

        # Validate shape and dtype
        if value.shape != self._value_shape:
            raise ValueError(
                f"Inconsistent value shape {value.shape}, expected {self._value_shape}")
        if value.dtype != self._dtype:
            raise ValueError(
                f"Inconsistent dtype {value.dtype}, expected {self._dtype}")

        # Move to target device if needed
        if value.device != self.device:
            value = value.to(self.device)

        # Write into buffer
        self.buffer[self.head].copy_(value.detach())
        self.head = (self.head + 1) % self.size
        if self.count < self.size:
            self.count += 1

    def get_array(self) -> torch.Tensor:
        '''Get the current buffer contents as a tensor.
        Returns:
            Tensor containing the buffered data in chron. order
        '''
        if self.count == 0:
            # If uninitialized, create an empty tensor on CPU
            if self.buffer is None:
                return torch.empty((0,))
            # Return empty with correct trailing shape/device/dtype
            empty_shape = (0, *self._value_shape)
            return torch.empty(empty_shape, dtype=self._dtype, device=self.device)

        if self.count < self.size:
            return self.buffer[:self.count]

        # Buffer is full: return from head to end, then start to head
        first = self.buffer[self.head:]
        second = self.buffer[:self.head]
        return torch.cat((first, second), dim=0)

    @property
    def is_full(self) -> bool:
        '''Check if the buffer is full.'''
        return self.count == self.size
