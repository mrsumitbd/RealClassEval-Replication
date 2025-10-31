
from abc import ABC, abstractmethod


class ErrorHandler(ABC):

    @abstractmethod
    def can_handle(self, e):
        """Return True if this handler can handle the exception `e`."""
        pass

    @abstractmethod
    def handle(self, e):
        """Handle the exception `e`."""
        pass
