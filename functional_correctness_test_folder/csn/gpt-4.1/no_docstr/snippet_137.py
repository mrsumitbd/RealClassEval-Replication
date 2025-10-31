
class Reservoir:

    def __init__(self, traces_per_sec=0):
        import time
        self.traces_per_sec = traces_per_sec
        self.capacity = traces_per_sec
        self.tokens = self.capacity
        self.last_time = time.time()

    def take(self):
        import time
        now = time.time()
        if self.traces_per_sec == 0:
            return False
        # Refill tokens
        elapsed = now - self.last_time
        refill = elapsed * self.traces_per_sec
        if refill > 0:
            self.tokens = min(self.capacity, self.tokens + refill)
            self.last_time = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
