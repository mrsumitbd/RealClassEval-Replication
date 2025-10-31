
import time
from typing import Any


class Stopwatch:
    """A class representing a stopwatch for measuring elapsed time.

    Attributes:
        elapsed (float): The elapsed time in seconds.
        is_running (bool): A flag indicating whether the stopwatch is running
    """

    def __init__(self) -> None:
        self.elapsed = 0.0
        self.is_running = False
        self.start_time = 0.0

    def __enter__(self) -> 'Stopwatch':
        """Enters a context block and starts the stopwatch.

        Returns:
            Stopwatch: The stopwatch instance.
        """
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Exits the context block and stops the stopwatch."""
        self.stop()

    def reset(self) -> None:
        """Resets the stopwatch by setting the elapsed time to zero and stopping it."""
        self.elapsed = 0.0
        self.is_running = False

    def start(self) -> None:
        """Starts the stopwatch by setting the start time and setting the 'is_running' flag to True."""
        if not self.is_running:
            self.start_time = time.time() - self.elapsed
            self.is_running = True

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        """Formats the elapsed time in seconds to a string representation.

        Args:
            elapsed_time (float): The elapsed time in seconds.

        Returns:
            str: The formatted elapsed time string.
        """
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = elapsed_time % 60
        if hours > 0:
            return f'{hours:02d}:{minutes:02d}:{seconds:05.2f}'
        elif minutes > 0:
            return f'{minutes:02d}:{seconds:05.2f}'
        else:
            return f'{seconds:.3f} seconds'

    def stop(self) -> None:
        """Stops the stopwatch by calculating the elapsed time and setting the 'is_running' flag to False."""
        if self.is_running:
            self.elapsed = time.time() - self.start_time
            self.is_running = False

    def __str__(self) -> str:
        """Returns a string representation of the elapsed time."""
        if self.is_running:
            elapsed_time = time.time() - self.start_time
        else:
            elapsed_time = self.elapsed
        return self._format_elapsed_time(elapsed_time)
