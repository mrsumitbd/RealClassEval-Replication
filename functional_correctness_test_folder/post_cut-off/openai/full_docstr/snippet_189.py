
import time


class RateLimiter:
    '''Convenience class for enforcing rates in loops.'''

    def __init__(self, hz):
        '''
        Args:
            hz (int): frequency to enforce
        '''
        if hz <= 0:
            raise ValueError("hz must be a positive number")
        self.period = 1.0 / hz
        self._last_time = None

    def sleep(self, env):
        '''Attempt to sleep at the specified rate in hz.'''
        # If env is a SimPy environment (has .now and .timeout)
        if hasattr(env, "now") and hasattr(env, "timeout"):
            now = env.now
            if self._last_time is None:
                self._last_time = now
                return
            elapsed = now - self._last_time
            sleep_time = self.period - elapsed
            if sleep_time > 0:
                # In SimPy, yielding a timeout suspends the process
                yield env.timeout(sleep_time)
            self._last_time = env.now
        # Fallback to real time using time.sleep
        else:
            now = time.time()
            if self._last_time is None:
                self._last_time = now
                return
            elapsed = now - self._last_time
            sleep_time = self.period - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            self._last_time = time.time()
