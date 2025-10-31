from abc import ABC, abstractmethod
from typing import Any


class ErrorHandler(ABC):
    '''
    Custom error handler providing a response on a particular error.
    '''

    @abstractmethod
    def can_handle(self, e: Exception) -> bool:
        '''
        Indicator if the handler is able to handle the given exception `e`.
        :param e: The exception that shall be determined if can be handled by the handler.
        :return: True if the handler can/should handle the exception, otherwise False.
        '''
        raise NotImplementedError

    @abstractmethod
    def handle(self, e: Exception) -> Any:
        '''
        Handle the exception.
        :param e: The handled exception.
        :return: The error response for the exception.
        '''
        raise NotImplementedError
