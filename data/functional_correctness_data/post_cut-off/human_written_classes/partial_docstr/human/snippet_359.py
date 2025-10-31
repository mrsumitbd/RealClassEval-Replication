import torch
from siirl.utils.extras.device import get_device_name
from typing import Dict, List, Optional

class MemoryBuffer:
    """
    A memory buffer is a contiguous torch tensor that may combine multiple tensors sharing with the underlying
    memory. It must have a unique type to support this behavior.
    """

    def __init__(self, numel: int, numel_padded: int, dtype: torch.dtype, source: Optional[torch.Tensor]=None):
        self.numel = numel
        self.numel_padded = numel_padded
        self.dtype = dtype
        if source is not None:
            self.data = source
        else:
            self.data = torch.zeros(self.numel_padded, dtype=self.dtype, device=get_device_name(), requires_grad=False)

    def zero(self):
        """Reset the buffer to zero."""
        self.data.zero_()

    def get(self, shape, start_index):
        """Return a tensor with the input `shape` as a view into the
        1-D data starting at `start_index`."""
        end_index = start_index + shape.numel()
        assert end_index <= self.numel, 'requested tensor is out of the buffer range.'
        buffer_tensor = self.data[start_index:end_index]
        buffer_tensor = buffer_tensor.view(shape)
        return buffer_tensor