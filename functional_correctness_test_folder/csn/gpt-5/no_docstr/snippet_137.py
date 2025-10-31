class Reservoir:

    def __init__(self, traces_per_sec=0):
        import time
        self._rate = float(traces_per_sec)
        self._capacity = max(0.0, self._rate)
        self._tokens = self._capacity
        self._last = time.monotonic()
        self._time_fn = time.monotonic
        try:
            import threading
            self._lock = threading.Lock()
        except Exception:
            self._lock = None

    def take(self):
        if self._rate <= 0.0:
            return False
        if self._lock is None:
            return self._take_nolock()
        with self._lock:
            return self._take_nolock()

    def _take_nolock(self):
        now = self._time_fn()
        elapsed = max(0.0, now - self._last)
        self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
        self._last = now
        if self._tokens >= 1.0:
            self._tokens -= 1.0
            return True
        return False
