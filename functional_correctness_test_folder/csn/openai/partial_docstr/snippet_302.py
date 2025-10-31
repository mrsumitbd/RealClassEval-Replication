
from abc import ABC, abstractmethod


class ErrorHandler(ABC):
    """
    Base class for error handlers. Subclasses should implement the
    :py:meth:`can_handle` and :py:meth:`handle` methods to provide
    custom error handling logic.
    """

    @abstractmethod
    def can_handle(self, e):
        """
        Determine whether this handler can process the given exception.

        :param e: The exception instance to check.
        :return: ``True`` if the handler can process the exception,
                 ``False`` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def handle(self, e):
        """
        Handle the exception and produce an error response.

        :param e: The exception instance to handle.
        :return: The error response for the exception.
        """
        raise NotImplementedError
