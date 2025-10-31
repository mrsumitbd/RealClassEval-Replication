
class Clock:
    '''A simple clock class that tracks time in nanoseconds.'''

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
            raise ValueError("New time is less than the current time")
        self._time_ns = ns

    @property
    def now_ns(self) -> int:
        '''Get the current time in nanoseconds.'''
        return self._time_ns

    @property
    def now_s(self) -> float:
        '''Get the current time in seconds.'''
        return self._time_ns / 1e9


# Example usage:
def main():
    clock = Clock()
    print(clock.now_ns)  # Output: 0
    print(clock.now_s)   # Output: 0.0
    clock.update(1000000000)
    print(clock.now_ns)  # Output: 1000000000
    print(clock.now_s)   # Output: 1.0
    try:
        clock.update(500000000)
    except ValueError as e:
        print(e)  # Output: New time is less than the current time


if __name__ == "__main__":
    main()
