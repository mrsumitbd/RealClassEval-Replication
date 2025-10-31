
from __future__ import annotations

import gc
import os
import psutil
from typing import Any, Dict

import torch
from torch import nn
from torch.cuda import amp


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
            gpu_info = {
                "total": self._gpu_props.total_memory,
                "reserved": torch.cuda.memory_reserved(self._device),
                "allocated": torch.cuda.memory_allocated(self._device),
                "cached": torch.cuda.memory_cached(self._device),
                "max_reserved": torch.cuda.max_memory_reserved(self._device),
                "max_allocated": torch.cuda.max_memory_allocated(self._device),
            }
            info["gpu"] = gpu_info
        else:
            info["gpu"] = None

        return info

    def cleanup_memory(self, force: bool = False) -> None:
        """Free up memory by garbage collection and emptying CUDA cache."""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            if force:
                torch.cuda.ipc_collect()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        """
        Get recommended configurations for model training based on hardware capabilities.
        Returns a dictionary with keys:
            - mixed_precision (bool)
            - batch_size (int)
            - gradient_accumulation_steps (int)
        """
        config: Dict[str, Any] = {"mixed_precision": False,
                                  "batch_size": 8, "gradient_accumulation_steps": 1}

        if torch.cuda.is_available():
            total_mem = self._gpu_props.total_memory  # in bytes
            total_gb = total_mem / (1024**3)

            # Simple heuristic: larger GPUs can handle larger batch sizes
            if total_gb >= 16:
                config["batch_size"] = 32
                config["gradient_accumulation_steps"] = 1
                config["mixed_precision"] = True
            elif total_gb >= 8:
                config["batch_size"] = 16
                config["gradient_accumulation_steps"] = 1
                config["mixed_precision"] = True
            elif total_gb >= 4:
                config["batch_size"] = 8
                config["gradient_accumulation_steps"] = 2
                config["mixed_precision"] = True
            else:
                config["batch_size"] = 4
                config["gradient_accumulation_steps"] = 4
                config["mixed_precision"] = False

        return config

    def optimize_model_for_training(self, model: nn.Module) -> None:
        """
        Apply PyTorch's built-in memory optimizations for training.
        This includes enabling cuDNN benchmark, allowing TF32, and
        setting the model to train mode.
        """
        if not isinstance(model, nn.Module):
            raise TypeError("model must be an instance of torch.nn.Module")

        # Enable cuDNN benchmark for faster convolutions on fixed input sizes
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.deterministic = False

        # Allow TF32 on matmul and cudnn for faster training on Ampere+ GPUs
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

        # Put model in training mode
        model.train()

    def optimize_training_args(self, training_args: Dict[str, Any]) -> None:
        """
        Configure training arguments for efficient memory usage.
        Modifies the dictionary in place.
        Expected keys may include:
            - batch_size
            - gradient_accumulation_steps
            - fp16 / mixed_precision
        """
        if not isinstance(training_args, dict):
            raise TypeError("training_args must be a dictionary")

        config = self.get_optimal_training_config()

        # Update mixed precision flag
        training_args["fp16"] = config["mixed_precision"]
        training_args["bf16"] = False  # prefer fp16 if available

        # Update batch size and gradient accumulation
        training_args["batch_size"] = config["batch_size"]
        training_args["gradient_accumulation_steps"] = config["gradient_accumulation_steps"]

        # If using AMP, set up autocast context manager
        if config["mixed_precision"]:
            training_args["amp"] = amp.autocast
        else:
            training_args["amp"] = None
