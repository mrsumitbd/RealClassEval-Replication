
from abc import ABC, abstractmethod


class ErrorHandler(ABC):

    @abstractmethod
    def can_handle(self, e):
        pass

    @abstractmethod
    def handle(self, e):
        pass
