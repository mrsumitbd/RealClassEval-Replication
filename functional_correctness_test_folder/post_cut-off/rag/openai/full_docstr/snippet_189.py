
import time


class RateLimiter:
    '''Convenience class for enforcing rates in loops.'''

    def __init__(self, hz):
        '''
        Args:
            hz (int): frequency to enforce
        '''
        if hz <= 0:
            raise ValueError("hz must be positive")
        self._interval = 1.0 / hz
        self._last = None

    def sleep(self, env=None):
        '''Attempt to sleep at the specified rate in hz.'''
        now = time.time()
        if self._last is None:
            # First call – just record the time and return
            self._last = now
            return

        elapsed = now - self._last
        if elapsed < self._interval:
            # Sleep the remaining time to hit the target interval
            time.sleep(self._interval - elapsed)

        # Update the timestamp for the next call
        self._last = time.time()
