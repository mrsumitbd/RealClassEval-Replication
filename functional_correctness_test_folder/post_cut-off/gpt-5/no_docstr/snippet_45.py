from typing import Optional
import time
import threading


class TokenBucketRateLimiter:
    def __init__(self, tokens_per_second: int, bucket_capacity: Optional[int] = None):
        if tokens_per_second <= 0:
            raise ValueError("tokens_per_second must be > 0")
        if bucket_capacity is None:
            bucket_capacity = tokens_per_second
        if bucket_capacity <= 0:
            raise ValueError("bucket_capacity must be > 0")
        self._rate = float(tokens_per_second)
        self._capacity = float(bucket_capacity)
        self._tokens = self._capacity
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill_tokens(self):
        now = time.monotonic()
        elapsed = now - self._last_refill
        if elapsed <= 0:
            self._last_refill = now
            return
        added = elapsed * self._rate
        if added > 0:
            self._tokens = min(self._capacity, self._tokens + added)
            self._last_refill = now

    def try_consume_token(self) -> bool:
        with self._lock:
            self._refill_tokens()
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True
            return False

    def get_wait_time(self) -> float:
        with self._lock:
            self._refill_tokens()
            if self._tokens >= 1.0:
                return 0.0
            needed = 1.0 - self._tokens
            return needed / self._rate
