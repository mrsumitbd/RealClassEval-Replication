
import os


class InGivenDirectory:
    '''Change directory to given directory for duration of ``with`` block.'''

    def __init__(self, path=None):
        '''
        Parameters
        ----------
        path : None or str, optional
            path to change directory to, for duration of ``with`` block.
            Defaults to ``os.getcwd()`` if None
        '''
        if path is None:
            self._path = os.getcwd()
        else:
            self._path = path
        self._old_cwd = None

    def __enter__(self):
        self._old_cwd = os.getcwd()
        os.chdir(self._path)
        return self._path

    def __exit__(self, exc, value, tb):
        '''Revert the working directory.'''
        if self._old_cwd is not None:
            os.chdir(self._old_cwd)
