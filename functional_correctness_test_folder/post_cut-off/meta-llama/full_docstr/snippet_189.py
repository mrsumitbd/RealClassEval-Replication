
import time


class RateLimiter:
    '''Convenience class for enforcing rates in loops.'''

    def __init__(self, hz):
        '''
        Args:
            hz (int): frequency to enforce
        '''
        self.period = 1.0 / hz
        self.last_time = time.time()

    def sleep(self):
        '''Attempt to sleep at the specified rate in hz.'''
        current_time = time.time()
        elapsed = current_time - self.last_time
        if elapsed < self.period:
            time.sleep(self.period - elapsed)
        self.last_time = time.time()
