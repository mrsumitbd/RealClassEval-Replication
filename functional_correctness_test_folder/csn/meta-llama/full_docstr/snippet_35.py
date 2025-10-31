
import time
from functools import wraps


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
        self.start_time = None
        self.last_time = None

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
            print(f"Time elapsed: {elapsed:.{digits}f} seconds")
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
            print(f"Time elapsed since tic: {elapsed:.{digits}f} seconds")
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
        elif not isinstance(args, list):
            args = [args]

        total_time = 0
        best_times = []

        for _ in range(n):
            start_time = time.time()
            function(*args)
            end_time = time.time()
            elapsed = end_time - start_time
            total_time += elapsed
            best_times.append(elapsed)

        average_time = total_time / n
        best_times = sorted(best_times)[:best_of]
        average_of_best = sum(best_times) / len(best_times)

        if verbose:
            print(f"Average time: {average_time:.{digits}f} seconds")
            print(
                f"Average of best {best_of} times: {average_of_best:.{digits}f} seconds")

        return average_time, average_of_best


# Example usage:
def example_function(x):
    time.sleep(0.1)  # Simulate some work
    return x * x


if __name__ == "__main__":
    timer = __Timer__()
    timer.tic()
    time.sleep(1)
    print(timer.tac())
    time.sleep(1)
    print(timer.toc())

    average_time, average_of_best = timer.loop_timer(
        10, example_function, args=5)
    print(f"Average time: {average_time}, Average of best: {average_of_best}")
