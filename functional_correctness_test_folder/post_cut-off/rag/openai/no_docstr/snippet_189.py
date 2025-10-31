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
        # Determine current time from the environment
        now = getattr(env, 'now', None)
        if now is None:
            # Fallback to real time if env has no 'now'
            import time
            now = time.time()

        if self.last_time is None:
            # First call: just record the time and return
            self.last_time = now
            return

        elapsed = now - self.last_time
        if elapsed < self.period:
            wait = self.period - elapsed
            # If env supports timeout (e.g., SimPy), use it
            if hasattr(env, 'timeout'):
                env.timeout(wait)
            else:
                # Fallback to real sleep
                import time
                time.sleep(wait)

        # Update last_time to the current time after sleeping
        self.last_time = getattr(env, 'now', None) or (
            lambda: __import__('time').time())()
