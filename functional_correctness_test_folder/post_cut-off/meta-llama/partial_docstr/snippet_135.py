
from typing import Optional, List, Dict, Generator
from contextlib import contextmanager
import torch


class GPUManager:

    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        '''Initialize the GPUManager.'''
        if gpu_indices is None:
            self.gpu_indices = list(range(torch.cuda.device_count()))
        else:
            self.gpu_indices = gpu_indices
        self.original_device = None

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        try:
            self.original_device = torch.cuda.current_device()
            torch.cuda.set_device(self.gpu_indices[0])
            yield
        finally:
            if self.original_device is not None:
                torch.cuda.set_device(self.original_device)

    def get_memory_usage(self) -> Dict[int, int]:
        memory_usage = {}
        for gpu_index in self.gpu_indices:
            torch.cuda.device(gpu_index)
            memory_usage[gpu_index] = torch.cuda.memory_allocated(
            ) // (1024 * 1024)  # in MB
        return memory_usage
