
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
        self.current_count = 0
        self.last_reset_time = int(time.time())
        self.lock = threading.Lock()

    def take(self):
        '''
        Returns True if there are segments left within the
        current second, otherwise return False.
        '''
        with self.lock:
            current_time = int(time.time())
            if current_time != self.last_reset_time:
                self.last_reset_time = current_time
                self.current_count = 0

            if self.current_count < self.traces_per_sec:
                self.current_count += 1
                return True
            else:
                return False
