class RateLimiter:
    """Convenience class for enforcing rates in loops."""

    def __init__(self, hz):
        """
        Args:
            hz (int): frequency to enforce
        """
        if hz <= 0:
            raise ValueError("hz must be > 0")
        self.hz = float(hz)
        self.period = 1.0 / self.hz
        self._next = None

    def sleep(self, env):
        """Attempt to sleep at the specified rate in hz."""
        now = env.time()
        if self._next is None:
            # Anchor the schedule to now, first sleep targets one period from now.
            self._next = now + self.period

        delay = self._next - now
        if delay > 0:
            env.sleep(delay)
            self._next += self.period
        else:
            # We're late; skip missed intervals and schedule the next one.
            # Find smallest k >= 1 such that _next + k*period > now.
            k = int((now - self._next) // self.period) + 1
            self._next += k * self.period
