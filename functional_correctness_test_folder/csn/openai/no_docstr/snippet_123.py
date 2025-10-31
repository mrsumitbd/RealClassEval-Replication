
import multiprocessing


class MultiprocessingStringIO:
    def __init__(self):
        self._manager = multiprocessing.Manager()
        self._lines = self._manager.list()
        self._lock = self._manager.Lock()

    def getvalue(self):
        with self._lock:
            return ''.join(self._lines)

    def writelines(self, content_list):
        with self._lock:
            for line in content_list:
                self._lines.append(line)
