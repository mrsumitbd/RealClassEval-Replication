
from __future__ import annotations

import gc
import psutil
from typing import Any, Dict

import torch


class MemoryManager:
    """Simple memory manager that leverages PyTorch's built-in memory optimizations."""

    def __init__(self) -> None:
        """Initialize the memory manager."""
        # Cache device properties for quick access
        self._device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        if torch.cuda.is_available():
            self._gpu_props = torch.cuda.get_device_properties(self._device)
        else:
            self._gpu_props = None

    def get_memory_info(self) -> Dict[str, Any]:
        """Get current memory usage information."""
        info: Dict[str, Any] = {}

        # CPU memory
        vm = psutil.virtual_memory()
        info["cpu_total"] = vm.total
        info["cpu_available"] = vm.available
        info["cpu_used"] = vm.used
        info["cpu_percent"] = vm.percent

        # GPU memory (if available)
        if torch.cuda.is_available():
            info["gpu_total"] = torch.cuda.get_device_properties(
                self._device).total_memory
            info["gpu_allocated"] = torch.cuda.memory_allocated(self._device)
            info["gpu_reserved"] = torch.cuda.memory_reserved(self._device)
            info["gpu_cached"] = torch.cuda.memory_cached(self._device)
            info["gpu_free"] = info["gpu_total"] - info["gpu_reserved"]
        else:
            info["gpu_total"] = 0
            info["gpu_allocated"] = 0
            info["gpu_reserved"] = 0
            info["gpu_cached"] = 0
            info["gpu_free"] = 0

        return info

    def cleanup_memory(self, force: bool = False) -> None:
        """Free up memory by garbage collection and emptying CUDA cache."""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            if force:
                # Force a full cache cleanup (may be slower)
                torch.cuda.ipc_collect()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        """Get recommended configurations for model training based on hardware capabilities."""
        config: Dict[str, Any] = {}

        # Default values
        batch_size = 8
        gradient_accumulation_steps = 1
        fp16 = False

        if torch.cuda.is_available():
            free_mem = self.get_memory_info()["gpu_free"]
            # Rough heuristic: use fp16 if GPU has > 8GB free
            if free_mem > 8 * 1024**3:
                fp16 = True
                batch_size = 32
                gradient_accumulation_steps = 1
            elif free_mem > 4 * 1024**3:
                fp16 = True
                batch_size = 16
                gradient_accumulation_steps = 1
            else:
                batch_size = 8
                gradient_accumulation_steps = 2

        config["batch_size"] = batch_size
        config["gradient_accumulation_steps"] = gradient_accumulation_steps
        config["fp16"] = fp16
        return config

    def optimize_model_for_training(self, model: torch.nn.Module) -> None:
        """Apply PyTorch's built-in memory optimizations for training."""
        # Enable cuDNN benchmark for faster convolutions
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.deterministic = False

        # Ensure gradients are enabled
        torch.set_grad_enabled(True)

        # Move model to the appropriate device
        if torch.cuda.is_available():
            model.to(self._device)

    def optimize_training_args(self, training_args: Dict[str, Any]) -> Dict[str, Any]:
        """Configure training arguments for efficient memory usage."""
        config = self.get_optimal_training_config()

        # Update batch size
        training_args["per_device_train_batch_size"] = config["batch_size"]

        # Update gradient accumulation
        training_args["gradient_accumulation_steps"] = config["gradient_accumulation_steps"]

        # Enable fp16 if available
        if config["fp16"]:
            training_args["fp16"] = True
            training_args["fp16_opt_level"] = "O1"

        # Ensure device placement
        if torch.cuda.is_available():
            training_args["device"] = "cuda"
        else:
            training_args["device"] = "cpu"

        return training_args
