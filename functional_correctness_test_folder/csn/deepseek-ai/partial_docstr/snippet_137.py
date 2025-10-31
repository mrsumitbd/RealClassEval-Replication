
import threading


class Reservoir:
    '''
    Keeps track of the number of sampled segments within
    a single second. This class is implemented to be
    thread-safe to achieve accurate sampling.
    '''

    def __init__(self, traces_per_sec=0):
        self._traces_per_sec = traces_per_sec
        self._counter = 0
        self._lock = threading.Lock()

    def take(self):
        with self._lock:
            if self._traces_per_sec <= 0:
                return False
            if self._counter < self._traces_per_sec:
                self._counter += 1
                return True
            return False
