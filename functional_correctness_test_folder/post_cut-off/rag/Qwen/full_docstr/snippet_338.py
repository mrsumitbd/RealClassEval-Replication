
import time
import threading


class RateLimiter:
    '''Simple rate limiter to ensure we don't exceed API rate limits.'''

    def __init__(self, max_calls: int = 3, period: float = 1.0):
        '''
        Initialize the rate limiter.
        Args:
            max_calls: Maximum number of calls allowed in the period
            period: Time period in seconds
        '''
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = threading.Lock()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        with self.lock:
            current_time = time.time()
            self.calls = [
                t for t in self.calls if current_time - t < self.period]
            if len(self.calls) >= self.max_calls:
                time.sleep(self.period - (current_time - self.calls[0]))
            self.calls.append(time.time())
