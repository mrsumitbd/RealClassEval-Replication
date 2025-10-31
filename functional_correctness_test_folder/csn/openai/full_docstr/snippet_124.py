
import time


class DelayTimer:
    ''' Utility class that allows us to detect a certain
        time has passed'''

    def __init__(self, delay):
        ''' Initialise the time with delay of dt seconds
        Parameters
        ----------
        delay: float
            The number of seconds in the timer
        '''
        self.dt = float(delay)
        self._last = time.monotonic()

    def is_time(self):
        '''
        Returns true if more than self.dt seconds has passed
        since the initialization or last call of successful is_time()
        Returns
        -------
        ret: bool
             True if specified amout of time has passed since the
             initialization or last successful is_time() call
        '''
        now = time.monotonic()
        if now - self._last >= self.dt:
            self._last = now
            return True
        return False
