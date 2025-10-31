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
        if not isinstance(size, int) or size <= 0:
            raise ValueError('size must be a positive integer')
        self.size: int = size
        self.buffer: torch.Tensor | None = None
        self.head: int = 0
        self.count: int = 0
        self.device: torch.device | None = device

    def append(self, value: torch.Tensor) -> None:
        '''Append a new value or batch of values to the buffer.
        Args:
            value: New tensor to store; can be a single sample (...,) or a batch (N, ...).
        '''
        if not isinstance(value, torch.Tensor):
            raise TypeError('value must be a torch.Tensor')

        # Initialize device from first append if not provided.
        if self.device is None:
            self.device = value.device

        # Initialize storage lazily on first append, using value shape/dtype.
        if self.buffer is None:
            sample_shape = value.shape  # treat as single sample on first append
            self.buffer = torch.empty(
                (self.size,) + sample_shape, dtype=value.dtype, device=self.device)
            self.head = 0
            self.count = 0

        # Determine if this is a single sample or a batch based on buffer shape.
        sample_shape = self.buffer.shape[1:]
        if value.shape == sample_shape:
            vals = value.unsqueeze(0)  # single sample
        elif value.dim() >= 1 and value.shape[1:] == sample_shape:
            vals = value  # batch of samples
        elif value.dim() == 0 and sample_shape == torch.Size():
            vals = value.view(1)  # scalar sample into scalar buffer
        else:
            raise ValueError(
                f'Value shape {tuple(value.shape)} is incompatible with buffer sample shape {tuple(sample_shape)}')

        # Ensure device and dtype match buffer.
        if vals.device != self.buffer.device or vals.dtype != self.buffer.dtype:
            vals = vals.to(device=self.buffer.device, dtype=self.buffer.dtype)

        B = vals.shape[0]
        if B == 0:
            return

        if B >= self.size:
            # Keep only the last `size` elements.
            self.buffer[:] = vals[-self.size:]
            self.head = 0
            self.count = self.size
            return

        # Write into buffer with wrap-around using at most two slices.
        n1 = min(B, self.size - self.head)
        self.buffer[self.head:self.head + n1] = vals[:n1]
        n2 = B - n1
        if n2 > 0:
            self.buffer[0:n2] = vals[n1:n1 + n2]

        self.head = (self.head + B) % self.size
        self.count = min(self.size, self.count + B)

    def get_array(self) -> torch.Tensor:
        '''Get the current buffer contents as a tensor.
        Returns:
            Tensor containing the buffered data in chron. order
        '''
        if self.count == 0:
            if self.buffer is None:
                dev = self.device if self.device is not None else torch.device(
                    'cpu')
                return torch.empty((0,), device=dev)
            return self.buffer[:0]
        if self.count < self.size:
            return self.buffer[:self.count]
        # Full buffer: concatenate tail and head to form chronological order.
        return torch.cat((self.buffer[self.head:], self.buffer[:self.head]), dim=0)

    @property
    def is_full(self) -> bool:
        '''Check if the buffer is full.'''
        return self.count == self.size
