
import os
from abc import abstractmethod


class FileLikeIO:
    '''Used by :class:`FileLike` to access low level file handle
    operations.
    '''
    @abstractmethod
    def open(self, path, mode='r'):
        '''Return a file handle
        For normal files, the implementation is:
