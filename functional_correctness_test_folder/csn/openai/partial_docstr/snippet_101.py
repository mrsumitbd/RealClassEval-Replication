
import os
import tempfile


class ClosableNamedTemporaryFile:
    def __init__(self):
        """Create a temporary file."""
        # Create a named temporary file that is not deleted on close
        self._tmp = tempfile.NamedTemporaryFile(delete=False, mode='w+b')
        self._path = self._tmp.name
        self._closed = False

    def write(self, buf):
        """Write `buf` to the file."""
        if self._closed:
            raise ValueError("I/O operation on closed file.")
        if isinstance(buf, str):
            buf = buf.encode()
        self._tmp.write(buf)

    def close(self):
        """Close the file and delete it."""
        if not self._closed:
            try:
                self._tmp.close()
            finally:
                try:
                    os.remove(self._path)
                except FileNotFoundError:
                    pass
                self._closed = True

    def __del__(self):
        """Ensure the file is cleaned up."""
        try:
            self.close()
        except Exception:
            # Suppress any exception during garbage collection
            pass
