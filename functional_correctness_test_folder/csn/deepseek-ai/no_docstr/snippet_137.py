
class Reservoir:

    def __init__(self, traces_per_sec=0):
        self.traces_per_sec = traces_per_sec
        self.tokens = 0
        self.last_time = None

    def take(self):
        import time

        current_time = time.time()
        if self.last_time is None:
            self.last_time = current_time

        elapsed = current_time - self.last_time
        self.tokens += elapsed * self.traces_per_sec
        self.last_time = current_time

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        else:
            return False
