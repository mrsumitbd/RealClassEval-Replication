import time
from typing import Callable, Iterable, Optional, Tuple


class __Timer__:
    def __init__(self):
        self._tic_time: Optional[float] = None
        self._last_time: Optional[float] = None

    def tic(self):
        now = time.perf_counter()
        self._tic_time = now
        self._last_time = now

    def tac(self, verbose=True, digits=2):
        '''
        Return and print elapsed time since last `tic()`, `tac()`, or
        `toc()`.
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
        '''
        now = time.perf_counter()
        if self._last_time is None:
            # Initialize if not started
            self._tic_time = now
            self._last_time = now
            elapsed = 0.0
        else:
            elapsed = now - self._last_time
            self._last_time = now
        if verbose:
            print(f"{elapsed:.{digits}f}s")
        return elapsed

    def toc(self, verbose=True, digits=2):
        '''
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
        '''
        now = time.perf_counter()
        if self._tic_time is None:
            # Initialize if not started
            self._tic_time = now
            self._last_time = now
            elapsed = 0.0
        else:
            elapsed = now - self._tic_time
            # Update last_time to align with tac() doc stating it measures since last tic/tac/toc
            self._last_time = now
        if verbose:
            print(f"{elapsed:.{digits}f}s")
        return elapsed

    def loop_timer(self, n, function: Callable, args: Optional[Iterable] = None, verbose=True, digits=2, best_of=3):
        '''
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
        '''
        if n <= 0:
            if verbose:
                print(f"0.00s total, 0.00s avg, 0.00s best-of")
            return 0.0, 0.0

        if args is None:
            call_args: Tuple = ()
        elif isinstance(args, (list, tuple)):
            call_args = tuple(args)
        else:
            call_args = (args,)

        times = []
        for _ in range(n):
            t0 = time.perf_counter()
            function(*call_args)
            t1 = time.perf_counter()
            times.append(t1 - t0)

        total_time = sum(times)
        average_time = total_time / n

        k = min(best_of, n) if best_of is not None else 1
        best_k_avg = sum(sorted(times)[:k]) / k

        if verbose:
            print(
                f"{total_time:.{digits}f}s total, {average_time:.{digits}f}s avg, {best_k_avg:.{digits}f}s best-of-{k}")

        return average_time, best_k_avg
