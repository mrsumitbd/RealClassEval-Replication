class RateLimiter:
    def __init__(self, hz):
        if hz <= 0:
            raise ValueError("hz must be positive")
        self.period = 1.0 / hz
        self.last_time = None

    def sleep(self, env):
        now = env.now
        if self.last_time is None:
            self.last_time = now
            return
        elapsed = now - self.last_time
        if elapsed < self.period:
            yield env.timeout(self.period - elapsed)
        self.last_time = env.now
