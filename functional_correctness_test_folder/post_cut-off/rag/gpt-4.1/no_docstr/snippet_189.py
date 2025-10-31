import time


class RateLimiter:
    '''Convenience class for enforcing rates in loops.'''

    def __init__(self, hz):
        '''
        Args:
            hz (int): frequency to enforce
        '''
        self.hz = hz
        self.period = 1.0 / hz if hz > 0 else 0
        self._last = None

    def sleep(self, env):
        '''Attempt to sleep at the specified rate in hz.'''
        now = time.time()
        if self._last is None:
            self._last = now
            return
        elapsed = now - self._last
        to_sleep = self.period - elapsed
        if to_sleep > 0:
            time.sleep(to_sleep)
            self._last = self._last + self.period
        else:
            self._last = now
