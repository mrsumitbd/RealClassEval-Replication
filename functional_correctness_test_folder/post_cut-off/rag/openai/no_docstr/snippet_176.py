
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
        self.buffer: torch.Tensor | None = None
        self.head = 0
        self.count = 0

    def append(self, value: torch.Tensor) -> None:
        '''Append a new value to the buffer.
        Args:
            value: New tensor to store
        '''
        if self.buffer is None:
            # First element determines the shape of each entry
            shape = value.shape
            dtype = value.dtype
            self.buffer = torch.empty(
                (self.size, *shape), dtype=dtype, device=self.device)
        else:
            if value.shape != self.buffer.shape[1:]:
                raise ValueError(f"All appended tensors must have the same shape. "
                                 f"Expected {self.buffer.shape[1:]}, got {value.shape}")

        # Write the value at the current head position
        self.buffer[self.head].copy_(value.to(self.device))
        # Advance head
        self.head = (self.head + 1) % self.size
        # Update count
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
            # Buffer not yet full – data is contiguous from 0 to count-1
            return self.buffer[:self.count].clone()
        else:
            # Buffer full – need to reorder from head to end then start to head-1
            first_part = self.buffer[self.head:].clone()
            second_part = self.buffer[:self.head].clone()
            return torch.cat((first_part, second_part), dim=0)

    @property
    def is_full(self) -> bool:
        '''Check if the buffer is full.'''
        return self.count == self.size
