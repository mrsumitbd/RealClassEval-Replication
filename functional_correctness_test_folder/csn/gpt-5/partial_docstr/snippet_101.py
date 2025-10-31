import os
import tempfile


class ClosableNamedTemporaryFile:

    def __init__(self):
        '''Create a temporary file.'''
        self._tmp = tempfile.NamedTemporaryFile(delete=False, mode='wb+')
        self.name = self._tmp.name
        self._closed = False
        self._unlinked = False

    def write(self, buf):
        '''Write `buf` to the file.'''
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        if isinstance(buf, str):
            buf = buf.encode('utf-8')
        self._tmp.write(buf)
        self._tmp.flush()

    def close(self):
        if not self._closed:
            try:
                self._tmp.close()
            finally:
                self._closed = True

    def __del__(self):
        try:
            if not self._closed:
                try:
                    self._tmp.close()
                except Exception:
                    pass
                self._closed = True
        except Exception:
            pass
        try:
            if not self._unlinked and hasattr(self, 'name') and self.name:
                try:
                    os.unlink(self.name)
                except FileNotFoundError:
                    pass
                except Exception:
                    pass
                finally:
                    self._unlinked = True
        except Exception:
            pass
