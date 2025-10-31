import time
import threading


class Reservoir:
    '''
    Keeps track of the number of sampled segments within
    a single second. This class is implemented to be
    thread-safe to achieve accurate sampling.
    '''

    def __init__(self, traces_per_sec=0):
        '''
        :param int traces_per_sec: number of guranteed
            sampled segments.
        '''
        self._traces_per_sec = max(0, int(traces_per_sec))
        self._lock = threading.Lock()
        self._current_sec = int(time.time())
        self._count = 0

    def take(self):
        '''
        Returns True if there are segments left within the
        current second, otherwise return False.
        '''
        now_sec = int(time.time())
        with self._lock:
            if now_sec != self._current_sec:
                self._current_sec = now_sec
                self._count = 0

            if self._count < self._traces_per_sec:
                self._count += 1
                return True

            return False
