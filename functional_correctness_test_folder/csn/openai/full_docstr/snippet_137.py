
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
        :param int traces_per_sec: number of guaranteed
            sampled segments.
        '''
        self._traces_per_sec = int(traces_per_sec)
        self._lock = threading.Lock()
        self._last_second = int(time.time())
        self._remaining = self._traces_per_sec

    def take(self):
        '''
        Returns True if there are segments left within the
        current second, otherwise return False.
        '''
        with self._lock:
            now_sec = int(time.time())
            if now_sec != self._last_second:
                self._last_second = now_sec
                self._remaining = self._traces_per_sec

            if self._remaining > 0:
                self._remaining -= 1
                return True
            return False
