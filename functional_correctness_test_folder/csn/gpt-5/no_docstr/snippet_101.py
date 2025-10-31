import os
import tempfile


class ClosableNamedTemporaryFile:

    def __init__(self):
        self._fp = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
        self.name = self._fp.name
        self._closed = False

    def write(self, buf):
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        if isinstance(buf, str):
            buf = buf.encode('utf-8')
        written = self._fp.write(buf)
        self._fp.flush()
        os.fsync(self._fp.fileno())
        return written

    def close(self):
        if not self._closed:
            try:
                self._fp.flush()
            except Exception:
                pass
            try:
                self._fp.close()
            finally:
                self._closed = True

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
        try:
            if self.name and os.path.exists(self.name):
                os.remove(self.name)
        except Exception:
            pass
