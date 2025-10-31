
import time
import threading
from typing import Dict, Any


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
        self._next_possible_time = 0.0
        self._lock = threading.Lock()

    def register_next(self) -> float:
        '''Determines if next download request can start or not by returning the waiting time in seconds.'''
        with self._lock:
            now = time.time()
            if now >= self._next_possible_time:
                return 0.0
            return self._next_possible_time - now

    def update(self, headers: Dict[str, Any], *, default: float
