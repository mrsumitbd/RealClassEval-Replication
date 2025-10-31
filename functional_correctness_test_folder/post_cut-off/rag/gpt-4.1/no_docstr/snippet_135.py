from typing import Optional, List, Dict, Generator
from contextlib import contextmanager

try:
    import pynvml
except ImportError:
    pynvml = None


class GPUManager:
    '''
    A manager class to handle GPU interactions using pynvml.
    Parameters
    ----------
    gpu_indices : Optional[List[int]]
        List of GPU indices to manage. If None, single GPU is assumed.
    '''

    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        '''Initialize the GPUManager.'''
        if pynvml is None:
            raise ImportError("pynvml is required for GPUManager")
        self.gpu_indices = gpu_indices
        self._initialized = False

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        '''
        Context manager to ensure pynvml is initialized and shut down properly.
        Yields
        ------
        None
        '''
        pynvml.nvmlInit()
        self._initialized = True
        try:
            yield
        finally:
            pynvml.nvmlShutdown()
            self._initialized = False

    def get_memory_usage(self) -> Dict[int, int]:
        '''
        Get the current memory usage for each managed GPU.
        Returns
        -------
        Dict[int, int]
            Dictionary of memory usage in bytes for each GPU.
        '''
        if not self._initialized:
            raise RuntimeError(
                "pynvml must be initialized (use manage_resources context manager)")
        memory_usage = {}
        if self.gpu_indices is None:
            count = pynvml.nvmlDeviceGetCount()
            indices = [0] if count > 0 else []
        else:
            indices = self.gpu_indices
        for idx in indices:
            handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
            meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
            memory_usage[idx] = meminfo.used
        return memory_usage
