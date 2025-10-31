import time
from typing import Any, Callable, Dict, Iterable, Optional, Tuple, Union


class __Timer__:
    def __init__(self):
        self._t0: Optional[float] = None
        self._t_last: Optional[float] = None

    def tic(self):
        now = time.perf_counter()
        self._t0 = now
        self._t_last = now
        return now

    def tac(self, verbose: bool = True, digits: int = 2):
        now = time.perf_counter()
        if self._t_last is None:
            self.tic()
            self._t_last = time.perf_counter()
        elapsed = now - self._t_last
        self._t_last = now
        if verbose:
            print(f"{elapsed:.{digits}f} s")
        return elapsed

    def toc(self, verbose: bool = True, digits: int = 2):
        now = time.perf_counter()
        if self._t0 is None:
            self.tic()
            self._t0 = time.perf_counter()
        elapsed = now - self._t0
        if verbose:
            print(f"{elapsed:.{digits}f} s")
        return elapsed

    def loop_timer(
        self,
        n: int,
        function: Callable,
        args: Optional[Union[Tuple, list, Dict, Any]] = None,
        verbose: bool = True,
        digits: int = 2,
        best_of: int = 3,
    ):
        def call_func():
            if args is None:
                function()
            elif isinstance(args, dict):
                function(**args)
            elif isinstance(args, (tuple, list)):
                function(*args)
            else:
                function(args)

        best_total = float("inf")
        best_per_iter = float("inf")

        for _ in range(max(1, int(best_of))):
            start = time.perf_counter()
            for _i in range(int(n)):
                call_func()
            total = time.perf_counter() - start
            per_iter = total / n if n > 0 else float("inf")
            if total < best_total:
                best_total = total
                best_per_iter = per_iter

        if verbose:
            print(
                f"Best of {best_of}: total {best_total:.{digits}f} s; per iter {best_per_iter:.{digits}f} s"
            )

        return best_total, best_per_iter
