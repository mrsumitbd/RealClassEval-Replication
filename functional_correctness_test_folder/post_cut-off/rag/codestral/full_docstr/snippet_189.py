
import time


class RateLimiter:
    '''Convenience class for enforcing rates in loops.'''

    def __init__(self, hz):
        '''
        Args:
            hz (int): frequency to enforce
        '''
        self.hz = hz
        self.period = 1.0 / hz
        self.last_time = time.time()

    def sleep(self, env):
        '''Attempt to sleep at the specified rate in hz.'''
        current_time = time.time()
        elapsed = current_time - self.last_time
        remaining = self.period - elapsed
        if remaining > 0:
            time.sleep(remaining)
        self.last_time = time.time()
