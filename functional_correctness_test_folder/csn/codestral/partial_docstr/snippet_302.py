
from abc import ABC, abstractmethod


class ErrorHandler(ABC):

    @abstractmethod
    def can_handle(self, e):
        pass

    @abstractmethod
    def handle(self, e):
        '''
        Handle the exception.
        :param e: The handled exception.
        :return: The error response for the exception.
        '''
        pass
