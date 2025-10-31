
import threading
import time


class Reservoir:
    '''
    Keeps track of the number of sampled segments within
    a single second. This class is implemented to be
    thread-safe to achieve accurate sampling.
    '''

    def __init__(self, traces_per_sec=0):
        self.traces_per_sec = traces_per_sec
        self._lock = threading.Lock()
        self._current_sec = int(time.time())
        self._count = 0

    def take(self):
        now_sec = int(time.time())
        with self._lock:
            if now_sec != self._current_sec:
                self._current_sec = now_sec
                self._count = 0
            if self.traces_per_sec == 0 or self._count < self.traces_per_sec:
                self._count += 1
                return True
            else:
                return False
