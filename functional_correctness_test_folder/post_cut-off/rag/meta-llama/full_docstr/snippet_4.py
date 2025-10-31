
import torch
import gc
from typing import Dict, Any


class MemoryManager:
    """Simple memory manager that leverages PyTorch's built-in memory optimizations."""

    def __init__(self):
        """Initialize the memory manager."""
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

    def get_memory_info(self) -> Dict[str, Any]:
        """Get current memory usage information."""
        memory_info = {}
        if self.device.type == "cuda":
            memory_info["cuda_allocated"] = torch.cuda.memory_allocated()
            memory_info["cuda_reserved"] = torch.cuda.memory_reserved()
        memory_info["cpu_allocated"] = gc.get_count()
        return memory_info

    def cleanup_memory(self, force: bool = False) -> None:
        """Free up memory by garbage collection and emptying CUDA cache."""
        gc.collect()
        if self.device.type == "cuda" or force:
            torch.cuda.empty_cache()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        """Get recommended configurations for model training based on hardware capabilities."""
        config = {}
        if self.device.type == "cuda":
            config["batch_size"] = 32  # adjust based on GPU memory
            # adjust based on GPU memory
            config["gradient_accumulation_steps"] = 1
        else:
            config["batch_size"] = 16  # adjust based on CPU memory
            # adjust based on CPU memory
            config["gradient_accumulation_steps"] = 2
        return config

    def optimize_model_for_training(self, model):
        """Apply PyTorch's built-in memory optimizations for training."""
        if self.device.type == "cuda":
            model.to(self.device)
            if torch.cuda.device_count() > 1:
                model = torch.nn.DataParallel(model)

    def optimize_training_args(self, training_args):
        """Configure training arguments for efficient memory usage."""
        if self.device.type == "cuda":
            training_args["fp16"] = True  # enable mixed precision training
            # reduce memory usage during training
            training_args["gradient_checkpointing"] = True
        return training_args
