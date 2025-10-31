
import os
import tempfile


class ClosableNamedTemporaryFile:
    '''Creates a temporary file that is not deleted when the file is closed.
    This allows the file to be opened with an exclusive lock, but used by other programs before
    it is deleted
    '''

    def __init__(self):
        '''Create a temporary file.'''
        # Create a named temporary file that is not automatically deleted
        self._tmp = tempfile.NamedTemporaryFile(delete=False, mode='w+b')
        self.name = self._tmp.name
        self._closed = False

    def write(self, buf):
        '''Write `buf` to the file.'''
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        # Ensure bytes
        if isinstance(buf, str):
            buf = buf.encode()
        self._tmp.write(buf)

    def close(self):
        '''Closes the file, allowing it to be opened by other programs. Does not delete the file.'''
        if not self._closed:
            self._tmp.close()
            self._closed = True

    def __del__(self):
        '''Deletes the temporary file.'''
        try:
            # Ensure the file is closed
            if not self._closed:
                self.close()
            # Remove the file if it still exists
            if os.path.exists(self.name):
                os.remove(self.name)
        except Exception:
            # Suppress all exceptions in __del__
            pass
