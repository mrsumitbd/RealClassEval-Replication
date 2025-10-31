
from abc import ABC, abstractmethod


class SearchDumperExt(ABC):
    """Interface for Search dumper extensions."""

    @abstractmethod
    def dump(self, record, data):
        """Dump the data."""
        pass

    @abstractmethod
    def load(self, data, record_cls):
        """Load the data.
        Reverse the changes made by the dump method.
        """
        pass
