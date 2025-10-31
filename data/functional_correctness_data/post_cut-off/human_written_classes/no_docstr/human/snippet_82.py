import torch

class CudaTimer:

    def __init__(self, enabled=True):
        self.enabled = enabled
        if self.enabled:
            self._start = torch.cuda.Event(enable_timing=True)
            self._recording = False
            self._end = torch.cuda.Event(enable_timing=True)

    def start(self):
        if self.enabled:
            assert not self._recording, 'CudaTimer has already started.'
            self._start.record()
            self._recording = True

    def end(self):
        if self.enabled:
            assert self._recording, 'CudaTimer has not started.'
            self._end.record()
            self._recording = False

    def timing(self) -> float:
        if self.enabled:
            assert not self._recording, 'CudaTimer has not ended.'
            self._end.synchronize()
            return self._start.elapsed_time(self._end)
        return 0.0