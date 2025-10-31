
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
        self._start_time = 0.0

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
        self._start_time = 0.0

    def start(self):
        '''
        Starts the stopwatch by setting the start time and setting the 'is_running' flag to True.
        '''
        if not self.is_running:
            self._start_time = time.time()
            self.is_running = True

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        '''
        Formats the elapsed time in seconds to a string representation.
        Args:
            elapsed_time (float): The elapsed time in seconds.
        Returns:
            str: The formatted elapsed time string.
        '''
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = (seconds - int(seconds)) * 1000
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds):03d}"

    def stop(self):
        '''
        Stops the stopwatch by calculating the elapsed time and setting the 'is_running' flag to False.
        '''
        if self.is_running:
            self.elapsed += time.time() - self._start_time
            self.is_running = False
