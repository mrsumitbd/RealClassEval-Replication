
from __future__ import annotations

from contextlib import contextmanager
from typing import Dict, Generator, List, Optional

try:
    import torch
except ImportError as exc:
    raise ImportError("torch is required for GPUManager") from exc


class GPUManager:
    """
    Simple GPU resource manager that tracks memory usage and provides a context
    manager for GPU resource cleanup.
    """

    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        """
        Parameters
        ----------
        gpu_indices : Optional[List[int]]
            List of GPU device indices to manage. If None, all available GPUs
            are managed.
        """
        if gpu_indices is None:
            self.gpu_indices = list(range(torch.cuda.device_count()))
        else:
            # Validate indices
            max_index = torch.cuda.device_count() - 1
            for idx in gpu_indices:
                if idx < 0 or idx > max_index:
                    raise ValueError(
                        f"GPU index {idx} is out of range (0-{max_index})")
            self.gpu_indices = gpu_indices

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        """
        Context manager that clears CUDA cache after the block.
        """
        try:
            yield
        finally:
            # Empty cache for all managed GPUs
            for idx in self.gpu_indices:
                torch.cuda.empty_cache()

    def get_memory_usage(self) -> Dict[int, int]:
        """
        Returns the current memory allocated on each managed GPU.

        Returns
        -------
        Dict[int, int]
            Mapping from GPU index to memory allocated in bytes.
        """
        usage: Dict[int, int] = {}
        for idx in self.gpu_indices:
            usage[idx] = torch.cuda.memory_allocated(idx)
        return usage
