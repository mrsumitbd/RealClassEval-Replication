import time
from typing import Optional


class Stopwatch:
    '''
    A class representing a stopwatch for measuring elapsed time.
    Attributes:
        elapsed (float): The elapsed time in seconds.
        is_running (bool): A flag indicating whether the stopwatch is running
    '''

    def __init__(self) -> None:
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
        '''
        Exits the context block and stops the stopwatch.
        '''
        self.stop()

    def reset(self):
        '''
        Resets the stopwatch by setting the elapsed time to zero and stopping it
        '''
        self.elapsed = 0.0
        self.is_running = False
        self._start_time = None

    def start(self):
        '''
        Starts the stopwatch by setting the start time and setting the 'is_running' flag to True.
        '''
        if not self.is_running:
            self._start_time = time.perf_counter()
            self.is_running = True

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        '''
        Formats the elapsed time in seconds to a string representation.
        Args:
            elapsed_time (float): The elapsed time in seconds.
        Returns:
            str: The formatted elapsed time string.
        '''
        if elapsed_time < 0:
            elapsed_time = 0.0
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = elapsed_time % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

    def stop(self):
        '''
        Stops the stopwatch by calculating the elapsed time and setting the 'is_running' flag to False.
        '''
        if self.is_running and self._start_time is not None:
            self.elapsed += time.perf_counter() - self._start_time
            self.is_running = False
            self._start_time = None
