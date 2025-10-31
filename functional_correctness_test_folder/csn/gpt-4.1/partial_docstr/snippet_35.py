
import time


class __Timer__:
    def __init__(self):
        self._start_time = None
        self._last_time = None

    def tic(self):
        self._start_time = time.perf_counter()
        self._last_time = self._start_time

    def tac(self, verbose=True, digits=2):
        now = time.perf_counter()
        if self._last_time is None:
            raise RuntimeError("Call tic() before tac().")
        elapsed = now - self._last_time
        self._last_time = now
        if verbose:
            print(f"Elapsed time: {elapsed:.{digits}f} s")
        return elapsed

    def toc(self, verbose=True, digits=2):
        now = time.perf_counter()
        if self._start_time is None:
            raise RuntimeError("Call tic() before toc().")
        elapsed = now - self._start_time
        if verbose:
            print(f"Total elapsed time: {elapsed:.{digits}f} s")
        return elapsed

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        if args is None:
            args = []
        times = []
        for _ in range(n):
            start = time.perf_counter()
            function(*args)
            end = time.perf_counter()
            times.append(end - start)
        total_time = sum(times)
        average_time = total_time / n if n > 0 else 0.0
        best_times = sorted(times)[:best_of]
        average_of_best = sum(best_times) / best_of if best_of > 0 else 0.0
        if verbose:
            print(f"Average time over {n} runs: {average_time:.{digits}f} s")
            print(
                f"Average of best {best_of} times: {average_of_best:.{digits}f} s")
        return average_time, average_of_best
