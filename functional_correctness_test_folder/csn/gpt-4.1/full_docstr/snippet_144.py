
import os


class InGivenDirectory:
    '''Change directory to given directory for duration of ``with`` block.'''

    def __init__(self, path=None):
        '''Initialize directory context manager.'''
        if path is None:
            self.path = os.getcwd()
        else:
            self.path = path
        self._old_cwd = None

    def __enter__(self):
        '''Chdir to the managed directory, creating it if needed.'''
        self._old_cwd = os.getcwd()
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        os.chdir(self.path)
        return self.path

    def __exit__(self, exc, value, tb):
        '''Revert the working directory.'''
        if self._old_cwd is not None:
            os.chdir(self._old_cwd)
