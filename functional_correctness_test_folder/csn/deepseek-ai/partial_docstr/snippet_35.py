
import time


class __Timer__:
    def __init__(self):
        self._tic_time = None
        self._last_time = None

    def tic(self):
        self._tic_time = time.time()
        self._last_time = self._tic_time

    def tac(self, verbose=True, digits=2):
        current_time = time.time()
        if self._last_time is None:
            raise RuntimeError("No tic() called yet.")
        elapsed = current_time - self._last_time
        self._last_time = current_time
        if verbose:
            print(f"Elapsed time: {round(elapsed, digits)} seconds")
        return elapsed

    def toc(self, verbose=True, digits=2):
        if self._tic_time is None:
            raise RuntimeError("No tic() called yet.")
        elapsed = time.time() - self._tic_time
        if verbose:
            print(f"Total elapsed time: {round(elapsed, digits)} seconds")
        return elapsed

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        if args is None:
            args = []
        times = []
        for _ in range(best_of):
            self.tic()
            for _ in range(n):
                function(*args)
            elapsed = self.toc(verbose=False)
            times.append(elapsed)
        average_time = sum(times) / best_of
        best_times = sorted(times)[:best_of]
        average_of_best = sum(best_times) / len(best_times)
        if verbose:
            print(
                f"Average time per run: {round(average_of_best / n, digits)} seconds")
        return average_time / n, average_of_best / n
