
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
        self.used = 0
        self.lock = threading.Lock()
        self.current_second = int(time.time())

    def take(self):
        '''
        Returns True if there are segments left within the
        current second, otherwise return False.
        '''
        with self.lock:
            now = int(time.time())
            if now != self.current_second:
                self.current_second = now
                self.used = 0

            if self.used < self.traces_per_sec:
                self.used += 1
                return True
            return False
