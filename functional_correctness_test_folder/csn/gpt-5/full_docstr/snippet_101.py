import tempfile
import os
import atexit


class ClosableNamedTemporaryFile:
    '''Creates a temporary file that is not deleted when the file is closed.
    This allows the file to be opened with an exclusive lock, but used by other programs before
    it is deleted
    '''

    def __init__(self):
        '''Create a temporary file.'''
        tmp = tempfile.NamedTemporaryFile(mode='wb', delete=False)
        self._fh = tmp
        self.name = tmp.name
        self._closed = False
        atexit.register(self._cleanup)

    def write(self, buf):
        '''Write `buf` to the file.'''
        if self._fh is None or self._fh.closed:
            raise ValueError("I/O operation on closed file.")
        if isinstance(buf, str):
            buf = buf.encode('utf-8')
        self._fh.write(buf)
        self._fh.flush()

    def close(self):
        '''Closes the file, allowing it to be opened by other programs. Does not delete the file.'''
        if self._fh and not self._fh.closed:
            try:
                self._fh.flush()
                os.fsync(self._fh.fileno())
            except Exception:
                pass
            self._fh.close()
        self._closed = True

    def _cleanup(self):
        try:
            if self._fh and not self._fh.closed:
                self._fh.close()
        except Exception:
            pass
        try:
            if self.name and os.path.exists(self.name):
                os.remove(self.name)
        except Exception:
            pass

    def __del__(self):
        '''Deletes the temporary file.'''
        self._cleanup()
