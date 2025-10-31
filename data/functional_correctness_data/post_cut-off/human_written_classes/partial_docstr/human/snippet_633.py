import json
import torch
from iree.runtime import ParameterIndex, ParameterIndexEntry
import numpy as np

class ParameterArchiveEntry:
    """Wraps a raw ParameterIndexEntry with additional helpers."""

    def __init__(self, raw: ParameterIndexEntry):
        self.raw = raw

    @property
    def key(self) -> str:
        return self.raw.key

    def as_flat_tensor(self) -> torch.Tensor:
        """Accesses the contents as a uint8 flat tensor.

        If it is a splat, then the tensor will be a view of the splat pattern.

        Raises a ValueError on unsupported entries.
        """
        if self.raw.is_file:
            wrapper = np.asarray(self.raw.file_view)
        elif self.raw.is_splat:
            wrapper = np.array(self.raw.splat_pattern)
        else:
            raise ValueError(f'Unsupported ParameterIndexEntry: {self.raw}')
        return torch.from_numpy(wrapper)

    def as_tensor(self) -> torch.Tensor:
        """Returns a tensor viewed with appropriate shape/dtype from metadata.

        Raises a ValueError if unsupported.
        """
        metadata = self.raw.metadata.decode()
        if not metadata.startswith(_metadata_prefix):
            raise ValueError(f'No metadata for parameter entry {self.key}: Cannot convert to tensor')
        metadata = metadata[len(_metadata_prefix):]
        d = json.loads(metadata)
        try:
            type_name = d['type']
            if d['type'] != 'Tensor':
                raise ValueError(f"Metadata for parameter entry {self.key} is not a Tensor ('{type_name}')")
            dtype_name = d['dtype']
            shape = d['shape']
        except KeyError as e:
            raise ValueError(f'Bad metadata for parameter entry {self.key}') from e
        try:
            dtype = _name_to_dtype[dtype_name]
        except KeyError:
            raise ValueError(f"Unknown dtype name '{dtype_name}'")
        try:
            shape = [int(d) for d in shape]
        except ValueError as e:
            raise ValueError(f'Illegal shape for parameter entry {self.key}') from e
        t = self.as_flat_tensor()
        return t.view(dtype=dtype).view(shape)

    def __repr__(self):
        return f'ParameterArchiveEntry({self.raw}, metadata={self.raw.metadata})'