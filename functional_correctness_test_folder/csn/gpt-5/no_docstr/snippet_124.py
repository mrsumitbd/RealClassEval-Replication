import time


class DelayTimer:

    def __init__(self, delay):
        self.delay = float(delay)
        self._next = time.monotonic() + max(self.delay, 0.0)

    def is_time(self):
        if self.delay <= 0:
            return True
        now = time.monotonic()
        if now >= self._next:
            self._next = now + self.delay
            return True
        return False
