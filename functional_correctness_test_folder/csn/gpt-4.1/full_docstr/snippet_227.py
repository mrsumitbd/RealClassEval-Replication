
from dataclasses import dataclass, asdict, fields
import h5py
import numpy as np


@dataclass
class TemplateFile:
    '''
    simple container to read and write
    the data to an hdf5 file
    '''

    def save(self, file_name: str):
        '''
        serialize the contents to a file
        :param file_name:
        :type file_name: str
        :returns:
        '''
        data = asdict(self)
        with h5py.File(file_name, 'w') as f:
            for key, value in data.items():
                if isinstance(value, (int, float, str, bool)):
                    f.attrs[key] = value
                elif isinstance(value, (list, tuple)):
                    arr = np.array(value)
                    f.create_dataset(key, data=arr)
                elif isinstance(value, np.ndarray):
                    f.create_dataset(key, data=value)
                elif value is None:
                    f.attrs[key] = 'None'
                else:
                    raise TypeError(
                        f"Unsupported type for field '{key}': {type(value)}")

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
        kwargs = {}
        with h5py.File(file_name, 'r') as f:
            for field in fields(cls):
                key = field.name
                if key in f.attrs:
                    val = f.attrs[key]
                    # h5py returns bytes for strings
                    if isinstance(val, bytes):
                        val = val.decode()
                    if val == 'None':
                        val = None
                    kwargs[key] = val
                elif key in f:
                    arr = f[key][()]
                    # Convert 0-dim arrays to scalars
                    if isinstance(arr, np.ndarray) and arr.shape == ():
                        arr = arr.item()
                    # Convert to list if original type was list or tuple
                    if field.type in (list, tuple):
                        arr = arr.tolist()
                        if field.type is tuple:
                            arr = tuple(arr)
                    kwargs[key] = arr
                else:
                    kwargs[key] = None
        return cls(**kwargs)
