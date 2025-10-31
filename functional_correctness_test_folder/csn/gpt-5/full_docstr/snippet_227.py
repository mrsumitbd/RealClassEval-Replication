from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

import pickle


@dataclass
class TemplateFile:
    '''
    simple container to read and write
    the data to an hdf5 file
    '''
    data: Dict[str, Any] = field(default_factory=dict)

    def save(self, file_name: str):
        '''
        serialize the contents to a file
        :param file_name:
        :type file_name: str
        :returns:
        '''
        try:
            import h5py
        except Exception as e:
            raise RuntimeError("h5py is required to save to HDF5 files") from e

        def _write_value(group, name: str, value: Any):
            # Dictionaries become groups
            if isinstance(value, dict):
                subgrp = group.create_group(name)
                subgrp.attrs["__type__"] = "dict"
                for k, v in value.items():
                    _write_value(subgrp, str(k), v)
                return

            # Primitive or array-like via native h5py support
            try:
                group.create_dataset(name, data=value)
                return
            except Exception:
                pass

            # Fallback: pickle arbitrary Python objects as variable-length bytes
            try:
                dt = h5py.vlen_dtype(bytes)
                ds = group.create_dataset(name, data=pickle.dumps(
                    value, protocol=pickle.HIGHEST_PROTOCOL), dtype=dt)
                ds.attrs["__pickled__"] = True
            except Exception as e:
                raise TypeError(
                    f"Unable to serialize key '{name}' of type {type(value)}") from e

        with h5py.File(file_name, "w") as f:
            f.attrs["__templatefile__"] = True
            root = f.create_group("data")
            root.attrs["__type__"] = "dict"
            for k, v in self.data.items():
                _write_value(root, str(k), v)

    @classmethod
    def from_file(cls, file_name: str):
        '''
        read contents from a file
        :param cls:
        :type cls:
        :param file_name:
        :type file_name: str
        :returns:
        '''
        try:
            import h5py
        except Exception as e:
            raise RuntimeError("h5py is required to read HDF5 files") from e

        def _read_node(obj):
            # Group -> dict
            if isinstance(obj, h5py.Group):
                result = {}
                for name, item in obj.items():
                    result[name] = _read_node(item)
                return result

            # Dataset -> possibly pickled, else native value
            if isinstance(obj, h5py.Dataset):
                if obj.attrs.get("__pickled__", False):
                    raw = obj[()]
                    if isinstance(raw, (bytes, bytearray, memoryview)):
                        data_bytes = bytes(raw)
                    else:
                        data_bytes = bytes(raw)  # best-effort
                    return pickle.loads(data_bytes)
                else:
                    val = obj[()]
                    # Convert 0-dim numpy scalars to Python scalars if possible
                    try:
                        return val.item()
                    except Exception:
                        return val

            raise TypeError("Unsupported HDF5 object encountered")

        with h5py.File(file_name, "r") as f:
            if "data" not in f:
                # Backward/loose compatibility: read whole file root if not present
                root_group = f
            else:
                root_group = f["data"]

            contents = _read_node(root_group)
            # If root_group is 'data' with dict marker, contents is a dict of user data
            # If we read from file root, ensure dict type
            if isinstance(contents, dict):
                return cls(data=contents)
            else:
                return cls(data={"data": contents})
