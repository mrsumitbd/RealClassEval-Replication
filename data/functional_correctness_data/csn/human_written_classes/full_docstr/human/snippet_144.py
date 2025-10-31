import os

class InGivenDirectory:
    """Change directory to given directory for duration of ``with`` block.

    Useful when you want to use `InTemporaryDirectory` for the final test, but
    you are still debugging.  For example, you may want to do this in the end:

    >>> with InTemporaryDirectory() as tmpdir:
    ...     # do something complicated which might break
    ...     pass

    But indeed the complicated thing does break, and meanwhile the
    ``InTemporaryDirectory`` context manager wiped out the directory with the
    temporary files that you wanted for debugging.  So, while debugging, you
    replace with something like:

    >>> with InGivenDirectory() as tmpdir: # Use working directory by default
    ...     # do something complicated which might break
    ...     pass

    You can then look at the temporary file outputs to debug what is happening,
    fix, and finally replace ``InGivenDirectory`` with ``InTemporaryDirectory``
    again.
    """

    def __init__(self, path=None):
        """Initialize directory context manager.

        Parameters
        ----------
        path : None or str, optional
            path to change directory to, for duration of ``with`` block.
            Defaults to ``os.getcwd()`` if None
        """
        if path is None:
            path = os.getcwd()
        self.path = os.path.abspath(path)

    def __enter__(self):
        """Chdir to the managed directory, creating it if needed."""
        self._pwd = os.path.abspath(os.getcwd())
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        os.chdir(self.path)
        return self.path

    def __exit__(self, exc, value, tb):
        """Revert the working directory."""
        os.chdir(self._pwd)