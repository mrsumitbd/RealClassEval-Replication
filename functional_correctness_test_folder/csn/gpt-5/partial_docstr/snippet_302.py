from abc import ABC, abstractmethod
from typing import Any


class ErrorHandler(ABC):
    @abstractmethod
    def can_handle(self, e: Exception) -> bool:
        """
        Determine if this handler can handle the given exception.
        :param e: The exception to check.
        :return: True if the exception can be handled by this handler, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def handle(self, e: Exception) -> Any:
        """
        Handle the exception.
        :param e: The handled exception.
        :return: The error response for the exception.
        """
        raise NotImplementedError
