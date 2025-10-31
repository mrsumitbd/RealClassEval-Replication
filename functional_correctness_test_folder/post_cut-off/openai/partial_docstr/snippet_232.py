
import time


class Stopwatch:
    '''
    A class representing a stopwatch for measuring elapsed time.
    Attributes:
        elapsed (float): The elapsed time in seconds.
        is_running (bool): A flag indicating whether the stopwatch is running
    '''

    def __init__(self):
        self.elapsed = 0.0
        self.is_running = False
        self._start_time = None

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
        # Do not suppress exceptions
        return False

    def reset(self):
        '''
        Resets the stopwatch to its initial state.
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
        Formats a time value in seconds to a string with three decimal places.
        '''
        return f"{elapsed_time:.3f}s"

    def stop(self):
        '''
        Stops the stopwatch by calculating the elapsed time and setting the 'is_running' flag to False.
        '''
        if self.is_running:
            now = time.perf_counter()
            self.elapsed += now - self._start_time
            self.is_running = False
            self._start_time = None

    def __str__(self):
        return self._format_elapsed_time(self.elapsed)

    def __repr__(self):
        status = "running" if self.is_running else "stopped"
        return f"<Stopwatch {status}, elapsed={self._format_elapsed_time(self.elapsed)}>"
