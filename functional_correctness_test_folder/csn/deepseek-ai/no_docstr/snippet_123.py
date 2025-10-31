
import io
from multiprocessing import Lock


class MultiprocessingStringIO:
    def __init__(self):
        self._buffer = io.StringIO()
        self._lock = Lock()

    def getvalue(self):
        with self._lock:
            return self._buffer.getvalue()

    def write(self, content):
        with self._lock:
            self._buffer.write(content)

    def writelines(self, content_list):
        with self._lock:
            self._buffer.writelines(content_list)
