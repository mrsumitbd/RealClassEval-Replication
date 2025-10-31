from pathlib import Path
from typing import List, Optional, Set, Tuple, Union
from iree.runtime import ParameterIndex, ParameterIndexEntry
from torch import nn
import torch

class ParameterArchiveBuilder:
    """Helper for building parameter archives from live modules."""

    def __init__(self):
        self._index = ParameterIndex()

    @property
    def index(self) -> ParameterIndex:
        return self._index

    def save(self, file_path: Union[str, Path]):
        """Saves the archive."""
        self._index.create_archive_file(str(file_path))

    def add_tensor(self, name: str, tensor: torch.Tensor):
        """Adds an named tensor to the archive."""
        metadata = _make_tensor_metadata(tensor)
        if len(tensor.shape) == 0:
            flat_array_np = tensor.detach().cpu().numpy().copy()
            host_array = flat_array_np
        else:
            flat_array = tensor.detach().flatten().contiguous().cpu().view(torch.uint8)
            host_array = flat_array.numpy()
        self._index.add_buffer(name, host_array, metadata=metadata)

    def add_module(self, module: nn.Module, *, prefix: str=''):
        """Adds all parameters and persistent buffers from a module hierarchy."""
        for name, t in _yield_saveable_tensors(module, prefix=prefix):
            self.add_tensor(name, t)

    def add_blob(self, key: str, blob):
        """Adds a raw blob to the index.

        The blob must be interpretable as a buffer.
        """
        self._index.add_buffer(key, blob)