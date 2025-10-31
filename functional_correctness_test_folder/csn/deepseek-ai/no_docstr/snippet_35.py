
import time


class __Timer__:
    def __init__(self):
        self._start_time = None
        self._end_time = None

    def tic(self):
        self._start_time = time.time()

    def tac(self, verbose=True, digits=2):
        if self._start_time is None:
            raise RuntimeError("Timer has not been started. Call tic() first.")
        self._end_time = time.time()
        elapsed = self._end_time - self._start_time
        if verbose:
            print(f"Elapsed time: {round(elapsed, digits)} seconds")
        return elapsed

    def toc(self, verbose=True, digits=2):
        return self.tac(verbose, digits)

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        if args is None:
            args = []
        best_time = float('inf')
        for _ in range(best_of):
            self.tic()
            for _ in range(n):
                function(*args)
            elapsed = self.tac(verbose=False)
            if elapsed < best_time:
                best_time = elapsed
        avg_time = best_time / n
        if verbose:
            print(
                f"Average time per loop (best of {best_of}): {round(avg_time, digits)} seconds")
        return avg_time
