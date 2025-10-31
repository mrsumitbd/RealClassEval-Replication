import time

class Timer:
    """
    A context object timer. Usage:
        >>> with Timer() as timer:
        ...     do_something()
        >>> print(timer.interval)
    """

    def __init__(self):
        self.time = time.time

    def __enter__(self):
        self.start = self.time()
        return self

    def __exit__(self, *exc):
        self.finish = self.time()
        self.interval = self.finish - self.start

    def __str__(self):
        return human_readable_time(self.interval)