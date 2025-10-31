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
        self.gpu_indices: List[int] = list(
            gpu_indices) if gpu_indices is not None else [0]
        self._pynvml = None

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        '''
        Context manager to ensure pynvml is initialized and shut down properly.
        Yields
        ------
        None
        '''
        try:
            import pynvml  # type: ignore
        except Exception:
            self._pynvml = None
            yield
            return
        try:
            pynvml.nvmlInit()
            self._pynvml = pynvml
            yield
        finally:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                pass
            self._pynvml = None

    def get_memory_usage(self) -> Dict[int, int]:
        '''
        Get the current memory usage for each managed GPU.
        Returns
        -------
        Dict[int, int]
            Dictionary of memory usage in bytes for each GPU.
        '''
        usage: Dict[int, int] = {}
        with self.manage_resources():
            if self._pynvml is None:
                return usage
            pynvml = self._pynvml
            try:
                device_count = pynvml.nvmlDeviceGetCount()
            except Exception:
                return usage
            valid_indices = [i for i in self.gpu_indices if isinstance(
                i, int) and 0 <= i < device_count]
            for idx in valid_indices:
                try:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
                    mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    usage[idx] = int(mem_info.used)
                except Exception:
                    # Skip indices that fail to query
                    continue
        return usage
