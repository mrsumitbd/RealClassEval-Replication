from abc import ABCMeta, abstractmethod

class ErrorHandler:
    """
    Custom error handler providing a response on a particular error.
    """
    __metaclass__ = ABCMeta

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