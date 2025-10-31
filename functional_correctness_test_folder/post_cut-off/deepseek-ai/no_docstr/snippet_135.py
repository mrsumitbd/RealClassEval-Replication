
import contextlib
from typing import List, Optional, Dict, Generator
import torch


class GPUManager:

    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        self.gpu_indices = gpu_indices if gpu_indices is not None else list(
            range(torch.cuda.device_count()))

    @contextlib.contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        try:
            for idx in self.gpu_indices:
                torch.cuda.set_device(idx)
                torch.cuda.empty_cache()
            yield
        finally:
            for idx in self.gpu_indices:
                torch.cuda.set_device(idx)
                torch.cuda.empty_cache()

    def get_memory_usage(self) -> Dict[int, int]:
        memory_usage = {}
        for idx in self.gpu_indices:
            torch.cuda.set_device(idx)
            memory_usage[idx] = torch.cuda.memory_allocated(idx)
        return memory_usage
