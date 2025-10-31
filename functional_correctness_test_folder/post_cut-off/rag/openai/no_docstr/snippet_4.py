
from __future__ import annotations

import gc
import psutil
from typing import Any, Dict

import torch


class MemoryManager:
    """Simple memory manager that leverages PyTorch's built-in memory optimizations."""

    def __init__(self) -> None:
        """Initialize the memory manager."""
        self._device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self._gpu_props = (
            torch.cuda.get_device_properties(self._device)
            if torch.cuda.is_available()
            else None
        )

    def get_memory_info(self) -> Dict[str, Any]:
        """Get current memory usage information."""
        info: Dict[str, Any] = {}

        # CPU memory
        vm = psutil.virtual_memory()
        info["cpu_total"] = vm.total
        info["cpu_available"] = vm.available
        info["cpu_used"] = vm.used
        info["cpu_percent"] = vm.percent

        # GPU memory
        if torch.cuda.is_available():
            gpu = self._device
            props = self._gpu_props
            info["gpu_total"] = props.total_memory
            info["gpu_allocated"] = torch.cuda.memory_allocated(gpu)
            info["gpu_reserved"] = torch.cuda.memory_reserved(gpu)
            info["gpu_cached"] = torch.cuda.memory_cached(gpu)
            info["gpu_free"] = props.total_memory - \
                torch.cuda.memory_reserved(gpu)
            info["gpu_utilization"] = torch.cuda.utilization(
                gpu) if hasattr(torch.cuda, "utilization") else None
        else:
            info["gpu_total"] = 0
            info["gpu_allocated"] = 0
            info["gpu_reserved"] = 0
            info["gpu_cached"] = 0
            info["gpu_free"] = 0
            info["gpu_utilization"] = None

        return info

    def cleanup_memory(self, force: bool = False) -> None:
        """Free up memory by garbage collection and emptying CUDA cache."""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            if force:
                torch.cuda.ipc_collect()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        """Get recommended configurations for model training based on hardware capabilities."""
        config: Dict[str, Any] = {}

        # Basic defaults
        config["mixed_precision"] = False
        config["gradient_accumulation_steps"] = 1
        config["batch_size"] = 8

        if torch.cuda.is_available():
            total_mem_gb = self._gpu_props.total_memory / (1024**3)
            # Heuristic: larger GPUs can handle larger batch sizes
            if total_mem_gb >= 12:
                config["batch_size"] = 32
                config["mixed_precision"] = True
                config["gradient_accumulation_steps"] = 1
            elif total_mem_gb >= 8:
                config["batch_size"] = 16
                config["mixed_precision"] = True
                config["gradient_accumulation_steps"] = 1
            else:
                config["batch_size"] = 8
                config["mixed_precision"] = False
                config["gradient_accumulation_steps"] = 2

        return config

    def optimize_model_for_training(self, model: torch.nn.Module) -> None:
        """Apply PyTorch's built-in memory optimizations for training."""
        # Enable cuDNN benchmark for faster convolutions
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.deterministic = False

        # If using mixed precision, set up autocast context manager
        if torch.cuda.is_available():
            # The user should wrap forward passes with torch.cuda.amp.autocast
            # Here we just ensure the device is set correctly
            model.to(self._device)

    def optimize_training_args(self, training_args: Dict[str, Any]) -> None:
        """Configure training arguments for efficient memory usage."""
        # Ensure training_args is a dict
        if not isinstance(training_args, dict):
            raise TypeError("training_args must be a dict")

        # Apply defaults from get_optimal_training_config
        optimal = self.get_optimal_training_config()
        training_args.setdefault("mixed_precision", optimal["mixed_precision"])
        training_args.setdefault(
            "gradient_accumulation_steps", optimal["gradient_accumulation_steps"])
        training_args.setdefault("batch_size", optimal["batch_size"])

        # If mixed precision is enabled, set up AMP
        if training_args["mixed_precision"]:
            training_args.setdefault("fp16", True)
            training_args.setdefault("bf16", False)
        else:
            training_args.setdefault("fp16", False)
            training_args.setdefault("bf16", False)

        # Ensure cuDNN benchmark is enabled
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.deterministic = False
