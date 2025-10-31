
import time
from typing import Optional


class Stopwatch:
    """
    A class representing a stopwatch for measuring elapsed time.

    Attributes:
        elapsed (float): The elapsed time in seconds.
        is_running (bool): A flag indicating whether the stopwatch is running.
    """

    def __init__(self) -> None:
        self.elapsed: float = 0.0
        self.is_running: bool = False
        self._start_time: Optional[float] = None

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------
    def __enter__(self) -> "Stopwatch":
        """
        Enters a context block and starts the stopwatch.

        Returns:
            Stopwatch: The stopwatch instance.
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits the context block and stops the stopwatch.
        """
        self.stop()

    # ------------------------------------------------------------------
    # Core stopwatch operations
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """
        Resets the stopwatch by setting the elapsed time to zero and stopping it.
        """
        self.elapsed = 0.0
        self.is_running = False
        self._start_time = None

    def start(self) -> None:
        """
        Starts the stopwatch by setting the start time and setting the
        'is_running' flag to True.
        """
        if not self.is_running:
            self._start_time = time.perf_counter()
            self.is_running = True

    def stop(self) -> None:
        """
        Stops the stopwatch by calculating the elapsed time and setting the
        'is_running' flag to False.
        """
        if self.is_running and self._start_time is not None:
            self.elapsed += time.perf_counter() - self._start_time
            self.is_running = False
            self._start_time = None

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def _format_elapsed_time(self, elapsed_time: float) -> str:
        """
        Formats the elapsed time in seconds to a string representation.

        Args:
            elapsed_time (float): The elapsed time in seconds.

        Returns:
            str: The formatted elapsed time string.
        """
        # Format to milliseconds precision, strip trailing zeros
        if elapsed_time < 1:
            # Show milliseconds
            return f"{elapsed_time * 1000:.3f} ms"
        elif elapsed_time < 60:
            return f"{elapsed_time:.3f} s"
        else:
            minutes = int(elapsed_time // 60)
            seconds = elapsed_time % 60
            return f"{minutes}m {seconds:.3f}s"
