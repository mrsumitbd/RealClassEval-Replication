
import time


class RateLimiter:
    '''Convenience class for enforcing rates in loops.'''

    def __init__(self, hz):
        if hz <= 0:
            raise ValueError("hz must be positive")
        self.period = 1.0 / hz
        self._last_time = None

    def sleep(self, env):
        """
        Enforce the desired rate by sleeping for the remaining time in the period.
        The `env` argument is expected to provide a `sleep(seconds)` method and
        optionally a `now` attribute that represents the current time (e.g. a
        simulation environment). If `env` does not provide a `now` attribute,
        the real wall‑clock time is used.
        """
        # Determine the current time
        if hasattr(env, 'now'):
            now = env.now
        else:
            now = time.time()

        if self._last_time is None:
            # First call: just record the time and return
            self._last_time = now
            return

        elapsed = now - self._last_time
        if elapsed < self.period:
            sleep_time = self.period - elapsed
            # Use the environment's sleep method if available
            if hasattr(env, 'sleep'):
                env.sleep(sleep_time)
            else:
                # Fallback to real time sleep
                time.sleep(sleep_time)
            # Update the last time after sleeping
            if hasattr(env, 'now'):
                self._last_time = env.now
            else:
                self._last_time = time.time()
        else:
            # No sleep needed; just update the last time
            self._last_time = now
