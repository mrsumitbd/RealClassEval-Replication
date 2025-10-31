import time
from threading import Lock


class Reservoir:
    '''
    Keeps track of the number of sampled segments within
    a single second. This class is implemented to be
    thread-safe to achieve accurate sampling.
    '''

    def __init__(self, traces_per_sec=0):
        self._limit = int(traces_per_sec) if traces_per_sec is not None else 0
        if self._limit < 0:
            self._limit = 0
        self._lock = Lock()
        self._second = None
        self._count = 0

    def take(self):
        now_sec = int(time.time())
        with self._lock:
            if self._limit <= 0:
                return False
            if self._second != now_sec:
                self._second = now_sec
                self._count = 0
            if self._count < self._limit:
                self._count += 1
                return True
            return False
