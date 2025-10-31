
import time


class Stopwatch:
    def __init__(self):
        self._start_time = None
        self._elapsed = 0.0
        self._running = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def reset(self):
        self._start_time = None
        self._elapsed = 0.0
        self._running = False

    def start(self):
        if not self._running:
            self._start_time = time.perf_counter()
            self._running = True

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:02.0f}:{:02.0f}:{:06.3f}".format(hours, minutes, seconds)

    def stop(self):
        if self._running:
            end_time = time.perf_counter()
            self._elapsed += end_time - self._start_time
            self._running = False
            return self._format_elapsed_time(self._elapsed)
        else:
            return self._format_elapsed_time(self._elapsed)
