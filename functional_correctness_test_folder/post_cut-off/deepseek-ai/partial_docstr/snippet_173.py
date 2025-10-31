
class Clock:

    def __init__(self) -> None:
        '''Initialize the clock with a starting time of 0 nanoseconds.'''
        self._time_ns = 0

    def update(self, ns: int) -> None:
        '''Update the clock with a new time in nanoseconds.
        Args:
            ns (int): The new time in nanoseconds to set the clock to.
        Raises:
            ValueError: If the new time is not greater than or equal to the current time
        '''
        if ns < self._time_ns:
            raise ValueError(
                "New time must be greater than or equal to current time")
        self._time_ns = ns

    @property
    def now_ns(self) -> int:
        return self._time_ns

    @property
    def now_s(self) -> float:
        return self._time_ns / 1e9
