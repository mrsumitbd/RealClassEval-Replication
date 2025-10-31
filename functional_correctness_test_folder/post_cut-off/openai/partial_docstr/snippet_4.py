
from typing import Dict, Any
import torch
import gc


class MemoryManager:
    """
    Utility class for monitoring and optimizing GPU memory usage during
    PyTorch model training.
    """

    def __init__(self):
        """
        Initialise the MemoryManager.  Detects the default CUDA device
        (if available) and caches the initial memory statistics.
        """
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self._update_memory_stats()

    def _update_memory_stats(self) -> None:
        """
        Internal helper to refresh cached memory statistics.
        """
        if self.device.type == "cuda":
            torch.cuda.synchronize()
            self._mem_allocated = torch.cuda.memory_allocated(self.device)
            self._mem_reserved = torch.cuda.memory_reserved(self.device)
            self._max_allocated = torch.cuda.max_memory_allocated(self.device)
            self._max_reserved = torch.cuda.max_memory_reserved(self.device)
            self._free, self._total = torch.cuda.mem_get_info(self.device)
        else:
            self._mem_allocated = 0
            self._mem_reserved = 0
            self._max_allocated = 0
            self._max_reserved = 0
            self._free = 0
            self._total = 0

    def get_memory_info(self) -> Dict[str, Any]:
        """
        Return a dictionary containing current and peak memory usage
        statistics for the default CUDA device.
        """
        self._update_memory_stats()
        return {
            "device": str(self.device),
            "memory_allocated_bytes": self._mem_allocated,
            "memory_reserved_bytes": self._mem_reserved,
            "max_memory_allocated_bytes": self._max_allocated,
            "max_memory_reserved_bytes": self._max_reserved,
            "free_memory_bytes": self._free,
            "total_memory_bytes": self._total,
        }

    def cleanup_memory(self, force: bool = False) -> None:
        """
        Release unused GPU memory.  If `force` is True, also clears the
        CUDA cache and triggers a garbage collection.
        """
        if self.device.type == "cuda":
            torch.cuda.empty_cache()
            if force:
                torch.cuda.ipc_collect()
                gc.collect()
        else:
            # No-op on CPU
            pass

    def get_optimal_training_config(self) -> Dict[str, Any]:
        """
        Estimate an optimal batch size and gradient accumulation steps
        based on the available GPU memory.  This is a heuristic and
        may need adjustment for specific models.
        """
        if self.device.type != "cuda":
            # Default CPU config
            return {"batch_size": 8, "gradient_accumulation_steps": 1}

        free_mem = self._free
        # Rough heuristic: use 50% of free memory for batch
        target_mem = free_mem * 0.5

        # Assume each sample consumes ~4 MB of GPU memory (model + activations)
        sample_mem = 4 * 1024 * 1024
        max_batch = max(1, int(target_mem // sample_mem))

        # Clamp batch size to a reasonable range
        batch_size = min(max_batch, 64)
        grad_accum = max(1, int(max_batch / batch_size))

        return {
            "batch_size": batch_size,
            "gradient_accumulation_steps": grad_accum,
        }

    def optimize_model_for_training(self, model):
        """
        Apply PyTorch's built-in memory optimizations for training.
        """
        if self.device.type == "cuda":
            # Enable cuDNN benchmark for faster convolutions
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False

            # If torch.compile is available, use it for speed
            if hasattr(torch, "compile"):
                try:
                    model = torch.compile(model)
                except Exception:
                    # Fall back silently if compilation fails
                    pass

        return model

    def optimize_training_args(self, training_args):
        """
        Adjust training arguments (e.g., batch size, gradient accumulation)
        to better fit the available GPU memory.
        """
        optimal = self.get_optimal_training_config()

        # Handle dict-like training_args
        if isinstance(training_args, dict):
            training_args["batch_size"] = optimal["batch_size"]
            training_args["gradient_accumulation_steps"] = optimal["gradient_accumulation_steps"]
            return training_args

        # Handle objects with attributes
        for key in ("batch_size", "gradient_accumulation_steps"):
            if hasattr(training_args, key):
                setattr(training_args, key, optimal[key])

        return training_args
