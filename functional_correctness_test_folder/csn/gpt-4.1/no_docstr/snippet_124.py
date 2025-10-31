
import time


class DelayTimer:

    def __init__(self, delay):
        self.delay = delay
        self.start_time = time.time()

    def is_time(self):
        current_time = time.time()
        if current_time - self.start_time >= self.delay:
            self.start_time = current_time
            return True
        return False
