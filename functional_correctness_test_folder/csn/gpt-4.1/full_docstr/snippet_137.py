
import threading
import time


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
        self.traces_per_sec = traces_per_sec
        self._lock = threading.Lock()
        self._current_second = int(time.time())
        self._used = 0

    def take(self):
        '''
        Returns True if there are segments left within the
        current second, otherwise return False.
        '''
        now = int(time.time())
        with self._lock:
            if now != self._current_second:
                self._current_second = now
                self._used = 0
            if self._used < self.traces_per_sec:
                self._used += 1
                return True
            else:
                return False
