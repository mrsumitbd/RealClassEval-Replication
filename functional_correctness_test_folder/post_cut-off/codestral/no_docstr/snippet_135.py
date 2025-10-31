
import pynvml
from contextlib import contextmanager
from typing import List, Optional, Dict, Generator


class GPUManager:

    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        pynvml.nvmlInit()
        self.gpu_indices = gpu_indices if gpu_indices is not None else list(
            range(pynvml.nvmlDeviceGetCount()))

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        try:
            yield
        finally:
            pynvml.nvmlShutdown()

    def get_memory_usage(self) -> Dict[int, int]:
        memory_usage = {}
        for index in self.gpu_indices:
            handle = pynvml.nvmlDeviceGetHandleByIndex(index)
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            memory_usage[index] = info.used
        return memory_usage
