
import time
import threading


class Reservoir:
    '''
    Keeps track of the number of sampled segments within
    a single second. This class is implemented to be
    thread-safe to achieve accurate sampling.
    '''

    def __init__(self, traces_per_sec=0):
        self.traces_per_sec = traces_per_sec
        self._lock = threading.Lock()
        self._last_second = int(time.time())
        self._count = 0

    def take(self):
        """
        Attempt to take a sample. Returns True if the sample
        is allowed under the per‑second limit, otherwise False.
        """
        with self._lock:
            now = int(time.time())
            if now != self._last_second:
                self._last_second = now
                self._count = 0

            if self.traces_per_sec <= 0:
                # Unlimited sampling
                return True

            if self._count < self.traces_per_sec:
                self._count += 1
                return True

            return False
