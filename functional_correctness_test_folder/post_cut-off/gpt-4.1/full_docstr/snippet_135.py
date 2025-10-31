
from typing import Optional, List, Dict, Generator
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
        self.gpu_indices = gpu_indices
        self._pynvml_initialized = False

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        '''
        Context manager to ensure pynvml is initialized and shut down properly.
        Yields
        ------
        None
        '''
        import pynvml
        pynvml.nvmlInit()
        self._pynvml_initialized = True
        try:
            yield
        finally:
            pynvml.nvmlShutdown()
            self._pynvml_initialized = False

    def get_memory_usage(self) -> Dict[int, int]:
        '''
        Get the current memory usage for each managed GPU.
        Returns
        -------
        Dict[int, int]
            Dictionary of memory usage in bytes for each GPU.
        '''
        import pynvml
        if not self._pynvml_initialized:
            raise RuntimeError(
                "pynvml is not initialized. Use manage_resources context manager.")
        memory_usage = {}
        if self.gpu_indices is None:
            # Assume single GPU (index 0)
            indices = [0]
        else:
            indices = self.gpu_indices
        for idx in indices:
            handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            memory_usage[idx] = mem_info.used
        return memory_usage
