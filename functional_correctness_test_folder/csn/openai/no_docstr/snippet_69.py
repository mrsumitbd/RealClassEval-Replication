
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def write(self, id, data):
        """Write data associated with the given id."""
        pass

    @abstractmethod
    def exists(self, id):
        """Return True if data for the given id exists, False otherwise."""
        pass

    @abstractmethod
    def max_file_idx(self):
        """Return the maximum file index currently stored."""
        pass
