
import time
from typing import Optional


class Stopwatch:
    """
    A class representing a stopwatch for measuring elapsed time.

    Attributes
    ----------
    elapsed : float
        The elapsed time in seconds.
    is_running : bool
        A flag indicating whether the stopwatch is running.
    """

    def __init__(self) -> None:
        self.elapsed: float = 0.0
        self.is_running: bool = False
        self._start_time: Optional[float] = None

    # ------------------------------------------------------------------
    # Context‑manager protocol
    # ------------------------------------------------------------------
    def __enter__(self) -> "Stopwatch":
        """Enters a context block and starts the stopwatch."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Exits the context block and stops the stopwatch."""
        self.stop()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """Resets the stopwatch by setting the elapsed time to zero and stopping it."""
        self.elapsed = 0.0
        self.is_running = False
        self._start_time = None

    def start(self) -> None:
        """Starts the stopwatch by setting the start time and setting the 'is_running' flag to True."""
        if not self.is_running:
            self._start_time = time.perf_counter()
            self.is_running = True

    def stop(self) -> None:
        """
        Stops the stopwatch by calculating the elapsed time and setting the 'is_running' flag to False.
        """
        if self.is_running and self._start_time is not None:
            self.elapsed += time.perf_counter() - self._start_time
            self.is_running = False
            self._start_time = None

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _format_elapsed_time(self, elapsed_time: float) -> str:
        """
        Formats the elapsed time in seconds to a string representation.

        Parameters
        ----------
        elapsed_time : float
            The elapsed time in seconds.

        Returns
        -------
        str
            The formatted elapsed time string.
        """
        # Use a simple human‑readable format: HH:MM:SS.mmm
        hours, rem = divmod(elapsed_time, 3600)
        minutes, rem = divmod(rem, 60)
        seconds, ms = divmod(rem, 1)
        ms = int(ms * 1000)

        if hours:
            return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{ms:03d}"
        elif minutes:
            return f"{int(minutes):02d}:{int(seconds):02d}.{ms:03d}"
        else:
            return f"{int(seconds):02d}.{ms:03d}"
