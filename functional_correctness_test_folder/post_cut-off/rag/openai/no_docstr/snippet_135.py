
from contextlib import contextmanager
from typing import Dict, Generator, List, Optional

import pynvml


class GPUManager:
    """
    A manager class to handle GPU interactions using pynvml.

    Parameters
    ----------
    gpu_indices : Optional[List[int]]
        List of GPU indices to manage. If None, a single GPU (index 0) is assumed.
    """

    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        """Initialize the GPUManager."""
        if gpu_indices is None:
            self.gpu_indices = [0]
        else:
            if not isinstance(gpu_indices, list):
                raise TypeError(
                    "gpu_indices must be a list of integers or None")
            if not gpu_indices:
                raise ValueError("gpu_indices list cannot be empty")
            self.gpu_indices = gpu_indices

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        """
        Context manager to ensure pynvml is initialized and shut down properly.

        Yields
        ------
        None
        """
        pynvml.nvmlInit()
        try:
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
        usage: Dict[int, int] = {}
        for idx in self.gpu_indices:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                usage[idx] = mem_info.used
            except pynvml.NVMLError as exc:
                raise RuntimeError(
                    f"Failed to get memory info for GPU {idx}: {exc}") from exc
        return usage
