
import time


class ExpiringCache:

    def __init__(self, seconds, timer=time.time):
        self.seconds = seconds
        self.timer = timer
        self._value = None
        self._expiry_time = 0

    def get(self):
        if self.timer() < self._expiry_time:
            return self._value
        return None

    def set(self, value):
        self._value = value
        self._expiry_time = self.timer() + self.seconds
