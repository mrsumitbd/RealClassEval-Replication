import time

class SentinelHubRateLimit:
    """Class implementing rate limiting logic of Sentinel Hub service

    It has 2 public methods:

    - register_next - tells if next download can start or if not, what is the wait before it can be asked again
    - update - updates expectations according to headers obtained from download

    The rate limiting object is collecting information about the status of rate limiting policy buckets from
    Sentinel Hub service. According to this information and a feedback from download requests it adapts expectations
    about when the next download attempt will be possible.
    """
    RETRY_HEADER = 'Retry-After'
    UNITS_SPENT_HEADER = 'X-ProcessingUnits-Spent'

    def __init__(self, num_processes: int=1, minimum_wait_time: float=0.05, maximum_wait_time: float=60.0):
        """
        :param num_processes: Number of parallel download processes running.
        :param minimum_wait_time: Minimum wait time between two consecutive download requests in seconds.
        :param maximum_wait_time: Maximum wait time between two consecutive download requests in seconds.
        """
        self.wait_time = min(num_processes * minimum_wait_time, maximum_wait_time)
        self.next_download_time = time.monotonic()

    def register_next(self) -> float:
        """Determines if next download request can start or not by returning the waiting time in seconds."""
        current_time = time.monotonic()
        wait_time = max(self.next_download_time - current_time, 0)
        if wait_time == 0:
            self.next_download_time = max(current_time + self.wait_time, self.next_download_time)
        return wait_time

    def update(self, headers: dict, *, default: float) -> None:
        """Update the next possible download time if the service has responded with the rate limit.

        :param headers: The headers that (may) contain information about waiting times.
        :param default: The default waiting time (in milliseconds) when retrying after getting a
            TOO_MANY_REQUESTS response without appropriate retry headers.
        """
        retry_after: float = int(headers.get(self.RETRY_HEADER, default))
        retry_after = retry_after / 1000
        if retry_after:
            self.next_download_time = max(time.monotonic() + retry_after, self.next_download_time)