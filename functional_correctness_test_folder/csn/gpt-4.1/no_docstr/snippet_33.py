
class ExceptionHandler:

    def wants(self, exc):
        """
        Returns True if this handler wants to handle the given exception.
        By default, handles all exceptions.
        """
        return True

    def handle(self, exc):
        """
        Handles the given exception.
        By default, just prints the exception.
        """
        print(f"Handled exception: {exc}")
