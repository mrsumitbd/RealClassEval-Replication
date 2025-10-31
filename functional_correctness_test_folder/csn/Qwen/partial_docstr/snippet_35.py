
import time


class __Timer__:

    def tic(self):
        self.start_time = time.time()
        self.last_time = self.start_time

    def tac(self, verbose=True, digits=2):
        current_time = time.time()
        elapsed = current_time - self.last_time
        self.last_time = current_time
        if verbose:
            print(f"Elapsed time: {elapsed:.{digits}f} seconds")
        return elapsed

    def toc(self, verbose=True, digits=2):
        current_time = time.time()
        elapsed = current_time - self.start_time
        if verbose:
            print(f"Total time: {elapsed:.{digits}f} seconds")
        return elapsed

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        if args is None:
            args = []
        total_times = []
        for _ in range(n):
            start = time.time()
            function(*args)
            end = time.time()
            total_times.append(end - start)

        average_time = sum(total_times) / n
        best_times = sorted(total_times)[:best_of]
        average_of_best = sum(best_times) / best_of if best_of > 0 else 0

        if verbose:
            print(
                f"Average time over {n} runs: {average_time:.{digits}f} seconds")
            print(
                f"Average of best {best_of} times: {average_of_best:.{digits}f} seconds")

        return average_time, average_of_best
