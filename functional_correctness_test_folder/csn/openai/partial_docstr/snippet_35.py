
import time


class __Timer__:
    def __init__(self):
        self._last_time = None

    def tic(self):
        """Start or restart the timer."""
        self._last_time = time.perf_counter()

    def tac(self, verbose=True, digits=2):
        """
        Return and print elapsed time since last `tic()`, `tac()`, or `toc()`.
        Parameters
        ----------
        verbose : bool, optional(default=True)
            If True, then prints time.
        digits : scalar(int), optional(default=2)
            Number of digits printed for time elapsed.
        Returns
        -------
        elapsed : scalar(float)
            Time elapsed since last `tic()`, `tac()`, or `toc()`.
        """
        if self._last_time is None:
            raise RuntimeError("Timer has not been started. Call tic() first.")
        now = time.perf_counter()
        elapsed = now - self._last_time
        self._last_time = now
        if verbose:
            print(f"Elapsed time: {elapsed:.{digits}f} s")
        return elapsed

    def toc(self, verbose=True, digits=2):
        """
        Return and print time elapsed since last `tic()`.
        Parameters
        ----------
        verbose : bool, optional(default=True)
            If True, then prints time.
        digits : scalar(int), optional(default=2)
            Number of digits printed for time elapsed.
        Returns
        -------
        elapsed : scalar(float)
            Time elapsed since last `tic()`.
        """
        if self._last_time is None:
            raise RuntimeError("Timer has not been started. Call tic() first.")
        now = time.perf_counter()
        elapsed = now - self._last_time
        if verbose:
            print(f"Elapsed time: {elapsed:.{digits}f} s")
        return elapsed

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        """
        Return and print the total and average time elapsed for n runs
        of function.
        Parameters
        ----------
        n : scalar(int)
            Number of runs.
        function : function
            Function to be timed.
        args : list, optional(default=None)
            Arguments of the function.
        verbose : bool, optional(default=True)
            If True, then prints average time.
        digits : scalar(int), optional(default=2)
            Number of digits printed for time elapsed.
        best_of : scalar(int), optional(default=3)
            Average time over best_of runs.
        Returns
        -------
        average_time : scalar(float)
            Average time elapsed for n runs of function.
        average_of_best : scalar(float)
            Average of best_of times for n runs of function.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n must be a positive integer")
        if best_of <= 0 or best_of > n:
            raise ValueError("best_of must be between 1 and n")

        times = []
        for _ in range(n):
            start = time.perf_counter()
            if args is None:
                function()
            else:
                function(*args)
            end = time.perf_counter()
            times.append(end - start)

        total_time = sum(times)
        average_time = total_time / n
        best_times = sorted(times)[:best_of]
        average_of_best = sum(best_times) / best_of

        if verbose:
            print(f"Total time for {n} runs: {total_time:.{digits}f} s")
            print(f"Average time per run: {average_time:.{digits}f} s")
            print(
                f"Average of best {best_of} runs: {average_of_best:.{digits}f} s")

        return average_time, average_of_best
