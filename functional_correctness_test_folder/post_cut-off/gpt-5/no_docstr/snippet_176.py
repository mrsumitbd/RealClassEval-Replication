import torch


class CircularBuffer:

    def __init__(self, size: int, device: torch.device | None = None) -> None:
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be a positive integer.")
        self.size = size
        self.device = device
        self._buffer: torch.Tensor | None = None
        self._write_idx: int = 0
        self._count: int = 0
        self._dtype: torch.dtype | None = None
        self._shape_tail: tuple[int, ...] | None = None

    def append(self, value: torch.Tensor) -> None:
        if not isinstance(value, torch.Tensor):
            raise TypeError("value must be a torch.Tensor")
        if self._buffer is None:
            self._dtype = value.dtype
            self._shape_tail = tuple(value.shape)
            dev = self.device if self.device is not None else value.device
            self.device = dev
            self._buffer = torch.empty(
                (self.size, *self._shape_tail), dtype=self._dtype, device=dev)
        else:
            if tuple(value.shape) != self._shape_tail:
                raise ValueError(
                    f"value shape {tuple(value.shape)} does not match buffer element shape {self._shape_tail}")
            if value.dtype != self._dtype:
                value = value.to(self._dtype)
            if value.device != self.device:
                value = value.to(self.device)

        # Write value
        self._buffer[self._write_idx] = value
        self._write_idx = (self._write_idx + 1) % self.size
        if self._count < self.size:
            self._count += 1

    def get_array(self) -> torch.Tensor:
        if self._buffer is None or self._count == 0:
            raise RuntimeError("Buffer is empty.")
        if self._count < self.size:
            return self._buffer[:self._count].clone()
        # full buffer: oldest at write_idx
        idx = self._write_idx
        return torch.cat((self._buffer[idx:], self._buffer[:idx]), dim=0).clone()

    @property
    def is_full(self) -> bool:
        return self._count == self.size
