
import time
import random


class Reservoir:

    def __init__(self, traces_per_sec=0):
        self.traces_per_sec = traces_per_sec
        self.last_call_time = time.time()
        self.interval = 1.0 / \
            self.traces_per_sec if self.traces_per_sec > 0 else float('inf')

    def take(self):
        current_time = time.time()
        if current_time - self.last_call_time >= self.interval:
            self.last_call_time = current_time
            return True
        return False
