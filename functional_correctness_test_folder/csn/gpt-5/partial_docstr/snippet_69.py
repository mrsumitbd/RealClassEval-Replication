from abc import ABC, abstractmethod
from typing import Any


class BaseStorage(ABC):
    '''Base class of backend storage'''

    @abstractmethod
    def write(self, id: str, data: Any) -> None:
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
        raise NotImplementedError
