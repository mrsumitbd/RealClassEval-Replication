class RateLimiter:
    """Convenience class for enforcing rates in loops."""

    def __init__(self, hz):
        """
        Args:
            hz (int): frequency to enforce
        """
        if hz is None or hz <= 0:
            raise ValueError("hz must be a positive number")
        self._period = 1.0 / float(hz)
        self._next = None

    def _now(self, env):
        fn = getattr(env, "monotonic", None)
        if callable(fn):
            return fn()
        fn = getattr(env, "time", None)
        if callable(fn):
            return fn()
        fn = getattr(env, "now", None)
        if callable(fn):
            return fn()
        import time
        return time.monotonic()

    def _sleep(self, env, duration):
        if duration <= 0:
            return
        fn = getattr(env, "sleep", None)
        if callable(fn):
            fn(duration)
        else:
            import time
            time.sleep(duration)

    def sleep(self, env):
        """Attempt to sleep at the specified rate in hz."""
        now = self._now(env)
        if self._next is None:
            self._next = now + self._period
            return
        remaining = self._next - now
        if remaining > 0:
            self._sleep(env, remaining)
            now = self._now(env)
        if now >= self._next:
            self._next = now + self._period
        else:
            self._next += self._period
