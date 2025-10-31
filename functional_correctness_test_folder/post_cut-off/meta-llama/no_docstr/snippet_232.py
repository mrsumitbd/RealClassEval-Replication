
import time
from typing import Optional


class Stopwatch:

    def __init__(self):
        self._start_time: Optional[float] = None
        self._elapsed_time: float = 0.0
        self._is_running: bool = False

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
            self._start_time = time.time() - self._elapsed_time
            self._is_running = True

    def _format_elapsed_time(self, elapsed_time: float) -> str:
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = elapsed_time % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

    def stop(self):
        if self._is_running:
            self._elapsed_time = time.time() - self._start_time
            self._is_running = False
            print(self._format_elapsed_time(self._elapsed_time))


# Example usage:
if __name__ == "__main__":
    with Stopwatch() as sw:
        time.sleep(1)
        time.sleep(2)
