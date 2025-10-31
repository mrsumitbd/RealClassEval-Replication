
from abc import ABC, abstractmethod


class ErrorHandler(ABC):
    '''
    Custom error handler providing a response on a particular error.
    '''
    @abstractmethod
    def can_handle(self, e):
        '''
        Indicator if the handler is able to handle the given exception `e`.
        :param e: The exception that shall be determined if can be handled by the handler.
        :return: `True` or `False` depending on whether the handler can/should handle the method.
        '''
        pass

    @abstractmethod
    def handle(self, e):
        '''
        Handle the exception.
        :param e: The handled exception.
        :return: The error response for the exception.
        '''
        pass


class SpecificErrorHandler(ErrorHandler):
    def __init__(self, exception_type, error_response):
        """
        Initialize the SpecificErrorHandler.

        :param exception_type: The type of exception this handler can handle.
        :param error_response: The response to return when handling the exception.
        """
        self.exception_type = exception_type
        self.error_response = error_response

    def can_handle(self, e):
        """
        Check if the given exception is of the type this handler is designed for.

        :param e: The exception to check.
        :return: True if the exception is of the correct type, False otherwise.
        """
        return isinstance(e, self.exception_type)

    def handle(self, e):
        """
        Handle the given exception by returning the predefined error response.

        :param e: The exception to handle.
        :return: The predefined error response.
        """
        return self.error_response


# Example usage
if __name__ == "__main__":
    # Create a handler for ValueError with a specific response
    value_error_handler = SpecificErrorHandler(
        ValueError, "Invalid value provided.")

    # Test the handler
    try:
        raise ValueError("Test value error")
    except Exception as e:
        if value_error_handler.can_handle(e):
            # Output: Invalid value provided.
            print(value_error_handler.handle(e))
        else:
            print("Cannot handle the exception.")
