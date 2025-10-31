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

    def __init__(self, dpath):
        '''
        Args:
            dpath (str | PathLike | None):
                The new directory to work in.
                If None, then the context manager is disabled.
        '''
        import os
        self._os = os
        self._dpath = dpath
        self._disabled = dpath is None
        self._prevdir = None

    def __enter__(self):
        '''
        Returns:
            ChDir: self
        '''
        if not self._disabled:
            self._prevdir = self._os.getcwd()
            self._os.chdir(self._os.fspath(self._dpath))
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
        if not self._disabled and self._prevdir is not None:
            self._os.chdir(self._prevdir)
        return False
