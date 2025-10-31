
import time


class RateLimiter:
    '''Convenience class for enforcing rates in loops.'''

    def __init__(self, hz):
        '''
        Args:
            hz (int): frequency to enforce
        '''
        self.hz = hz
        self.interval = 1.0 / hz
        self.last_call = time.time()

    def sleep(self, env=None):
        '''Attempt to sleep at the specified rate in hz.'''
        now = time.time()
        elapsed = now - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.time()
