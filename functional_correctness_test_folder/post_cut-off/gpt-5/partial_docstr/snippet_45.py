from typing import Optional
import time
import threading


class TokenBucketRateLimiter:
    def __init__(self, tokens_per_second: int, bucket_capacity: Optional[int] = None):
        '''
        Initialize token bucket rate limiter.
        Args:
            tokens_per_second: Rate at which tokens are refilled
            bucket_capacity: Maximum number of tokens in bucket (defaults to tokens_per_second)
        '''
        if tokens_per_second <= 0:
            raise ValueError("tokens_per_second must be > 0")
        if bucket_capacity is not None and bucket_capacity <= 0:
            raise ValueError("bucket_capacity must be > 0 when provided")

        self._rate: float = float(tokens_per_second)
        self._capacity: float = float(
            bucket_capacity if bucket_capacity is not None else tokens_per_second)
        self._tokens: float = self._capacity
        self._last_refill: float = time.monotonic()
        self._lock = threading.Lock()

    def _refill_tokens(self):
        '''Refill tokens based on time elapsed since last refill.'''
        now = time.monotonic()
        elapsed = now - self._last_refill
        if elapsed <= 0:
            return
        new_tokens = elapsed * self._rate
        if new_tokens > 0:
            self._tokens = min(self._capacity, self._tokens + new_tokens)
            self._last_refill = now

    def try_consume_token(self) -> bool:
        '''
        Try to consume a token from the bucket.
        Returns:
            True if token was consumed, False if bucket is empty
        '''
        with self._lock:
            self._refill_tokens()
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True
            return False

    def get_wait_time(self) -> float:
        '''
        Calculate how long to wait before a token will be available.
        Returns:
            Time in seconds to wait
        '''
        with self._lock:
            self._refill_tokens()
            if self._tokens >= 1.0:
                return 0.0
            needed = 1.0 - self._tokens
            return needed / self._rate
