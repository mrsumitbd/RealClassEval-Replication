
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    '''Base class of backend storage'''

    @abstractmethod
    def write(self, id, data):
        '''Write data to storage'''
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
        '''Return the maximum file index in storage'''
        pass
