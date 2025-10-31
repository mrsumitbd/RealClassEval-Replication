class Clock:

    def __init__(self) -> None:
        '''Initialize the clock with a starting time of 0 nanoseconds.'''
        self._now_ns: int = 0

    def update(self, ns: int) -> None:
        '''Update the clock with a new time in nanoseconds.
        Args:
            ns (int): The new time in nanoseconds to set the clock to.
        Raises:
            ValueError: If the new time is not greater than or equal to the current time
        '''
        if ns < self._now_ns:
            raise ValueError(
                "New time must be greater than or equal to the current time.")
        self._now_ns = ns

    @property
    def now_ns(self) -> int:
        return self._now_ns

    @property
    def now_s(self) -> float:
        return self._now_ns / 1_000_000_000.0
