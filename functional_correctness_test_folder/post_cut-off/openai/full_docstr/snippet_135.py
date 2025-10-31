
from contextlib import contextmanager
from typing import Dict, Generator, List, Optional

import pynvml


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
        if gpu_indices is None:
            # Default to the first GPU if no indices are provided
            self.gpu_indices = [0]
        else:
            self.gpu_indices = gpu_indices

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        '''
        Context manager to ensure pynvml is initialized and shut down properly.
        Yields
        ------
        None
        '''
        try:
            pynvml.nvmlInit()
            yield
        finally:
            try:
                pynvml.nvmlShutdown()
            except pynvml.NVMLError:
                # Ignore errors during shutdown
                pass

    def get_memory_usage(self) -> Dict[int, int]:
        '''
        Get the current memory usage for each managed GPU.
        Returns
        -------
        Dict[int, int]
            Dictionary of memory usage in bytes for each GPU.
        '''
        usage: Dict[int, int] = {}
        for idx in self.gpu_indices:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                usage[idx] = mem_info.used
            except pynvml.NVMLError as e:
                # If the GPU index is invalid or inaccessible, record 0 usage
                usage[idx] = 0
        return usage
