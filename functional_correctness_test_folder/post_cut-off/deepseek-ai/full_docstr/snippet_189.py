
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

    def sleep(self, env):
        '''Attempt to sleep at the specified rate in hz.'''
        elapsed = time.time() - self.last_time
        sleep_time = max(0.0, self.period - elapsed)
        time.sleep(sleep_time)
        self.last_time = time.time()
