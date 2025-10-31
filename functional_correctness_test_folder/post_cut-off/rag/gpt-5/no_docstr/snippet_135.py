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
        self.gpu_indices: Optional[List[int]] = list(
            gpu_indices) if gpu_indices is not None else None
        self._nvml = None

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        '''
        Context manager to ensure pynvml is initialized and shut down properly.
        Yields
        ------
        None
        '''
        initialized = False
        try:
            if self._nvml is None:
                try:
                    import pynvml as _pynvml
                    self._nvml = _pynvml
                except Exception:
                    self._nvml = None
            if self._nvml is not None:
                try:
                    self._nvml.nvmlInit()
                    initialized = True
                except Exception:
                    initialized = False
            yield
        finally:
            if self._nvml is not None and initialized:
                try:
                    self._nvml.nvmlShutdown()
                except Exception:
                    pass

    def get_memory_usage(self) -> Dict[int, int]:
        '''
        Get the current memory usage for each managed GPU.
        Returns
        -------
        Dict[int, int]
            Dictionary of memory usage in bytes for each GPU.
        '''
        with self.manage_resources():
            if self._nvml is None:
                return {}

            try:
                count = int(self._nvml.nvmlDeviceGetCount())
            except Exception:
                return {}

            if self.gpu_indices is None:
                indices: List[int] = [0] if count > 0 else []
            else:
                indices = self.gpu_indices

            # Keep order, unique, and within valid range
            seen = set()
            valid_indices: List[int] = []
            for idx in indices:
                if isinstance(idx, int) and 0 <= idx < count and idx not in seen:
                    valid_indices.append(idx)
                    seen.add(idx)

            usage: Dict[int, int] = {}
            for i in valid_indices:
                try:
                    handle = self._nvml.nvmlDeviceGetHandleByIndex(i)
                    meminfo = self._nvml.nvmlDeviceGetMemoryInfo(handle)
                    used = getattr(meminfo, 'used', 0)
                    usage[i] = int(used)
                except Exception:
                    usage[i] = 0
            return usage
