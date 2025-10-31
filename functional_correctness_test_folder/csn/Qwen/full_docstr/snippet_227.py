
from dataclasses import dataclass, asdict, fields
import h5py
import json


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
        with h5py.File(file_name, 'w') as f:
            for field_name, value in asdict(self).items():
                if isinstance(value, (list, dict)):
                    f.create_dataset(
                        field_name, data=json.dumps(value).encode('utf-8'))
                else:
                    f.create_dataset(field_name, data=value)

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
        with h5py.File(file_name, 'r') as f:
            data = {}
            for field in fields(cls):
                value = f[field.name][()]
                if isinstance(value, bytes):
                    try:
                        value = json.loads(value.decode('utf-8'))
                    except json.JSONDecodeError:
                        pass
                data[field.name] = value
        return cls(**data)
