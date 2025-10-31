
import time
from threading import Lock


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
        self.lock = Lock()

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        with self.lock:
            now = time.time()
            # Remove calls that are outside the current period
            self.calls = [
                call for call in self.calls if call > now - self.period]

            if len(self.calls) >= self.max_calls:
                # Calculate the time to wait until the oldest call in the current period expires
                oldest_call = self.calls[0]
                wait_time = (oldest_call + self.period) - now
                if wait_time > 0:
                    time.sleep(wait_time)

            # Record the current call
            self.calls.append(time.time())
