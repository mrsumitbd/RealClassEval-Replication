
import threading
import time


class SentinelHubRateLimit:
    '''Class implementing rate limiting logic of Sentinel Hub service
    It has 2 public methods:
    - register_next - tells if next download can start or if not, what is the wait before it can be asked again
    - update - updates expectations according to headers obtained from download
    The rate limiting object is collecting information about the status of rate limiting policy buckets from
    Sentinel Hub service. According to this information and a feedback from download requests it adapts expectations
    about when the next download attempt will be possible.
    '''

    def __init__(self, num_processes: int = 1, minimum_wait_time: float = 0.05, maximum_wait_time: float = 60.0):
        '''
        :param num_processes: Number of parallel download processes running.
        :param minimum_wait_time: Minimum wait time between two consecutive download requests in seconds.
        :param maximum_wait_time: Maximum wait time between two consecutive download requests in seconds.
        '''
        self.num_processes = max(1, int(num_processes))
        self.minimum_wait_time = float(minimum_wait_time)
        self.maximum_wait_time = float(maximum_wait_time)
        self._lock = threading.Lock()
        self._next_allowed_time = 0.0

    def register_next(self) -> float:
        '''Determines if next download request can start or not by returning the waiting time in seconds.'''
        with self._lock:
            now = time.time()
            wait = self._next_allowed_time - now
            if wait < 0:
                wait = 0.0
            # After registering, set the next allowed time
            self._next_allowed_time = max(
                self._next_allowed_time, now) + self.minimum_wait_time / self.num_processes
            return min(wait, self.maximum_wait_time)

    def update(self, headers: dict, *, default: float) -> None:
        '''Update the next possible download time if the service has responded with the rate limit.
        :param headers: The headers that (may) contain information about waiting times.
        :param default: The default waiting time (in milliseconds) when retrying after getting a
            TOO_MANY_REQUESTS response without appropriate retry headers.
        '''
        # Sentinel Hub may return 'Retry-After' or 'X-RateLimit-Reset' headers
        retry_after = headers.get('Retry-After')
        rate_limit_reset = headers.get('X-RateLimit-Reset')
        wait_time = None

        if retry_after is not None:
            try:
                wait_time = float(retry_after)
            except Exception:
                pass
        elif rate_limit_reset is not None:
            try:
                reset_time = float(rate_limit_reset)
                now = time.time()
                wait_time = max(0.0, reset_time - now)
            except Exception:
                pass

        if wait_time is None:
            # Use default, which is in milliseconds
            wait_time = float(default) / 1000.0

        wait_time = max(self.minimum_wait_time, min(
            wait_time, self.maximum_wait_time))

        with self._lock:
            now = time.time()
            self._next_allowed_time = max(
                self._next_allowed_time, now) + wait_time
