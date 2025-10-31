import time
from typing import Optional


class Stopwatch:
    '''
    A class representing a stopwatch for measuring elapsed time.
    Attributes:
        elapsed (float): The elapsed time in seconds.
        is_running (bool): A flag indicating whether the stopwatch is running
    '''

    def __init__(self):
        self.elapsed: float = 0.0
        self.is_running: bool = False
        self._start_time: Optional[float] = None

    def __enter__(self):
        '''
        Enters a context block and starts the stopwatch.
        Returns:
            Stopwatch: The stopwatch instance.
        '''
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        return False

    def reset(self):
        self.elapsed = 0.0
        if self.is_running:
            self._start_time = time.perf_counter()
        else:
            self._start_time = None

    def start(self):
        '''
        Starts the stopwatch by setting the start time and setting the 'is_running' flag to True.
        '''
        if not self.is_running:
            self._start_time = time.perf_counter()
            self.is_running = True

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        total_ms = int(round(elapsed_time * 1000))
        hours, rem_ms = divmod(total_ms, 3600_000)
        minutes, rem_ms = divmod(rem_ms, 60_000)
        seconds, milliseconds = divmod(rem_ms, 1000)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    def stop(self):
        '''
        Stops the stopwatch by calculating the elapsed time and setting the 'is_running' flag to False.
        '''
        if self.is_running and self._start_time is not None:
            self.elapsed += time.perf_counter() - self._start_time
            self.is_running = False
            self._start_time = None
        return self.elapsed
