
import time
from typing import Optional, Type


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
        self.start_time = 0.0

    def __enter__(self):
        '''
        Enters a context block and starts the stopwatch.
        Returns:
            Stopwatch: The stopwatch instance.
        '''
        self.start()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback):
        self.stop()

    def reset(self):
        self.elapsed = 0.0
        self.is_running = False

    def start(self):
        '''
        Starts the stopwatch by setting the start time and setting the 'is_running' flag to True.
        '''
        if not self.is_running:
            self.start_time = time.time() - self.elapsed
            self.is_running = True

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = elapsed_time % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

    def stop(self):
        '''
        Stops the stopwatch by calculating the elapsed time and setting the 'is_running' flag to False.
        '''
        if self.is_running:
            self.elapsed = time.time() - self.start_time
            self.is_running = False

    def __str__(self):
        return self._format_elapsed_time(self.elapsed)

    def __repr__(self):
        return f"Stopwatch(elapsed={self.elapsed}, is_running={self.is_running})"


# Example usage:
if __name__ == "__main__":
    stopwatch = Stopwatch()
    stopwatch.start()
    time.sleep(1.5)
    stopwatch.stop()
    print(stopwatch)

    with Stopwatch() as sw:
        time.sleep(2.0)
    print(sw)

    stopwatch.reset()
    print(stopwatch)
