
import os
from pathlib import Path


class InGivenDirectory:
    """
    Context manager that temporarily changes the current working directory
    to the specified path and restores the original directory on exit.
    """

    def __init__(self, path=None):
        """
        Initialize the context manager.

        Parameters
        ----------
        path : str or pathlib.Path, optional
            The directory to switch to. If None, the current directory
            is left unchanged.
        """
        self.target_path = Path(
            path).expanduser() if path is not None else None
        self.original_cwd = None

    def __enter__(self):
        """
        Enter the context: change to the target directory.

        Returns
        -------
        InGivenDirectory
            The context manager instance.
        """
        if self.target_path is not None:
            # Store the original working directory
            self.original_cwd = Path(os.getcwd())
            # Resolve the target path to an absolute path
            resolved = self.target_path.resolve(strict=True)
            os.chdir(resolved)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context: restore the original working directory.

        Parameters
        ----------
        exc_type : type
            The exception type, if any.
        exc_val : Exception
            The exception instance, if any.
        exc_tb : traceback
            The traceback, if any.

        Returns
        -------
        bool
            False to propagate any exception that occurred.
        """
        if self.original_cwd is not None:
            os.chdir(self.original_cwd)
        # Returning False propagates any exception that occurred
        return False
