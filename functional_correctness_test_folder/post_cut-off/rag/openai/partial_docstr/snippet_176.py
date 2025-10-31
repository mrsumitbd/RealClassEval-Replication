
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
        if size <= 0:
            raise ValueError("size must be positive")
        self.size = size
        self.device = device or torch.device('cpu')
        # buffer will be created lazily on first append to preserve dtype
        self.buffer = None
        self.head = 0
        self.count = 0

    def append(self, value: torch.Tensor) -> None:
        '''Append a new value to the buffer.
        Args:
            value: New tensor to store
        '''
        if self.buffer is None:
            # create buffer with same dtype and shape as value
            shape = (self.size, *value.shape)
            self.buffer = torch.empty(
                shape, dtype=value.dtype, device=self.device)
        if value.shape != self.buffer.shape[1:]:
            raise ValueError(
                f"Appended tensor shape {value.shape} does not match buffer element shape {self.buffer.shape[1:]}")
        # write value at current head
        self.buffer[self.head] = value
        # advance head
        self.head = (self.head + 1) % self.size
        # update count
        if self.count < self.size:
            self.count += 1

    def get_array(self) -> torch.Tensor:
        '''Get the current buffer contents as a tensor.
        Returns:
            Tensor containing the buffered data in chronological order
        '''
        if self.buffer is None or self.count == 0:
            return torch.empty((0,), dtype=torch.float32, device=self.device)
        if self.count < self.size:
            # buffer not yet full, data is in order from 0 to count-1
            return self.buffer[:self.count]
        # buffer full: need to reorder from head to head+count-1
        # head points to next write position, so oldest element is at head
        start = self.head
        end = start + self.count
        if end <= self.size:
            # contiguous slice
            return self.buffer[start:end]
        else:
            # wrap around
            first_part = self.buffer[start:self.size]
            second_part = self.buffer[:end - self.size]
            return torch.cat([first_part, second_part], dim=0)

    @property
    def is_full(self) -> bool:
        '''Check if the buffer is full.'''
        return self.count == self.size
