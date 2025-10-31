
import time


class Stopwatch:
    """
    A simple stopwatch that can be used as a context manager or manually.
    """

    def __init__(self):
        self._start_time = None
        self._elapsed = 0.0
        self._running = False

    # Context manager protocol ------------------------------------------------
    def __enter__(self):
        """Start the stopwatch when entering the context."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Stop the stopwatch when exiting the context."""
        self.stop()

    # Public API --------------------------------------------------------------
    def reset(self):
        """Reset the stopwatch to zero and stop it."""
        self._start_time = None
        self._elapsed = 0.0
        self._running = False

    def start(self):
        """Start or resume the stopwatch."""
        if not self._running:
            self._start_time = time.perf_counter()
            self._running = True

    def stop(self):
        """Stop the stopwatch and return the elapsed time in seconds."""
        if self._running:
            now = time.perf_counter()
            self._elapsed += now - self._start_time
            self._start_time = None
            self._running = False
        return self._elapsed

    # Helper ------------------------------------------------------------------
    def _format_elapsed_time(self, elapsed_time: float) -> str:
        """
        Format a time duration in seconds into a string of the form
        HH:MM:SS.mmm (hours, minutes, seconds with 3 decimal places).
        """
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}"
