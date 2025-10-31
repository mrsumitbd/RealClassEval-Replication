
import time
from typing import Callable, Iterable, List, Optional, Tuple, Union


class __Timer__:
    """Computes elapsed time, between tic, tac, and toc.

    Methods
    -------
    tic :
        Resets timer.
    toc :
        Returns and prints time elapsed since last tic().
    tac :
        Returns and prints time elapsed since last
             tic(), tac() or toc() whichever occured last.
    loop_timer :
        Returns and prints the total and average time elapsed for n runs
        of a given function.
    """

    def __init__(self):
        self._start_time: Optional[float] = None
        self._last_time: Optional[float] = None

    def tic(self):
        """
        Save time for future use with `tac()` or `toc()`.
        Returns
        -------
        None
            This function doesn't return a value.
        """
        self._start_time = time.perf_counter()
        self._last_time = self._start_time

    def tac(self, verbose: bool = True, digits: int = 2) -> float:
        """
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
        """
        if self._last_time is None:
            raise RuntimeError("Timer has not been started with tic()")
        now = time.perf_counter()
        elapsed = now - self._last_time
        self._last_time = now
        if verbose:
            print(f"tac: {elapsed:.{digits}f} s")
        return elapsed

    def toc(self, verbose: bool = True, digits: int = 2) -> float:
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
        if self._start_time is None:
            raise RuntimeError("Timer has not been started with tic()")
        now = time.perf_counter()
        elapsed = now - self._start_time
        if verbose:
            print(f"toc: {elapsed:.{digits}f} s")
        return elapsed

    def loop_timer(
        self,
        n: int,
        function: Callable,
        args: Optional[Iterable] = None,
        verbose: bool = True,
        digits: int = 2,
        best_of: int = 3,
    ) -> Tuple[float, float]:
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
        if n <= 0:
            raise ValueError("n must be a positive integer")
        if best_of <= 0:
            raise ValueError("best_of must be a positive integer")
        if best_of > n:
            best_of = n

        times: List[float] = []

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
            print(
                f"loop_timer: total={total_time:.{digits}f}s, "
                f"average={average_time:.{digits}f}s, "
                f"average_of_best={average_of_best:.{digits}f}s"
            )

        return average_time, average_of_best
