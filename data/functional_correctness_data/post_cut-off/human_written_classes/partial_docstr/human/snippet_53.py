import time

class ProfileKV:
    """
    Usage:
    with logger.ProfileKV("interesting_scope"):
        code
    """

    def __init__(self, n):
        self.n = 'wait_' + n

    def __enter__(self):
        self.t1 = time.time()

    def __exit__(self, type, value, traceback):
        Logger.CURRENT.name2val[self.n] += time.time() - self.t1