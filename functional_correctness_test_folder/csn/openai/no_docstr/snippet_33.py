
import sys
import traceback


class ExceptionHandler:
    """
    A simple exception handler that can be configured to handle a specific
    exception type. By default it handles all exceptions.
    """

    def __init__(self, exception_type=Exception):
        """
        :param exception_type: The exception type (or tuple of types) this handler
                               is interested in. Defaults to Exception, meaning
                               it will handle any exception.
        """
        self.exception_type = exception_type

    def wants(self, exc):
        """
        Return True if this handler is interested in handling the given exception.
        """
        return isinstance(exc, self.exception_type)

    def handle(self, exc):
        """
        Handle the exception by printing its traceback to stderr.
        Returns True to indicate the exception was handled.
        """
        traceback.print_exception(
            type(exc), exc, exc.__traceback__, file=sys.stderr)
        return True
