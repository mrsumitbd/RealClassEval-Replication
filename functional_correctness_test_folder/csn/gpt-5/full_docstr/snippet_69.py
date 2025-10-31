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
        raise NotImplementedError

    @abstractmethod
    def exists(self, id: str) -> bool:
        '''Check the existence of some data
        Args:
            id (str): unique id of the data in the storage
        Returns:
            bool: whether the data exists
        '''
        raise NotImplementedError

    @abstractmethod
    def max_file_idx(self) -> int:
        '''Get the max existing file index
        Returns:
            int: the max index
        '''
        raise NotImplementedError
