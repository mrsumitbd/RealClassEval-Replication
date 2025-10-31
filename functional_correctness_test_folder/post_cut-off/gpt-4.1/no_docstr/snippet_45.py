
import time
from typing import Optional


class TokenBucketRateLimiter:

    def __init__(self, tokens_per_second: int, bucket_capacity: Optional[int] = None):
        self.tokens_per_second = tokens_per_second
        self.bucket_capacity = bucket_capacity if bucket_capacity is not None else tokens_per_second
        self.tokens = float(self.bucket_capacity)
        self.last_refill = time.monotonic()

    def _refill_tokens(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        refill = elapsed * self.tokens_per_second
        if refill > 0:
            self.tokens = min(self.bucket_capacity, self.tokens + refill)
            self.last_refill = now

    def try_consume_token(self) -> bool:
        self._refill_tokens()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def get_wait_time(self) -> float:
        self._refill_tokens()
        if self.tokens >= 1:
            return 0.0
        needed = 1 - self.tokens
        return needed / self.tokens_per_second
