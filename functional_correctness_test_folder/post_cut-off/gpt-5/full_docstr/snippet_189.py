class RateLimiter:
    '''Convenience class for enforcing rates in loops.'''

    def __init__(self, hz):
        '''
        Args:
            hz (int): frequency to enforce
        '''
        if hz is None or hz <= 0:
            raise ValueError("hz must be a positive number")
        self._period = 1.0 / float(hz)
        self._last = None

    def _now(self, env):
        for attr in ("monotonic", "time", "now"):
            fn = getattr(env, attr, None)
            if callable(fn):
                try:
                    return float(fn())
                except Exception:
                    pass
        try:
            import time as _time
            return _time.perf_counter()
        except Exception:
            import time as _time
            return _time.time()

    def _sleep(self, env, duration):
        if duration <= 0:
            return
        for attr in ("sleep", "wait"):
            fn = getattr(env, attr, None)
            if callable(fn):
                try:
                    fn(duration)
                    return
                except Exception:
                    pass
        import time as _time
        _time.sleep(duration)

    def sleep(self, env):
        '''Attempt to sleep at the specified rate in hz.'''
        now = self._now(env)
        if self._last is None:
            self._last = now
            return
        elapsed = now - self._last
        if elapsed < self._period:
            self._sleep(env, self._period - elapsed)
            # After sleeping, advance by exactly one period to maintain cadence
            self._last = self._last + self._period
        else:
            # We're behind schedule; resync to current time
            self._last = now
