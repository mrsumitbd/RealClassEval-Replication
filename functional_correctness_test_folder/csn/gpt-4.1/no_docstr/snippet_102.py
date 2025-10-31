
import time


class ExpiringCache:

    def __init__(self, seconds, timer=time.time):
        self.seconds = seconds
        self.timer = timer
        self._value = None
        self._expire_at = None

    def get(self):
        if self._expire_at is None or self.timer() >= self._expire_at:
            self._value = None
            self._expire_at = None
            return None
        return self._value

    def set(self, value):
        self._value = value
        self._expire_at = self.timer() + self.seconds
