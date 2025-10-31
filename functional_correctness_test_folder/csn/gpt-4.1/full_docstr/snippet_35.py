
import time


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

    def __init__(self):
        self._tic_time = None
        self._last_time = None

    def tic(self):
        '''
        Save time for future use with `tac()` or `toc()`.
        Returns
        -------
        None
            This function doesn't return a value.
        '''
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
        if self._last_time is None:
            raise RuntimeError("tic() must be called before tac()")
        now = time.perf_counter()
        elapsed = now - self._last_time
        self._last_time = now
        if verbose:
            print(f"Elapsed time: {elapsed:.{digits}f} seconds")
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
        if self._tic_time is None:
            raise RuntimeError("tic() must be called before toc()")
        now = time.perf_counter()
        elapsed = now - self._tic_time
        self._last_time = now
        if verbose:
            print(f"Elapsed time since tic: {elapsed:.{digits}f} seconds")
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
            print(f"Total time for {n} runs: {total_time:.{digits}f} seconds")
            print(f"Average time per run: {average_time:.{digits}f} seconds")
            print(
                f"Average of best {best_of} runs: {average_of_best:.{digits}f} seconds")
        return average_time, average_of_best
