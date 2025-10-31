
import time


class __Timer__:

    def tic(self):
        self.start_time = time.time()

    def tac(self, verbose=True, digits=2):
        elapsed_time = time.time() - self.start_time
        if verbose:
            print(f"Elapsed time: {elapsed_time:.{digits}f} seconds")
        return elapsed_time

    def toc(self, verbose=True, digits=2):
        return self.tac(verbose, digits)

    def loop_timer(self, n, function, args=None, verbose=True, digits=2, best_of=3):
        if args is None:
            args = ()
        best_time = float('inf')
        for _ in range(best_of):
            self.tic()
            for _ in range(n):
                function(*args)
            elapsed_time = self.tac(False)
            if elapsed_time < best_time:
                best_time = elapsed_time
        if verbose:
            print(
                f"Best of {best_of}: {best_time:.{digits}f} seconds for {n} iterations")
        return best_time
