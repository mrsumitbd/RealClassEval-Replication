
import time


class __Timer__:

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def tic(self):
        self.start_time = time.time()

    def tac(self, verbose=True, digits=2):
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        if verbose:
            print(f"Elapsed time: {elapsed_time:.{digits}f} seconds")
        return elapsed_time

    def toc(self, verbose=True, digits=2):
        elapsed_time = self.tac(verbose=False)
        self.start_time = None
        self.end_time = None
        if verbose:
            print(f"Total elapsed time: {elapsed_time:.{digits}f} seconds")
        return elapsed_time

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        if args is None:
            args = ()
        best_time = float('inf')
        for _ in range(best_of):
            self.tic()
            for _ in range(n):
                function(*args)
            current_time = self.tac(verbose=False)
            if current_time < best_time:
                best_time = current_time
        if verbose:
            print(
                f"Best of {best_of} loops: {best_time:.{digits}f} seconds per loop")
        return best_time
