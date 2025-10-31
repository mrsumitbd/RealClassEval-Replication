import time

class Timer:
    """Context manager for timing code.

    >>> with Timer():
    ...     your_code()
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def __enter__(self, progress=None):
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        self.interval = self.end - self.start
        if self.verbose:
            print('elapsed time: {0} sec'.format(self.interval))