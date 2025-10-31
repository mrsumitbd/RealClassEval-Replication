from io import StringIO

class ConsoleCapture:
    """A context manager to output into a string."""

    def __init__(self):
        self._saved_file = None
        self._buffer = None

    def __enter__(self):
        cflush()
        self._saved_file = console().file
        self._buffer = StringIO()
        console().file = self._buffer
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        console().file = self._saved_file

    @property
    def value(self):
        """Returns the captured text."""
        return self._buffer.getvalue()