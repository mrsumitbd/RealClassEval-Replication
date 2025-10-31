import torch
import time
from contextlib import contextmanager

class Timer:
    """Handles accurate GPU timing using GPU events or CPU timing."""

    def __init__(self):
        if torch.cuda.is_available():
            self.start_event = torch.cuda.Event(enable_timing=True)
            self.end_event = torch.cuda.Event(enable_timing=True)
            self.use_gpu_timing = True
        elif torch.backends.mps.is_available():
            self.use_gpu_timing = False
        else:
            self.use_gpu_timing = False

    @contextmanager
    def timing(self):
        if self.use_gpu_timing:
            self.start_event.record()
            yield
            self.end_event.record()
            self.end_event.synchronize()
        else:
            start_time = time.time()
            yield
            self.cpu_elapsed = time.time() - start_time

    def elapsed_time(self) -> float:
        if self.use_gpu_timing:
            return self.start_event.elapsed_time(self.end_event) / 1000
        else:
            return self.cpu_elapsed