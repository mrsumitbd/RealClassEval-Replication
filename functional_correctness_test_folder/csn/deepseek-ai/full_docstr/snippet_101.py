
import tempfile
import os


class ClosableNamedTemporaryFile:
    '''Creates a temporary file that is not deleted when the file is closed.
    This allows the file to be opened with an exclusive lock, but used by other programs before
    it is deleted
    '''

    def __init__(self):
        '''Create a temporary file.'''
        self._file = tempfile.NamedTemporaryFile(delete=False)
        self.name = self._file.name

    def write(self, buf):
        '''Write `buf` to the file.'''
        self._file.write(buf)

    def close(self):
        '''Closes the file, allowing it to be opened by other programs. Does not delete the file.'''
        self._file.close()

    def __del__(self):
        '''Deletes the temporary file.'''
        if hasattr(self, '_file') and not self._file.closed:
            self._file.close()
        if hasattr(self, 'name') and os.path.exists(self.name):
            os.unlink(self.name)
