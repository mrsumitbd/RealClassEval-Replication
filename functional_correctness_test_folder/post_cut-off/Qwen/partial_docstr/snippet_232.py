
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

    def reset(self):
        self.elapsed = 0.0
        self.is_running = False
        self._start_time = None

    def start(self):
        '''
        Starts the stopwatch by setting the start time and setting the 'is_running' flag to True.
        '''
        if not self.is_running:
            self._start_time = time.time() - self.elapsed
            self.is_running = True

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time % 1) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

    def stop(self):
        '''
        Stops the stopwatch by calculating the elapsed time and setting the 'is_running' flag to False.
        '''
        if self.is_running:
            self.elapsed = time.time() - self._start_time
            self.is_running = False

    def get_elapsed_time(self) -> str:
        if self.is_running:
            current_elapsed = time.time() - self._start_time
        else:
            current_elapsed = self.elapsed
        return self._format_elapsed_time(current_elapsed)
