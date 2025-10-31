
import time
from datetime import datetime, timedelta


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
        self.next_possible_time = datetime.now()
        self.last_update_time = datetime.now()

    def register_next(self) -> float:
        '''Determines if next download request can start or not by returning the waiting time in seconds.'''
        current_time = datetime.now()
        if current_time < self.next_possible_time:
            wait_time = (self.next_possible_time -
                         current_time).total_seconds()
            return max(wait_time, self.minimum_wait_time)
        return 0.0

    def update(self, headers: dict, *, default: float) -> None:
        '''Update the next possible download time if the service has responded with the rate limit.
        :param headers: The headers that (may) contain information about waiting times.
        :param default: The default waiting time (in milliseconds) when retrying after getting a
            TOO_MANY_REQUESTS response without appropriate retry headers.
        '''
        current_time = datetime.now()
        self.last_update_time = current_time

        if 'X-RateLimit-Reset' in headers:
            reset_time = datetime.fromtimestamp(
                int(headers['X-RateLimit-Reset']))
            self.next_possible_time = max(self.next_possible_time, reset_time)
        elif 'Retry-After' in headers:
            # Convert milliseconds to seconds
            retry_after = float(headers['Retry-After']) / 1000.0
            self.next_possible_time = max(
                self.next_possible_time, current_time + timedelta(seconds=retry_after))
        else:
            default_wait_time = default / 1000.0  # Convert milliseconds to seconds
            self.next_possible_time = max(
                self.next_possible_time, current_time + timedelta(seconds=default_wait_time))

        self.next_possible_time = max(
            self.next_possible_time, current_time + timedelta(seconds=self.minimum_wait_time))
