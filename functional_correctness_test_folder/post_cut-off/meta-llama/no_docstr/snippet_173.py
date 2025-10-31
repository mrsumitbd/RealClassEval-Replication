
class Clock:

    def __init__(self) -> None:
        """
        Initializes the Clock object.
        """
        self._time_ns = 0

    def update(self, ns: int) -> None:
        """
        Updates the current time by the given nanoseconds.

        Args:
        ns (int): The number of nanoseconds to add to the current time.
        """
        self._time_ns += ns

    @property
    def now_ns(self) -> int:
        """
        Gets the current time in nanoseconds.

        Returns:
        int: The current time in nanoseconds.
        """
        return self._time_ns

    @property
    def now_s(self) -> float:
        """
        Gets the current time in seconds.

        Returns:
        float: The current time in seconds.
        """
        return self._time_ns / 1e9


# Example usage:
def main():
    clock = Clock()
    print(clock.now_ns)  # Output: 0
    print(clock.now_s)   # Output: 0.0

    clock.update(1000000000)  # Update by 1 second
    print(clock.now_ns)  # Output: 1000000000
    print(clock.now_s)   # Output: 1.0


if __name__ == "__main__":
    main()
