
import torch


class CircularBuffer:
    def __init__(self, size: int, device: torch.device | None = None) -> None:
        """
        Initialize a circular buffer.
        Args:
            size: Maximum number of elements to store
            device: Device for tensor storage (CPU or GPU)
        """
        self.size = size
        self.device = device if device is not None else torch.device("cpu")
        self.buffer: torch.Tensor | None = None
        self.idx = 0          # next write position
        self.count = 0        # number of elements currently stored
        self.shape = None     # shape of the tensors stored

    def append(self, value: torch.Tensor) -> None:
        if self.buffer is None:
            # Allocate buffer on first append
            self.shape = value.shape
            self.buffer = torch.empty(
                (self.size, *self.shape),
                dtype=value.dtype,
                device=self.device,
            )
        if self.count < self.size:
            self.buffer[self.idx] = value
            self.idx = (self.idx + 1) % self.size
            self.count += 1
        else:
            # Buffer is full; overwrite oldest element
            self.buffer[self.idx] = value
            self.idx = (self.idx + 1) % self.size

    def get_array(self) -> torch.Tensor:
        if self.buffer is None or self.count == 0:
            # Return an empty tensor with the correct dtype/device
            return torch.empty((0, *self.shape) if self.shape else (0,),
                               dtype=self.buffer.dtype if self.buffer else torch.float32,
                               device=self.device)
        if self.count < self.size:
            return self.buffer[:self.count]
        # Buffer is full; need to reorder from oldest to newest
        return torch.cat([self.buffer[self.idx:], self.buffer[:self.idx]], dim=0)

    @property
    def is_full(self) -> bool:
        return self.count == self.size
