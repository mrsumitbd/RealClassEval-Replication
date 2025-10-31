
import threading


class Reservoir:
    '''
    Keeps track of the number of sampled segments within
    a single second. This class is implemented to be
    thread-safe to achieve accurate sampling.
    '''

    def __init__(self, traces_per_sec=0):
        self.traces_per_sec = traces_per_sec
        self.count = 0
        self.lock = threading.Lock()

    def take(self):
        with self.lock:
            if self.count < self.traces_per_sec or self.traces_per_sec == 0:
                self.count += 1
                return True
            return False
