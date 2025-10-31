
import tempfile


class ClosableNamedTemporaryFile:

    def __init__(self):
        '''Create a temporary file.'''
        self.file = tempfile.NamedTemporaryFile(delete=False)
        self.closed = False

    def write(self, buf):
        '''Write `buf` to the file.'''
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        self.file.write(buf)

    def close(self):
        self.file.close()
        self.closed = True

    def __del__(self):
        if not self.closed:
            self.close()
