
import time


class DelayTimer:

    def __init__(self, delay):
        self.delay = delay
        self.start_time = time.time()

    def is_time(self):
        return time.time() - self.start_time >= self.delay
