from abc import abstractmethod

class FileLikeIO:
    """Used by :class:`FileLike` to access low level file handle
    operations.
    """

    @abstractmethod
    def open(self, path, mode='r'):
        """Return a file handle

        For normal files, the implementation is:

        ```python
        return open(path, mode)
        ```
        """

    @abstractmethod
    def exists(self, path):
        """Test whether a path exists

        For normal files, the implementation is:

        ```python
        return os.path.exists(path)
        ```
        """

    @abstractmethod
    def remove(self, path):
        """Remove a file

        For normal files, the implementation is:

        ```python
        os.remove(path)
        ```
        """