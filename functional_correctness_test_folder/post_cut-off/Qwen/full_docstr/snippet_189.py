
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

    def sleep(self, env=None):
        '''Attempt to sleep at the specified rate in hz.'''
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        sleep_time = self.period - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)
        self.last_time = time.time()
