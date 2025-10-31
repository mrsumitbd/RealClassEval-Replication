
import time


class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0.0

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0.0

    def start(self):
        if self.start_time is None:
            self.start_time = time.time()

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = (seconds - int(seconds)) * 1000
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds):03d}"

    def stop(self):
        if self.start_time is not None:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None
        return self._format_elapsed_time(self.elapsed_time)
