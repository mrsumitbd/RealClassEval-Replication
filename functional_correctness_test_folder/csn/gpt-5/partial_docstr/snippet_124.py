import time


class DelayTimer:
    ''' Utility class that allows us to detect a certain
        time has passed'''

    def __init__(self, delay):
        self.delay = float(delay)
        self._next = time.monotonic() + self.delay

    def is_time(self):
        now = time.monotonic()
        if now >= self._next:
            self._next = now + self.delay
            return True
        return False
