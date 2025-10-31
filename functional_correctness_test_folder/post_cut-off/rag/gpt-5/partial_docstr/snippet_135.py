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
        if gpu_indices is None:
            self.gpu_indices: List[int] = [0]
        else:
            if not isinstance(gpu_indices, (list, tuple)):
                raise TypeError(
                    'gpu_indices must be a list or tuple of integers')
            cleaned: List[int] = []
            for idx in gpu_indices:
                if not isinstance(idx, int):
                    raise TypeError('All gpu_indices must be integers')
                if idx not in cleaned:
                    cleaned.append(idx)
            self.gpu_indices = cleaned
        self._nvml = None

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        '''
        Context manager to ensure pynvml is initialized and shut down properly.
        Yields
        ------
        None
        '''
        try:
            import pynvml as _nvml  # type: ignore
        except Exception as e:
            raise ImportError('pynvml is required to use GPUManager') from e

        self._nvml = _nvml
        try:
            self._nvml.nvmlInit()
            count = self._nvml.nvmlDeviceGetCount()
            for idx in self.gpu_indices:
                if idx < 0 or idx >= count:
                    raise IndexError(
                        f'GPU index {idx} is out of range [0, {count - 1}]')
            yield None
        finally:
            try:
                self._nvml.nvmlShutdown()
            except Exception:
                pass
            self._nvml = None

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
            if not self.gpu_indices:
                return usage
            nvml = self._nvml
            for idx in self.gpu_indices:
                handle = nvml.nvmlDeviceGetHandleByIndex(idx)
                meminfo = nvml.nvmlDeviceGetMemoryInfo(handle)
                usage[idx] = int(meminfo.used)
        return usage
