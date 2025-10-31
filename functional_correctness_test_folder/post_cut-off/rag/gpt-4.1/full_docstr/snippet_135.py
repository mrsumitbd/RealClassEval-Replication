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
        self._pynvml = None

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        '''
        Context manager to ensure pynvml is initialized and shut down properly.
        Yields
        ------
        None
        '''
        import pynvml
        self._pynvml = pynvml
        pynvml.nvmlInit()
        try:
            yield
        finally:
            pynvml.nvmlShutdown()
            self._pynvml = None

    def get_memory_usage(self) -> Dict[int, int]:
        '''
        Get the current memory usage for each managed GPU.
        Returns
        -------
        Dict[int, int]
            Dictionary of memory usage in bytes for each GPU.
        '''
        if self._pynvml is None:
            import pynvml
            self._pynvml = pynvml
            self._pynvml.nvmlInit()
            shutdown = True
        else:
            shutdown = False

        pynvml = self._pynvml
        if self.gpu_indices is None:
            count = pynvml.nvmlDeviceGetCount()
            indices = list(range(count))
        else:
            indices = self.gpu_indices

        usage = {}
        for idx in indices:
            handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
            meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
            usage[idx] = meminfo.used

        if shutdown:
            pynvml.nvmlShutdown()
            self._pynvml = None

        return usage
