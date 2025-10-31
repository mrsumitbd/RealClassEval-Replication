from typing import Callable, Generator, Optional, Sequence, Union
import sys
import time

class TimeoutChecker:

    def __init__(self, timeout: Optional[str]='00:03:45:00', fit_last_save_time: bool=False):
        """Initializes the TimeoutChecker.

        Args:
            timeout (str or None): Timeout in format 'DD:HH:MM:SS'. If None, timeout is considered infinite.
            fit_last_save_time (bool): If True, considers average iteration time when checking timeout.
        """
        super().__init__()
        self.last_save_time = float('inf') if timeout is None else convert_to_seconds(timeout)
        self.start_time = time.time()
        self.last_saved = False
        self.iteration_times = []
        self.previous_iteration_time: Optional[float] = None
        self.fit_last_save_time = fit_last_save_time

    def check_save(self):
        sys.stdout.flush()
        sys.stderr.flush()
        if self.last_saved:
            return False
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if self.fit_last_save_time and self.iteration_times:
            average_iteration_time = sum(self.iteration_times) / len(self.iteration_times)
            if elapsed_time + average_iteration_time >= self.last_save_time:
                self.last_saved = True
                return True
        if elapsed_time >= self.last_save_time:
            self.last_saved = True
            return True
        return False

    def start_iterations(self):
        self.previous_iteration_time = time.time()

    def mark_iteration(self):
        sys.stdout.flush()
        sys.stderr.flush()
        current_time = time.time()
        if self.previous_iteration_time is not None:
            elapsed_time = current_time - self.previous_iteration_time
            self.previous_iteration_time = current_time
        self.iteration_times.append(elapsed_time)