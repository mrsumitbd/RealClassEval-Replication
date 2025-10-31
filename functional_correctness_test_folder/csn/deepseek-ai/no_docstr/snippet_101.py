
import tempfile
import os


class ClosableNamedTemporaryFile:

    def __init__(self):
        self._tempfile = tempfile.NamedTemporaryFile(delete=False)
        self._closed = False

    def write(self, buf):
        if not self._closed:
            return self._tempfile.write(buf)
        else:
            raise ValueError("I/O operation on closed file")

    def close(self):
        if not self._closed:
            self._tempfile.close()
            self._closed = True

    def __del__(self):
        if not self._closed:
            self._tempfile.close()
        if os.path.exists(self._tempfile.name):
            os.unlink(self._tempfile.name)
