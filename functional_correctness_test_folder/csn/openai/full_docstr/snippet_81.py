
import os
from typing import Optional, Union, Any, Type


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

    def __init__(self, dpath: Optional[Union[str, os.PathLike]]) -> None:
        '''
        Args:
            dpath (str | PathLike | None):
                The new directory to work in.
                If None, then the context manager is disabled.
        '''
        self.dpath = os.fspath(dpath) if dpath is not None else None
        self._original_cwd: Optional[str] = None

    def __enter__(self) -> 'ChDir':
        '''
        Returns:
            ChDir: self
        '''
        if self.dpath is None:
            return self
        # Store the original working directory
        self._original_cwd = os.getcwd()
        # Change to the new directory
        os.chdir(self.dpath)
        return self

    def __exit__(self, ex_type: Optional[Type[BaseException]],
                 ex_value: Optional[BaseException],
                 ex_traceback: Optional[Any]) -> Optional[bool]:
        '''
        Args:
            ex_type (Type[BaseException] | None):
            ex_value (BaseException | None):
            ex_traceback (TracebackType | None):
        Returns:
            bool | None
        '''
        if self.dpath is None:
            return None
        # Restore the original working directory
        if self._original_cwd is not None:
            os.chdir(self._original_cwd)
        return None
