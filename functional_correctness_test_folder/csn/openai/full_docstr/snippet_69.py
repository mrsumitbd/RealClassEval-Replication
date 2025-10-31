
import os
import pathlib
from abc import ABC, abstractmethod
from typing import Union


class BaseStorage(ABC):
    '''Base class of backend storage'''

    @abstractmethod
    def write(self, id: str, data: Union[bytes, str]) -> None:
        '''Abstract interface of writing data
        Args:
            id (str): unique id of the data in the storage.
            data (bytes or str): data to be stored.
        '''
        pass

    @abstractmethod
    def exists(self, id: str) -> bool:
        '''Check the existence of some data
        Args:
            id (str): unique id of the data in the storage
        Returns:
            bool: whether the data exists
        '''
        pass

    @abstractmethod
    def max_file_idx(self) -> int:
        '''Get the max existing file index
        Returns:
            int: the max index
        '''
        pass


class FileSystemStorage(BaseStorage):
    '''Concrete implementation of BaseStorage that stores data in a directory on disk.'''

    def __init__(self, root_dir: Union[str, pathlib.Path]) -> None:
        self.root = pathlib.Path(root_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    def _file_path(self, id: str) -> pathlib.Path:
        return self.root / id

    def write(self, id: str, data: Union[bytes, str]) -> None:
        path = self._file_path(id)
        mode = 'wb' if isinstance(data, bytes) else 'w'
        with path.open(mode) as f:
            f.write(data)

    def exists(self, id: str) -> bool:
        return self._file_path(id).exists()

    def max_file_idx(self) -> int:
        max_idx = 0
        for entry in self.root.iterdir():
            if entry.is_file():
                try:
                    idx = int(entry.name)
                    if idx > max_idx:
                        max_idx = idx
                except ValueError:
                    # ignore non-integer filenames
                    pass
        return max_idx
