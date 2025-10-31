
import time


class Stopwatch:

    def __init__(self):
        self._start_time = None
        self._elapsed_time = 0.0
        self._is_running = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def reset(self):
        self._start_time = None
        self._elapsed_time = 0.0
        self._is_running = False

    def start(self):
        if not self._is_running:
            self._start_time = time.time()
            self._is_running = True

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}"

    def stop(self):
        if self._is_running:
            end_time = time.time()
            self._elapsed_time += end_time - self._start_time
            self._is_running = False
            return self._format_elapsed_time(self._elapsed_time)
        return self._format_elapsed_time(self._elapsed_time)
