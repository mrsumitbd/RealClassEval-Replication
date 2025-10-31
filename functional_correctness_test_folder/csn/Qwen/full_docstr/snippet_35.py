
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

    def tic(self):
        '''
        Save time for future use with `tac()` or `toc()`.
        Returns
        -------
        None
            This function doesn't return a value.
        '''
        self.start_time = time.time()
        self.last_time = self.start_time

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
        current_time = time.time()
        elapsed = current_time - self.last_time
        self.last_time = current_time
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
        current_time = time.time()
        elapsed = current_time - self.start_time
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
            start = time.time()
            function(*args)
            end = time.time()
            times.append(end - start)

        average_time = sum(times) / n
        best_times = sorted(times)[:best_of]
        average_of_best = sum(best_times) / best_of if best_times else 0

        if verbose:
            print(
                f"Average time over {n} runs: {average_time:.{digits}f} seconds")
            print(
                f"Average of best {best_of} times: {average_of_best:.{digits}f} seconds")

        return average_time, average_of_best
