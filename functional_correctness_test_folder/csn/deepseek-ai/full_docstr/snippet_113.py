
import os
from abc import ABC, abstractmethod


class FileLikeIO(ABC):
    '''Used by :class:`FileLike` to access low level file handle
    operations.
    '''
    @abstractmethod
    def open(self, path, mode='r'):
        '''Return a file handle
        For normal files, the implementation is:
