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
        return False

    def reset(self):
        self._start_time = None
        self._elapsed = 0.0
        self._running = False
        return self

    def start(self):
        if not self._running:
            self._start_time = time.perf_counter()
            self._running = True
        return self

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        if elapsed_time < 0:
            elapsed_time = 0.0
        total_seconds = int(elapsed_time)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        milliseconds = int(round((elapsed_time - total_seconds) * 1000))
        if milliseconds == 1000:
            milliseconds = 0
            seconds += 1
            if seconds == 60:
                seconds = 0
                minutes += 1
                if minutes == 60:
                    minutes = 0
                    hours += 1
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    def stop(self):
        if self._running:
            end_time = time.perf_counter()
            self._elapsed += end_time - self._start_time
            self._start_time = None
            self._running = False
        return self._elapsed
