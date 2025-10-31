
import time
from threading import Lock


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
        self.num_processes = num_processes
        self.minimum_wait_time = minimum_wait_time
        self.maximum_wait_time = maximum_wait_time
        self.next_request_time = [time.time()] * num_processes
        self.lock = Lock()

    def register_next(self) -> float:
        '''Determines if next download request can start or not by returning the waiting time in seconds.'''
        with self.lock:
            current_time = time.time()
            wait_times = [max(0, next_time - current_time)
                          for next_time in self.next_request_time]
            min_wait_time = min(wait_times)
            return min_wait_time

    def update(self, headers: dict, *, default: float) -> None:
        '''Update the next possible download time if the service has responded with the rate limit.
        :param headers: The headers that (may) contain information about waiting times.
        :param default: The default waiting time (in milliseconds) when retrying after getting a
            TOO_MANY_REQUESTS response without appropriate retry headers.
        '''
        with self.lock:
            retry_after = headers.get('Retry-After')
            if retry_after:
                try:
                    # Retry-After can be in seconds or a HTTP date
                    retry_after_seconds = float(retry_after)
                except ValueError:
                    # If it's not a float, it's likely a HTTP date, which we can't handle here
                    retry_after_seconds = default / 1000.0
            else:
                retry_after_seconds = default / 1000.0

            retry_after_seconds = max(self.minimum_wait_time, min(
                self.maximum_wait_time, retry_after_seconds))
            current_time = time.time()
            self.next_request_time = [current_time +
                                      retry_after_seconds] * self.num_processes
