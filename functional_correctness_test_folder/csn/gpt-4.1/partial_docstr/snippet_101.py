
import tempfile
import os


class ClosableNamedTemporaryFile:

    def __init__(self):
        '''Create a temporary file.'''
        self._tmp = tempfile.NamedTemporaryFile(delete=False)
        self.name = self._tmp.name
        self._closed = False

    def write(self, buf):
        '''Write `buf` to the file.'''
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        return self._tmp.write(buf)

    def close(self):
        if not self._closed:
            try:
                self._tmp.close()
            finally:
                try:
                    os.unlink(self.name)
                except FileNotFoundError:
                    pass
                self._closed = True

    def __del__(self):
        self.close()
