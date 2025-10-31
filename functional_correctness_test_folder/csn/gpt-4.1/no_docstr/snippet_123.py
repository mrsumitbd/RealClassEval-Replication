
import multiprocessing
import io


class MultiprocessingStringIO:
    def __init__(self):
        self._queue = multiprocessing.Queue()
        self._lock = multiprocessing.Lock()

    def getvalue(self):
        with self._lock:
            items = []
            while not self._queue.empty():
                items.append(self._queue.get())
            # Put them back for future calls
            for item in items:
                self._queue.put(item)
            return ''.join(items)

    def writelines(self, content_list):
        with self._lock:
            for line in content_list:
                self._queue.put(str(line))
