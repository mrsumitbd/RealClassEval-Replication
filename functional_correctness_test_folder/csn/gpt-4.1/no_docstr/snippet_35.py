
import time


class __Timer__:
    def __init__(self):
        self._start_time = None
        self._last_time = None

    def tic(self):
        self._start_time = time.perf_counter()
        self._last_time = self._start_time

    def tac(self, verbose=True, digits=2):
        if self._last_time is None:
            raise RuntimeError("Timer not started. Call tic() first.")
        now = time.perf_counter()
        elapsed = now - self._last_time
        self._last_time = now
        if verbose:
            print(f"Elapsed: {elapsed:.{digits}f} s")
        return elapsed

    def toc(self, verbose=True, digits=2):
        if self._start_time is None:
            raise RuntimeError("Timer not started. Call tic() first.")
        now = time.perf_counter()
        elapsed = now - self._start_time
        if verbose:
            print(f"Total elapsed: {elapsed:.{digits}f} s")
        return elapsed

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        if args is None:
            args = ()
        best_time = float('inf')
        for _ in range(best_of):
            self.tic()
            for _ in range(n):
                function(*args)
            elapsed = self.toc(verbose=False)
            if elapsed < best_time:
                best_time = elapsed
        avg_time = best_time / n
        if verbose:
            print(f"Best of {best_of}: {avg_time:.{digits}f} s per loop")
        return avg_time
