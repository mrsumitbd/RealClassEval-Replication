
import time


class ExpiringCache:

    def __init__(self, seconds, timer=time.time):
        self.seconds = seconds
        self.timer = timer
        self.value = None
        self.expiration_time = None

    def get(self):
        if self.expiration_time is None or self.timer() > self.expiration_time:
            return None
        return self.value

    def set(self, value):
        self.value = value
        self.expiration_time = self.timer() + self.seconds
