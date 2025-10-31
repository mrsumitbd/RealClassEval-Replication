
import h5py
from dataclasses import dataclass, asdict


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
            for key, value in asdict(self).items():
                f.attrs[key] = value

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
            attrs = dict(f.attrs)
            return cls(**attrs)
