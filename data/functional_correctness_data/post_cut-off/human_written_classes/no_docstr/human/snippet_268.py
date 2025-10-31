import threading
import time

class TokenBucket:

    def __init__(self, rate_limit: float):
        self.rate_limit = rate_limit
        self.tokens = rate_limit
        self.last_update = time.time()
        self.lock = threading.Lock()

    def acquire(self) -> bool:
        with self.lock:
            now = time.time()
            new_tokens = (now - self.last_update) * self.rate_limit
            self.tokens = min(self.rate_limit, self.tokens + new_tokens)
            self.last_update = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False