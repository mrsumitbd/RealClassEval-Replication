
import os
from abc import ABC, abstractmethod
from typing import TextIO


class FileLikeIO(ABC):
    """Used by :class:`FileLike` to access low level file handle
    operations.
    """

    @abstractmethod
    def open(self, path: str, mode: str = "r") -> TextIO:
        """Return a file handle.

        For normal files, the implementation is::

            return open(path, mode)
        """
        return open(path, mode)

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Return ``True`` if the given path exists, otherwise ``False``."""
        return os.path.exists(path)

    @abstractmethod
    def remove(self, path: str) -> None:
        """Remove the file at the given path."""
        os.remove(path)
