
import tempfile
import os


class ClosableNamedTemporaryFile:

    def __init__(self):
        self._file = tempfile.NamedTemporaryFile(delete=False)
        self.name = self._file.name
        self._closed = False

    def write(self, buf):
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        return self._file.write(buf)

    def close(self):
        if not self._closed:
            try:
                self._file.close()
            finally:
                if os.path.exists(self.name):
                    os.unlink(self.name)
                self._closed = True

    def __del__(self):
        self.close()
