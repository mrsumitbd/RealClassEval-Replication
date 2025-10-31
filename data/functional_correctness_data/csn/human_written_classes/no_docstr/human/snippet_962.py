import time

class Stats:

    def __init__(self):
        self.init = time.time()
        self.requested = 0
        self.completed = 0
        self.retries = 0

    @property
    def duration(self):
        return time.time() - self.init

    @property
    def rate(self):
        return self.completed / self.duration