
from dataclasses import dataclass, field
from typing import Any, Dict
import h5py
import pickle
import numpy as np


@dataclass
class TemplateFile:
    """
    Simple container to read and write the data to an HDF5 file.
    The data is stored as a nested dictionary.
    """
    data: Dict[str, Any] = field(default_factory=dict)

    def _write_item(self, grp, key, value):
        """
        Write a single item to an HDF5 group.
        """
        if isinstance(value, dict):
            subgrp = grp.create_group(key)
            for k, v in value.items():
                self._write_item(subgrp, k, v)
        elif isinstance(value, (np.ndarray, list, tuple)):
            # Convert list/tuple to numpy array
            arr = np.array(value)
            grp.create_dataset(key, data=arr)
        else:
            # For other types, store pickled bytes
            grp.create_dataset(key, data=pickle.dumps(value))

    def _read_item(self, grp, key):
        """
        Read a single item from an HDF5 group.
        """
        obj = grp[key]
        if isinstance(obj, h5py.Group):
            return {k: self._read_item(obj, k) for k in obj}
        else:
            # Try to unpickle, fallback to raw data
            try:
                return pickle.loads(obj[()])
            except Exception:
                return obj[()]

    def save(self, file_name: str):
        """
        Serialize the contents to a file.
        """
        with h5py.File(file_name, 'w') as f:
            for k, v in self.data.items():
                self._write_item(f, k, v)

    @classmethod
    def from_file(cls, file_name: str):
        """
        Read contents from a file.
        """
        with h5py.File(file_name, 'r') as f:
            data = {k: cls._read_item(f, k) for k in f}
        return cls(data=data)
