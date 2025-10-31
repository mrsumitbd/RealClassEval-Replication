
import time


class DelayTimer:
    def __init__(self, delay):
        self.delay = delay
        self.start = time.time()

    def is_time(self):
        return time.time() >= self.start + self.delay
