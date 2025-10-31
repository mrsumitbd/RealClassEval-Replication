
import time
from functools import wraps


class __Timer__:

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None

    def tic(self):
        """Start the timer."""
        self.start_time = time.time()

    def tac(self, verbose=True, digits=2):
        """Record the end time and calculate elapsed time."""
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        if verbose:
            print(f"Elapsed time: {self.elapsed_time:.{digits}f} seconds")

    def toc(self, verbose=True, digits=2):
        """Alias for tac."""
        self.tac(verbose, digits)

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        """Time a function n times and return the average execution time."""
        if args is None:
            args = ()

        times = []
        for _ in range(best_of):
            total_time = 0
            for _ in range(n):
                start = time.time()
                function(*args)
                end = time.time()
                total_time += end - start
            times.append(total_time / n)

        avg_time = min(times)
        if verbose:
            print(
                f"Average execution time over {n} runs (best of {best_of}): {avg_time:.{digits}f} seconds")
        return avg_time

# Example usage:


def example_function(x, y):
    time.sleep(0.1)  # Simulate some work
    return x + y


timer = __Timer__()
timer.tic()
time.sleep(1)
timer.toc()

timer.loop_timer(10, example_function, (1, 2))
