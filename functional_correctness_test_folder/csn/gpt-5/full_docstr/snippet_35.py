import time
from typing import Any, Callable, Iterable, Optional, Tuple


class __Timer__:
    '''Computes elapsed time, between tic, tac, and toc.
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
    '''

    def __init__(self) -> None:
        self._t0: Optional[float] = None
        self._t_last: Optional[float] = None

    def tic(self):
        '''
        Save time for future use with `tac()` or `toc()`.
        Returns
        -------
        None
            This function doesn't return a value.
        '''
        now = time.perf_counter()
        self._t0 = now
        self._t_last = now

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
        if self._t_last is None:
            # Auto-initialize if not started
            self.tic()
            elapsed = 0.0
            # Ensure t_last corresponds to 'now' consistently
            self._t_last = now
            self._t0 = now
        else:
            elapsed = now - self._t_last
            self._t_last = now
        if verbose:
            print(f"tac: {elapsed:.{int(digits)}f} s")
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
        if self._t0 is None:
            # Auto-initialize if not started
            self.tic()
            elapsed = 0.0
            # After toc, last checkpoint becomes now
            self._t_last = now
            self._t0 = now
        else:
            elapsed = now - self._t0
            self._t_last = now
        if verbose:
            print(f"toc: {elapsed:.{int(digits)}f} s")
        return elapsed

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
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
                print("Average time: 0.00 s | Best-of average: 0.00 s | Total: 0.00 s")
            return 0.0, 0.0

        if args is None:
            call_args: Tuple[Any, ...] = ()
        elif isinstance(args, tuple):
            call_args = args
        elif isinstance(args, list):
            call_args = tuple(args)
        else:
            call_args = (args,)

        times = []
        for _ in range(n):
            start = time.perf_counter()
            function(*call_args)
            end = time.perf_counter()
            times.append(end - start)

        total_time = sum(times)
        average_time = total_time / n
        k = max(1, min(int(best_of), n))
        best_times = sorted(times)[:k]
        average_of_best = sum(best_times) / k

        if verbose:
            d = int(digits)
            print(
                f"Total: {total_time:.{d}f} s | "
                f"Average: {average_time:.{d}f} s | "
                f"Best-{k} average: {average_of_best:.{d}f} s"
            )

        return average_time, average_of_best
