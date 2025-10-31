import time as _time


class RateLimiter:
    """Convenience class for enforcing rates in loops."""

    def __init__(self, hz):
        """
        Args:
            hz (int): frequency to enforce
        """
        self._period = 1.0 / float(hz) if hz and hz > 0 else None
        self._next_time = None

    def _now(self, env):
        n = getattr(env, "now", None)
        if callable(n):
            return float(n())
        if n is not None:
            return float(n)
        t = getattr(env, "time", None)
        if callable(t):
            return float(t())
        return float(_time.time())

    def _sleep(self, env, duration):
        s = getattr(env, "sleep", None)
        if callable(s) and duration > 0:
            s(duration)
        elif duration > 0:
            _time.sleep(duration)

    def sleep(self, env):
        """Attempt to sleep at the specified rate in hz."""
        now = self._now(env)

        if not self._period:
            self._next_time = now
            return 0.0

        if self._next_time is None:
            self._next_time = now + self._period
            return 0.0

        while self._next_time <= now:
            self._next_time += self._period

        delay = self._next_time - now
        if delay > 0:
            self._sleep(env, delay)
        return delay if delay > 0 else 0.0
