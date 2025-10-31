
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    '''Base class of backend storage'''
    @abstractmethod
    def write(self, id, data):
        '''Abstract interface of writing data
        Args:
            id (str): unique id of the data in the storage.
            data (bytes or str): data to be stored.
        '''
        pass

    @abstractmethod
    def exists(self, id):
        '''Check the existence of some data
        Args:
            id (str): unique id of the data in the storage
        Returns:
            bool: whether the data exists
        '''
        pass

    @abstractmethod
    def max_file_idx(self):
        '''Get the max existing file index
        Returns:
            int: the max index
        '''
        pass
