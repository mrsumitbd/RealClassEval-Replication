import os
import sys
from typing import Any

class SuppressOutput:
    """Context manager to suppress output in console or Jupyter notebook."""

    def __enter__(self) -> 'SuppressOutput':
        """Enter the context manager."""
        self._is_notebook = is_notebook()
        if self._is_notebook:
            from IPython.utils import io
            self._suppressor = io.capture_output()
            self._suppressor.__enter__()
        else:
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Exit the context manager."""
        if self._is_notebook:
            self._suppressor.__exit__(exc_type, exc_value, traceback)
        else:
            sys.stdout.close()
            sys.stdout = self._original_stdout