
import time


class __Timer__:

    def __init__(self):
        self._start_time = None
        self._last_time = None

    def tic(self):
        self._start_time = time.time()
        self._last_time = self._start_time

    def tac(self, verbose=True, digits=2):
        current_time = time.time()
        elapsed = current_time - self._last_time
        self._last_time = current_time
        if verbose:
            print(f"Elapsed time: {elapsed:.{digits}f} seconds")
        return elapsed

    def toc(self, verbose=True, digits=2):
        current_time = time.time()
        elapsed = current_time - self._start_time
        if verbose:
            print(f"Total elapsed time: {elapsed:.{digits}f} seconds")
        return elapsed

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        if args is None:
            args = []
        times = []
        for _ in range(n):
            self.tic()
            function(*args)
            times.append(self.toc(verbose=False))
        average_time = sum(times) / n
        best_times = sorted(times)[:best_of]
        average_of_best = sum(best_times) / best_of
        if verbose:
            print(
                f"Average time for {n} runs: {average_time:.{digits}f} seconds")
            print(
                f"Average of best {best_of} times: {average_of_best:.{digits}f} seconds")
        return average_time, average_of_best
