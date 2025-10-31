
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
        self.buffer = torch.empty(size, *value.shape[1:], device=device)
        self.head = 0
        self.count = 0
        self.device = device

    def append(self, value: torch.Tensor) -> None:
        '''Append a new value to the buffer.
        Args:
            value: New tensor to store
        '''
        if self.count < self.size:
            self.count += 1
        self.buffer[self.head] = value
        self.head = (self.head + 1) % self.size

    def get_array(self) -> torch.Tensor:
        '''Get the current buffer contents as a tensor.
        Returns:
            Tensor containing the buffered data in chron. order
        '''
        if self.count < self.size:
            return self.buffer[:self.count]
        else:
            return torch.cat((self.buffer[self.head:], self.buffer[:self.head]))

    @property
    def is_full(self) -> bool:
        '''Check if the buffer is full.'''
        return self.count == self.size
