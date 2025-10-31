
import os
import tempfile


class ClosableNamedTemporaryFile:
    def __init__(self):
        # Create a temporary file that is not deleted automatically
        self._tmp = tempfile.NamedTemporaryFile(delete=False, mode='w+b')
        self.name = self._tmp.name
        self._closed = False

    def write(self, buf):
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        if isinstance(buf, str):
            buf = buf.encode()
        self._tmp.write(buf)

    def close(self):
        if not self._closed:
            try:
                self._tmp.close()
            finally:
                try:
                    os.remove(self.name)
                except FileNotFoundError:
                    pass
                self._closed = True

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
