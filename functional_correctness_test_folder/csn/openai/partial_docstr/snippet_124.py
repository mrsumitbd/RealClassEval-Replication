
import time


class DelayTimer:
    '''Utility class that allows us to detect when a certain
    amount of time has passed since the timer was started or last reset.'''

    def __init__(self, delay: float):
        """
        Parameters
        ----------
        delay : float
            The delay in seconds that must elapse before `is_time` returns True.
        """
        self.delay = float(delay)
        self._start = time.monotonic()

    def is_time(self) -> bool:
        """
        Returns
        -------
        bool
            True if the configured delay has elapsed since the timer was
            created or last reset, False otherwise.
        """
        return (time.monotonic() - self._start) >= self.delay

    def reset(self) -> None:
        """
        Reset the timer to start counting from the current time.
        """
        self._start = time.monotonic()
