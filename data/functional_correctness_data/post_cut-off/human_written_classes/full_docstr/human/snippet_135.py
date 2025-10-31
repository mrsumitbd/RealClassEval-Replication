from typing import Any, Dict, Generator, List, Optional, Type, cast
from contextlib import contextmanager
import pynvml

class GPUManager:
    """
    A manager class to handle GPU interactions using pynvml.

    Parameters
    ----------
    gpu_indices : Optional[List[int]]
        List of GPU indices to manage. If None, single GPU is assumed.
    """

    def __init__(self, gpu_indices: Optional[List[int]]=None) -> None:
        """Initialize the GPUManager."""
        self.device_count = 0
        self.gpu_indices = gpu_indices
        self.handles: List[Any] = []

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        """
        Context manager to ensure pynvml is initialized and shut down properly.

        Yields
        ------
        None
        """
        try:
            pynvml.nvmlInit()
            self.device_count = pynvml.nvmlDeviceGetCount()
            self.gpu_indices = self.gpu_indices or list(range(self.device_count))
            for idx in self.gpu_indices:
                if idx >= self.device_count:
                    raise ValueError(f'GPU index {idx} is out of range. Only {self.device_count} GPUs available.')
                handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
                self.handles.append(handle)
            yield
        finally:
            pynvml.nvmlShutdown()

    def get_memory_usage(self) -> Dict[int, int]:
        """
        Get the current memory usage for each managed GPU.

        Returns
        -------
        Dict[int, int]
            Dictionary of memory usage in bytes for each GPU.
        """
        if self.gpu_indices is None or self.handles is None:
            raise ValueError('GPU indices and handles must be initialized')
        memory_usages = {}
        for idx, handle in zip(self.gpu_indices, self.handles):
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            memory_usages[idx] = mem_info.used
        return memory_usages