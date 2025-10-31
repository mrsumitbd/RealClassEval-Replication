
import os
from typing import Optional, Union


class ChDir:
    '''
    Context manager that changes the current working directory and then
    returns you to where you were.
    This is nearly the same as the stdlib :func:`contextlib.chdir`, with the
    exception that it will do nothing if the input path is None (i.e. the user
    did not want to change directories).
    SeeAlso:
        :func:`contextlib.chdir`
    Example:
        >>> import ubelt as ub
        >>> dpath = ub.Path.appdir('ubelt/tests/chdir').ensuredir()
        >>> dir1 = (dpath / 'dir1').ensuredir()
        >>> dir2 = (dpath / 'dir2').ensuredir()
        >>> with ChDir(dpath):
        >>>     assert ub.Path.cwd() == dpath
        >>>     # change to the given directory, and then returns back
        >>>     with ChDir(dir1):
        >>>         assert ub.Path.cwd() == dir1
        >>>         with ChDir(dir2):
        >>>             assert ub.Path.cwd() == dir2
        >>>             # changes inside the context manager will be reset
        >>>             os.chdir(dpath)
        >>>         assert ub.Path.cwd() == dir1
        >>>     assert ub.Path.cwd() == dpath
        >>>     with ChDir(dir1):
        >>>         assert ub.Path.cwd() == dir1
        >>>         with ChDir(None):
        >>>             assert ub.Path.cwd() == dir1
        >>>             # When disabled, the cwd does *not* reset at context exit
        >>>             os.chdir(dir2)
        >>>         assert ub.Path.cwd() == dir2
        >>>         os.chdir(dir1)
        >>>         # Dont change dirs, but reset to your cwd at context end
        >>>         with ChDir('.'):
        >>>             os.chdir(dir2)
        >>>         assert ub.Path.cwd() == dir1
        >>>     assert ub.Path.cwd() == dpath
    '''

    def __init__(self, dpath: Optional[Union[str, os.PathLike]]):
        self.dpath = dpath
        self._original_cwd: Optional[str] = None

    def __enter__(self):
        if self.dpath is not None:
            # Save the current working directory
            self._original_cwd = os.getcwd()
            # Change to the new directory
            os.chdir(os.fspath(self.dpath))
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        # Only restore if we actually changed directories
        if self.dpath is not None and self._original_cwd is not None:
            os.chdir(self._original_cwd)
        # Returning False propagates any exception that occurred
        return False
