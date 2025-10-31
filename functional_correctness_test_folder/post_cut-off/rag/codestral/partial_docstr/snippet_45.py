
import time
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
        self.tokens_per_second = tokens_per_second
        self.bucket_capacity = bucket_capacity if bucket_capacity is not None else tokens_per_second
        self.tokens = self.bucket_capacity
        self.last_refill_time = time.time()

    def _refill_tokens(self):
        '''Refill tokens based on time elapsed since last refill.'''
        now = time.time()
        time_elapsed = now - self.last_refill_time
        tokens_to_add = time_elapsed * self.tokens_per_second
        self.tokens = min(self.tokens + tokens_to_add, self.bucket_capacity)
        self.last_refill_time = now

    def try_consume_token(self) -> bool:
        '''
        Try to consume a token from the bucket.
        Returns:
            True if token was consumed, False if bucket is empty
        '''
        self._refill_tokens()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def get_wait_time(self) -> float:
        '''
        Calculate how long to wait before a token will be available.
        Returns:
            Time in seconds to wait
        '''
        self._refill_tokens()
        if self.tokens >= 1:
            return 0.0
        return (1 - self.tokens) / self.tokens_per_second
