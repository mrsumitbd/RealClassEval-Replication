
class ExceptionHandler:
    """
    A base class for handling exceptions.
    """

    def wants(self, exc):
        """
        Checks if this handler wants to handle the given exception.

        Args:
            exc (Exception): The exception to be handled.

        Returns:
            bool: True if this handler wants to handle the exception, False otherwise.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def handle(self, exc):
        """
        Handles the given exception.

        Args:
            exc (Exception): The exception to be handled.

        Returns:
            Any: The result of handling the exception.
        """
        raise NotImplementedError("Subclasses must implement this method")


# Example implementation of a concrete exception handler
class TypeErrorHandler(ExceptionHandler):
    def wants(self, exc):
        return isinstance(exc, TypeError)

    def handle(self, exc):
        # Handle TypeError
        print(f"Handling TypeError: {exc}")
        return None


# Example usage
if __name__ == "__main__":
    try:
        x = "hello"
        y = 5
        x + y  # This will raise a TypeError
    except Exception as e:
        handler = TypeErrorHandler()
        if handler.wants(e):
            handler.handle(e)
        else:
            print(f"Unhandled exception: {e}")
