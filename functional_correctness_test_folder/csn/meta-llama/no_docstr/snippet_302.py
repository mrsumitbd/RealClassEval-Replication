
from abc import ABC, abstractmethod


class ErrorHandler(ABC):

    @abstractmethod
    def can_handle(self, e):
        pass

    @abstractmethod
    def handle(self, e):
        pass


class ConcreteErrorHandler(ErrorHandler):
    def __init__(self, error_type):
        """
        Initialize the ConcreteErrorHandler with a specific error type.

        Args:
        error_type (type): The type of error this handler can handle.
        """
        self.error_type = error_type

    def can_handle(self, e):
        """
        Check if the given exception is of the type this handler is designed for.

        Args:
        e (Exception): The exception to check.

        Returns:
        bool: True if the exception is of the correct type, False otherwise.
        """
        return isinstance(e, self.error_type)

    def handle(self, e):
        """
        Handle the given exception.

        Args:
        e (Exception): The exception to handle.

        Raises:
        TypeError: If the exception is not of the type this handler is designed for.
        """
        if not self.can_handle(e):
            raise TypeError(
                "This handler cannot handle this type of exception")
        # Implement your error handling logic here
        print(f"Handling {type(e).__name__}: {str(e)}")


# Example usage
if __name__ == "__main__":
    try:
        # Simulate an error
        raise ValueError("Invalid value")
    except Exception as e:
        # Create a handler for ValueError
        handler = ConcreteErrorHandler(ValueError)
        if handler.can_handle(e):
            handler.handle(e)
        else:
            print("No handler available for this type of exception")
