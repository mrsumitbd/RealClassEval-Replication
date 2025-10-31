
import pynvml
from typing import List, Dict, Optional, Generator
from contextlib import contextmanager


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
        self.gpu_indices = gpu_indices if gpu_indices is not None else [0]

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        '''
        Context manager to ensure pynvml is initialized and shut down properly.
        Yields
        ------
        None
        '''
        pynvml.nvmlInit()
        try:
            yield
        finally:
            pynvml.nvmlShutdown()

    def get_memory_usage(self) -> Dict[int, int]:
        '''
        Get the current memory usage for each managed GPU.
        Returns
        -------
        Dict[int, int]
            Dictionary of memory usage in bytes for each GPU.
        '''
        memory_usage = {}
        for gpu_index in self.gpu_indices:
            handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_index)
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            memory_usage[gpu_index] = info.used
        return memory_usage
