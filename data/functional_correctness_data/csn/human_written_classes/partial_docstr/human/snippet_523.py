from sys import stdout
from scvelo import settings
from time import time as get_time

class ProgressReporter:
    """TODO."""

    def __init__(self, total, interval=3):
        self.count = 0
        self.total = total
        self.timestamp = get_time()
        self.interval = interval

    def update(self):
        """TODO."""
        self.count += 1
        if settings.verbosity > 1 and (get_time() - self.timestamp > self.interval or self.count == self.total):
            self.timestamp = get_time()
            percent = int(self.count * 100 / self.total)
            stdout.write(f'\r... {percent}%')
            stdout.flush()

    def finish(self):
        """TODO."""
        if settings.verbosity > 1:
            stdout.write('\r')
            stdout.flush()