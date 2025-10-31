
import time


class ExpiringCache:

    def __init__(self, seconds, timer=time.time):
        self.seconds = seconds
        self.timer = timer
        self.value = None
        self.expiry = 0

    def get(self):
        if self.timer() < self.expiry:
            return self.value
        else:
            return None

    def set(self, value):
        self.value = value
        self.expiry = self.timer() + self.seconds
