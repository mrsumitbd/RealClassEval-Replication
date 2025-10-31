
import tempfile
import os


class ClosableNamedTemporaryFile:
    '''Creates a temporary file that is not deleted when the file is closed.
    This allows the file to be opened with an exclusive lock, but used by other programs before
    it is deleted
    '''

    def __init__(self):
        '''Create a temporary file.'''
        self._tempfile = tempfile.NamedTemporaryFile(delete=False)
        self.name = self._tempfile.name
        self._closed = False

    def write(self, buf):
        '''Write `buf` to the file.'''
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        return self._tempfile.write(buf)

    def close(self):
        '''Closes the file, allowing it to be opened by other programs. Does not delete the file.'''
        if not self._closed:
            self._tempfile.close()
            self._closed = True

    def __del__(self):
        '''Deletes the temporary file.'''
        try:
            if hasattr(self, 'name') and self.name and os.path.exists(self.name):
                os.unlink(self.name)
        except Exception:
            pass
