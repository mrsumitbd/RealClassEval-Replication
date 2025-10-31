import time
import threading
from typing import Optional


class TokenBucketRateLimiter:
    '''
    Token Bucket Rate Limiter Implementation
    The token bucket algorithm allows for a burst of traffic up to the bucket capacity,
    while maintaining a steady rate of token refill.
    '''

    def __init__(self, tokens_per_second: int, bucket_capacity: Optional[int] = None):
        '''
        Initialize token bucket rate limiter.
        Args:
            tokens_per_second: Rate at which tokens are refilled
            bucket_capacity: Maximum number of tokens in bucket (defaults to tokens_per_second)
        '''
        if tokens_per_second <= 0:
            raise ValueError("tokens_per_second must be > 0")
        if bucket_capacity is None:
            bucket_capacity = tokens_per_second
        if bucket_capacity <= 0:
            raise ValueError("bucket_capacity must be > 0")

        self.tokens_per_second: float = float(tokens_per_second)
        self.bucket_capacity: float = float(bucket_capacity)
        self._tokens: float = float(bucket_capacity)
        self._last_refill: float = time.monotonic()
        self._lock = threading.RLock()

    def _refill_tokens(self):
        '''Refill tokens based on time elapsed since last refill.'''
        now = time.monotonic()
        with self._lock:
            elapsed = now - self._last_refill
            if elapsed <= 0:
                return
            refill = elapsed * self.tokens_per_second
            if refill > 0:
                self._tokens = min(self.bucket_capacity, self._tokens + refill)
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
            missing = 1.0 - self._tokens
            return missing / self.tokens_per_second
