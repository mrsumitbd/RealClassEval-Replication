
from contextlib import contextmanager
from typing import Dict, Generator, List, Optional

try:
    import torch
except ImportError:  # pragma: no cover
    torch = None


class GPUManager:
    """
    Simple GPU resource manager that can be used as a context manager.
    It keeps track of the GPUs that should be used and can report memory
    usage for each of them.
    """

    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        """
        Initialize the GPUManager.

        Parameters
        ----------
        gpu_indices : Optional[List[int]]
            List of GPU indices to manage. If None, all available GPUs are used.
        """
        if torch is None:
            raise RuntimeError("PyTorch is required for GPUManager to work.")

        if gpu_indices is None:
            self.gpu_indices = list(range(torch.cuda.device_count()))
        else:
            # Validate indices
            max_index = torch.cuda.device_count() - 1
            for idx in gpu_indices:
                if idx < 0 or idx > max_index:
                    raise ValueError(
                        f"GPU index {idx} is out of range (0-{max_index}).")
            self.gpu_indices = gpu_indices

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        """
        Context manager that can be used to temporarily set the default
        CUDA device to the first GPU in the list. After the context exits,
        the original device is restored.

        Yields
        ------
        None
        """
        if not self.gpu_indices:
            # No GPUs to manage; just yield
            yield
            return

        # Save the current device
        current_device = torch.cuda.current_device()
        try:
            # Set the default device to the first GPU in the list
            torch.cuda.set_device(self.gpu_indices[0])
            yield
        finally:
            # Restore the original device
            torch.cuda.set_device(current_device)

    def get_memory_usage(self) -> Dict[int, int]:
        """
        Get the memory usage for each managed GPU.

        Returns
        -------
        Dict[int, int]
            Mapping from GPU index to memory usage in megabytes.
        """
        usage: Dict[int, int] = {}
        for idx in self.gpu_indices:
            # memory_allocated returns bytes
            mem_bytes = torch.cuda.memory_allocated(idx)
            usage[idx] = mem_bytes // (1024 * 1024)  # Convert to MB
        return usage
