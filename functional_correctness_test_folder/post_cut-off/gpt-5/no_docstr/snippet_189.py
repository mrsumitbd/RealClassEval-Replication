class RateLimiter:
    def __init__(self, hz):
        if hz is None or hz <= 0:
            self._period = None
        else:
            self._period = 1.0 / float(hz)
        self._next_time = None

    def sleep(self, env):
        # No rate limiting requested
        if self._period is None:
            # If SimPy-like env, return an immediate timeout for composability
            if hasattr(env, "timeout"):
                return env.timeout(0)
            return None

        # Determine current time and create a sleeper depending on env type
        if hasattr(env, "now") and hasattr(env, "timeout"):
            # SimPy-like environment
            now = float(env.now)
            if self._next_time is None:
                self._next_time = now
            self._next_time += self._period
            delay = self._next_time - now
            if delay < 0:
                # Fell behind; reset schedule to now to avoid accumulating lag
                self._next_time = now
                delay = 0.0
            return env.timeout(delay)
        else:
            # Wall-clock fallback
            import time
            now = time.monotonic()
            if self._next_time is None:
                self._next_time = now
            self._next_time += self._period
            delay = self._next_time - now
            if delay > 0:
                time.sleep(delay)
            else:
                # Fell behind; reset to current time
                self._next_time = time.monotonic()
            return None
