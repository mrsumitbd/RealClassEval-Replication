
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
        self.period = 1.0 / hz
        self.last_time = None

    def sleep(self, env):
        '''Attempt to sleep at the specified rate in hz.'''
        # Determine current time
        if hasattr(env, 'time'):
            now = env.time()
        else:
            now = time.time()

        if self.last_time is None:
            # First call: just record time
            self.last_time = now
            return

        elapsed = now - self.last_time
        if elapsed < self.period:
            # Need to sleep for the remaining period
            sleep_time = self.period - elapsed
            if hasattr(env, 'sleep'):
                env.sleep(sleep_time)
            else:
                time.sleep(sleep_time)
            # Update last_time after sleeping
            if hasattr(env, 'time'):
                self.last_time = env.time()
            else:
                self.last_time = time.time()
        else:
            # We're behind schedule; just update last_time
            self.last_time = now
