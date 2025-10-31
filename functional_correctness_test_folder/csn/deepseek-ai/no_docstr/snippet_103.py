
import contextlib
import io


class Reader:

    def __init__(self, stream):
        self.stream = stream
        self._captured_stream = None

    def readfmt(self, fmt):
        data = self.stream.read(fmt)
        return data

    @contextlib.contextmanager
    def capture(self, stream):
        old_stream = self.stream
        self.stream = stream
        try:
            yield
        finally:
            self.stream = old_stream
