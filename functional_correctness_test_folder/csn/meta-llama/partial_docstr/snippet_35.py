
import time
from functools import wraps


class __Timer__:
    def __init__(self):
        self.start_time = None
        self.last_time = None

    def tic(self):
        self.start_time = time.time()
        self.last_time = self.start_time

    def tac(self, verbose=True, digits=2):
        current_time = time.time()
        elapsed = current_time - self.last_time
        self.last_time = current_time
        if verbose:
            print(f"Time elapsed: {elapsed:.{digits}f} seconds")
        return elapsed

    def toc(self, verbose=True, digits=2):
        current_time = time.time()
        elapsed = current_time - self.start_time
        if verbose:
            print(f"Time elapsed since tic: {elapsed:.{digits}f} seconds")
        return elapsed

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        if args is None:
            args = []
        times = []
        for _ in range(n):
            start_time = time.time()
            for _ in range(best_of):
                function(*args)
            end_time = time.time()
            times.append((end_time - start_time) / best_of)
        average_time = sum(times) / n
        average_of_best = min(times)
        if verbose:
            print(
                f"Average time over {n} runs: {average_time:.{digits}f} seconds")
            print(
                f"Best time over {n} runs: {average_of_best:.{digits}f} seconds")
        return average_time, average_of_best

# Example usage:


def example_function(x, y):
    time.sleep(0.1)  # Simulate some work
    return x + y


timer = __Timer__()
timer.tic()
time.sleep(1)
timer.tac()
time.sleep(1)
timer.tac()
timer.toc()

average_time, average_of_best = timer.loop_timer(5, example_function, [1, 2])
print(f"Average time: {average_time}, Average of best: {average_of_best}")
