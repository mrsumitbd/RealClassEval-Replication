class RateLimiter:
    '''Convenience class for enforcing rates in loops.'''

    def __init__(self, hz):
        if hz is None or hz <= 0:
            raise ValueError("hz must be a positive number")
        self.hz = float(hz)
        self.period = 1.0 / self.hz
        self._next = None

    def sleep(self, env):
        if self._next is None:
            self._next = env.now
        self._next += self.period
        if self._next <= env.now:
            behind_periods = int((env.now - self._next) // self.period) + 1
            self._next += behind_periods * self.period
        return env.timeout(self._next - env.now)
