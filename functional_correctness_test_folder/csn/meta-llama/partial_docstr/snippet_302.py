
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


class ConcreteErrorHandler(ErrorHandler):
    def can_handle(self, e):
        return isinstance(e, Exception)

    def handle(self, e):
        error_response = {
            'error': str(e),
            'type': type(e).__name__
        }
        return error_response


# Example usage:
if __name__ == "__main__":
    try:
        raise ValueError("Invalid value")
    except Exception as e:
        handler = ConcreteErrorHandler()
        if handler.can_handle(e):
            error_response = handler.handle(e)
            print(error_response)
        else:
            print("Cannot handle the exception")
