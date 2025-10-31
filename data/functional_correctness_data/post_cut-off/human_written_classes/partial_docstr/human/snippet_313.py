import time

class Timer:
    """Simple timer for measuring elapsed time."""

    def __init__(self):
        self.start_time = None
        self.elapsed = 0.0

    def start(self):
        self.start_time = time.time()

    def get_elapsed(self):
        if self.start_time is not None:
            self.elapsed = time.time() - self.start_time
        return self.elapsed

    def stop(self):
        if self.start_time is not None:
            self.elapsed = time.time() - self.start_time
            self.start_time = None