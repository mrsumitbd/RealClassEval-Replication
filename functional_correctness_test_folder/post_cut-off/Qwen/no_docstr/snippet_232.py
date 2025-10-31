
import time


class Stopwatch:

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def reset(self):
        self._start_time = None
        self._elapsed_time = 0.0

    def start(self):
        if self._start_time is not None:
            raise RuntimeError("Stopwatch is already running")
        self._start_time = time.perf_counter()

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}"

    def stop(self):
        if self._start_time is None:
            raise RuntimeError("Stopwatch is not running")
        self._elapsed_time += time.perf_counter() - self._start_time
        self._start_time = None

    def elapsed_time(self) -> str:
        if self._start_time is not None:
            elapsed = self._elapsed_time + \
                (time.perf_counter() - self._start_time)
        else:
            elapsed = self._elapsed_time
        return self._format_elapsed_time(elapsed)

    def __init__(self):
        self.reset()
