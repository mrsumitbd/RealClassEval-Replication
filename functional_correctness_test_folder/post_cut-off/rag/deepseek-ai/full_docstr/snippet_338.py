
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
        self.lock = threading.Lock()
        self.calls = []

    def wait(self):
        '''
        Wait if necessary to respect the rate limit.
        '''
        with self.lock:
            now = time.time()
            # Remove calls older than the current period
            self.calls = [
                call for call in self.calls if call > now - self.period]

            if len(self.calls) >= self.max_calls:
                # Calculate the time to wait until the oldest call is outside the period
                oldest_call = self.calls[0]
                time_to_wait = oldest_call + self.period - now
                if time_to_wait > 0:
                    time.sleep(time_to_wait)
                    # Update the calls list after waiting
                    now = time.time()
                    self.calls = [
                        call for call in self.calls if call > now - self.period]

            # Add the current call time
            self.calls.append(time.time())
