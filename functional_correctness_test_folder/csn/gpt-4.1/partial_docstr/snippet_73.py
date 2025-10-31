
import threading
import time


class SentinelHubRateLimit:

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
        self._next_time = time.time()

    def register_next(self) -> float:
        with self._lock:
            now = time.time()
            wait_time = max(self._next_time - now, 0)
            self._next_time = max(self._next_time, now) + \
                self.minimum_wait_time / self.num_processes
            return wait_time

    def update(self, headers: dict, *, default: float) -> None:
        '''Update the next possible download time if the service has responded with the rate limit.
        :param headers: The headers that (may) contain information about waiting times.
        :param default: The default waiting time (in milliseconds) when retrying after getting a
            TOO_MANY_REQUESTS response without appropriate retry headers.
        '''
        retry_after = None
        # Try to get retry-after from headers (case-insensitive)
        for key in headers:
            if key.lower() == "retry-after":
                retry_after = headers[key]
                break
            if key.lower() == "x-ratelimit-reset":
                retry_after = headers[key]
                break

        wait_seconds = None
        if retry_after is not None:
            try:
                wait_seconds = float(retry_after)
            except ValueError:
                try:
                    # Sometimes retry-after is a date, try to parse as timestamp
                    wait_seconds = max(0, time.mktime(time.strptime(
                        retry_after, "%a, %d %b %Y %H:%M:%S %Z")) - time.time())
                except Exception:
                    wait_seconds = None

        if wait_seconds is None:
            wait_seconds = float(default) / 1000.0

        wait_seconds = min(
            max(wait_seconds, self.minimum_wait_time), self.maximum_wait_time)

        with self._lock:
            self._next_time = max(self._next_time, time.time()) + wait_seconds
