
from abc import ABC, abstractmethod


class ErrorHandler(ABC):
    """
    Custom error handler providing a response on a particular error.
    """

    @abstractmethod
    def can_handle(self, e):
        """
        Indicator if the handler is able to handle the given exception `e`.

        :param e: The exception that shall be determined if can be handled by the handler.
        :return: `True` or `False` depending on whether the handler can/should handle the method.
        """
        pass

    @abstractmethod
    def handle(self, e):
        """
        Handle the exception.

        :param e: The handled exception.
        :return: The error response for the exception.
        """
        pass
