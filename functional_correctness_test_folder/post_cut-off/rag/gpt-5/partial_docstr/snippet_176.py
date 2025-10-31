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
        self._item_shape: Optional[torch.Size] = None
        self._dtype: Optional[torch.dtype] = None

    def append(self, value: torch.Tensor) -> None:
        '''Append a new value to the buffer.
        Args:
            value: New tensor to store
        '''
        if not isinstance(value, torch.Tensor):
            raise TypeError("value must be a torch.Tensor")

        if self.buffer is None:
            self._item_shape = value.shape
            self._dtype = value.dtype
            if self.device is None:
                self.device = value.device
            self.buffer = torch.empty(
                (self.size,) + self._item_shape,
                dtype=self._dtype,
                device=self.device,
            )

        if value.shape != self._item_shape:
            raise ValueError(
                f"Incoming value shape {value.shape} does not match buffer item shape {self._item_shape}")

        # In-place copy to avoid extra allocation
        self.buffer[self.head].copy_(
            value.to(device=self.device, dtype=self._dtype))

        self.head = (self.head + 1) % self.size
        if self.count < self.size:
            self.count += 1

    def get_array(self) -> torch.Tensor:
        '''Get the current buffer contents as a tensor.
        Returns:
            Tensor containing the buffered data in chron. order
        '''
        if self.count == 0:
            dev = self.device if self.device is not None else torch.device(
                'cpu')
            if self._item_shape is None:
                return torch.empty((0,), device=dev)
            return torch.empty((0,) + self._item_shape, dtype=self._dtype, device=dev)

        assert self.buffer is not None
        if self.count < self.size:
            return self.buffer.narrow(0, 0, self.count)
        # Full buffer: oldest element is at head
        return torch.cat((self.buffer.narrow(0, self.head, self.size - self.head),
                          self.buffer.narrow(0, 0, self.head)), dim=0)

    @property
    def is_full(self) -> bool:
        '''Check if the buffer is full.'''
        return self.count == self.size
