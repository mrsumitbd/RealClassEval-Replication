
import torch
from typing import Optional, List, Dict, Generator
from contextlib import contextmanager


class GPUManager:

    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        if gpu_indices is None:
            self.gpu_indices = list(range(torch.cuda.device_count()))
        else:
            self.gpu_indices = gpu_indices
        self.original_gpu_indices = None

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        try:
            self.original_gpu_indices = [torch.cuda.current_device()]
            for gpu_index in self.gpu_indices:
                torch.cuda.set_device(gpu_index)
                torch.cuda.empty_cache()
            yield
        finally:
            if self.original_gpu_indices is not None:
                for original_gpu_index in self.original_gpu_indices:
                    torch.cuda.set_device(original_gpu_index)

    def get_memory_usage(self) -> Dict[int, int]:
        memory_usage = {}
        for gpu_index in self.gpu_indices:
            torch.cuda.set_device(gpu_index)
            memory_usage[gpu_index] = torch.cuda.memory_allocated()
        if self.original_gpu_indices is not None:
            torch.cuda.set_device(self.original_gpu_indices[0])
        return memory_usage
