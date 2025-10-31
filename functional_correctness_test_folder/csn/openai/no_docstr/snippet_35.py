
import time


class __Timer__:
    def __init__(self):
        self._start = None

    def tic(self):
        """Start the timer."""
        self._start = time.perf_counter()

    def tac(self, verbose=True, digits=2):
        """Return the elapsed time since the last tic."""
        if self._start is None:
            raise RuntimeError("Timer has not been started with tic()")
        elapsed = time.perf_counter() - self._start
        if verbose:
            print(f"Elapsed time: {elapsed:.{digits}f} s")
        return elapsed

    def toc(self, verbose=True, digits=2):
        """Alias for tac."""
        return self.tac(verbose=verbose, digits=digits)

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        """
        Run `function` `n` times, timing each run.

        Parameters
        ----------
        n : int
            Number of times to run the function.
        function : callable
            The function to time.
        args : tuple or None
            Positional arguments to pass to the function.
        verbose : bool
            If True, print timing information.
        digits : int
            Number of decimal places to display.
        best_of : int
            Number of best (shortest) runs to average.

        Returns
        -------
        float
            The average time of the best_of shortest runs.
        """
        if args is None:
            args = ()
        times = []

        for _ in range(n):
            self.tic()
            function(*args)
            times.append(self.toc(verbose=False))

        times.sort()
        best_times = times[:best_of]
        avg_best = sum(best_times) / len(best_times)

        if verbose:
            print(
                f"Best {best_of} of {n} runs: {[f'{t:.{digits}f}s' for t in best_times]}")
            print(f"Average best time: {avg_best:.{digits}f} s")

        return avg_best
