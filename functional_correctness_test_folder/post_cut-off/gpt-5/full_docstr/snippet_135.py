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
            if not gpu_indices:
                raise ValueError(
                    "gpu_indices must be a non-empty list or None.")
            self.gpu_indices = list(gpu_indices)

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        '''
        Context manager to ensure pynvml is initialized and shut down properly.
        Yields
        ------
        None
        '''
        try:
            import pynvml
        except Exception as e:
            raise ImportError("pynvml is required to use GPUManager.") from e

        initialized_here = False
        try:
            # Initialize NVML
            pynvml.nvmlInit()
            initialized_here = True

            # Validate GPU indices
            count = pynvml.nvmlDeviceGetCount()
            for idx in self.gpu_indices:
                if not (0 <= int(idx) < count):
                    raise ValueError(
                        f"GPU index {idx} is out of range. Available GPUs: 0..{count-1}")

            yield
        finally:
            if initialized_here:
                try:
                    pynvml.nvmlShutdown()
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
        try:
            import pynvml
        except Exception as e:
            raise ImportError("pynvml is required to use GPUManager.") from e

        usage: Dict[int, int] = {}
        with self.manage_resources():
            for idx in self.gpu_indices:
                handle = pynvml.nvmlDeviceGetHandleByIndex(int(idx))
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                usage[int(idx)] = int(mem_info.used)
        return usage
