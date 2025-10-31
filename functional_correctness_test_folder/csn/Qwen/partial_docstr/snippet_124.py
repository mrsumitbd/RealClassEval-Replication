
import time


class DelayTimer:
    ''' Utility class that allows us to detect a certain
        time has passed'''

    def __init__(self, delay):
        self.delay = delay
        self.start_time = time.time()

    def is_time(self):
        return time.time() - self.start_time >= self.delay
