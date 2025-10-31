
import torch


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
        self.size = size
        self.device = device if device is not None else torch.device('cpu')
        self.buffer: torch.Tensor | None = None
        self.head = 0
        self.count = 0

    def append(self, value: torch.Tensor) -> None:
        '''Append a new value to the buffer.
        Args:
            value: New tensor to store
        '''
        if self.buffer is None:
            # Allocate buffer on first append
            shape = (self.size, *value.shape)
            self.buffer = torch.empty(
                shape, dtype=value.dtype, device=self.device)
        # Store the value
        self.buffer[self.head] = value.to(self.device)
        # Update head and count
        self.head = (self.head + 1) % self.size
        if self.count < self.size:
            self.count += 1

    def get_array(self) -> torch.Tensor:
        '''Get the current buffer contents as a tensor.
        Returns:
            Tensor containing the buffered data in chronological order
        '''
        if self.buffer is None or self.count == 0:
            return torch.empty((0,), device=self.device)
        if self.count < self.size:
            return self.buffer[:self.count].clone()
        # Buffer is full: need to reorder from oldest to newest
        return torch.cat([self.buffer[self.head:], self.buffer[:self.head]]).clone()

    @property
    def is_full(self) -> bool:
        '''Check if the buffer is full.'''
        return self.count == self.size
