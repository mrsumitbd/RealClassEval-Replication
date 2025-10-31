
import os
from pathlib import Path


class ChDir:
    '''
    Context manager that changes the current working directory and then
    returns you to where you were.
    This is nearly the same as the stdlib :func:`contextlib.chdir`, with the
    exception that it will do nothing if the input path is None (i.e. the user
    did not want to change directories).
    SeeAlso:
        :func:`contextlib.chdir`
    '''

    def __init__(self, dpath):
        '''
        Args:
            dpath (str | PathLike | None):
                The new directory to work in.
                If None, then the context manager is disabled.
        '''
        self.dpath = Path(dpath) if dpath is not None else None
        self.original_cwd = None

    def __enter__(self):
        '''
        Returns:
            ChDir: self
        '''
        if self.dpath is not None:
            self.original_cwd = Path.cwd()
            os.chdir(self.dpath)
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        '''
        Args:
            ex_type (Type[BaseException] | None):
            ex_value (BaseException | None):
            ex_traceback (TracebackType | None):
        Returns:
            bool | None
        '''
        if self.original_cwd is not None:
            os.chdir(self.original_cwd)
        return None
