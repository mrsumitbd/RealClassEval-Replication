
import os
from abc import ABC, abstractmethod


class FileLikeIO(ABC):
    '''Used by :class:`FileLike` to access low level file handle operations.'''

    @abstractmethod
    def open(self, path, mode='r'):
        '''Return a file handle.'''
        return open(path, mode)

    @abstractmethod
    def exists(self, path):
        '''Test whether a path exists.'''
        return os.path.exists(path)

    @abstractmethod
    def remove(self, path):
        '''Remove a file.'''
        os.remove(path)
