
import gc
import torch
from typing import Any, Dict


class MemoryManager:
    '''Simple memory manager that leverages PyTorch's built-in memory optimizations.'''

    def __init__(self):
        '''Initialize the memory manager.'''
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

    def get_memory_info(self) -> Dict[str, Any]:
        '''Get current memory usage information.'''
        info: Dict[str, Any] = {}
        if torch.cuda.is_available():
            info["cuda_allocated"] = torch.cuda.memory_allocated(self.device)
            info["cuda_reserved"] = torch.cuda.memory_reserved(self.device)
            info["cuda_max_allocated"] = torch.cuda.max_memory_allocated(
                self.device)
            info["cuda_max_reserved"] = torch.cuda.max_memory_reserved(
                self.device)
            info["cuda_summary"] = torch.cuda.memory_summary(self.device)
        else:
            info["cuda_allocated"] = 0
            info["cuda_reserved"] = 0
            info["cuda_max_allocated"] = 0
            info["cuda_max_reserved"] = 0
            info["cuda_summary"] = "CUDA not available"
        # CPU memory usage (approximate)
        try:
            import psutil
            process = psutil.Process()
            info["cpu_memory"] = process.memory_info().rss
        except Exception:
            info["cpu_memory"] = None
        return info

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
        gc.collect()
        if torch.cuda.is_available() and (force or True):
            torch.cuda.empty_cache()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        '''Get recommended configurations for model training based on hardware capabilities.'''
        config: Dict[str, Any] = {}
        if torch.cuda.is_available():
            # Rough heuristic: batch size proportional to available GPU memory
            free_mem = torch.cuda.get_device_properties(
                self.device).total_memory - torch.cuda.memory_reserved(self.device)
            # Assume each sample uses ~4MB of GPU memory (this is a placeholder)
            batch_size = max(1, int(free_mem // (4 * 1024 * 1024)))
            config["device"] = "cuda"
            config["batch_size"] = batch_size
            config["gradient_accumulation_steps"] = 1
        else:
            config["device"] = "cpu"
            config["batch_size"] = 8
            config["gradient_accumulation_steps"] = 4
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        if torch.cuda.is_available():
            # Use mixed precision if possible
            model = model.to(self.device)
            if hasattr(model, "half"):
                model.half()
        else:
            model = model.to(self.device)
        return model

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        # Assume training_args is a dict-like object
        if not isinstance(training_args, dict):
            raise TypeError("training_args must be a dict")
        # Adjust gradient accumulation based on available memory
        if torch.cuda.is_available():
            free_mem = torch.cuda.get_device_properties(
                self.device).total_memory - torch.cuda.memory_reserved(self.device)
            # If free memory is low, increase accumulation steps
            if free_mem < 2 * 1024 * 1024 * 1024:  # less than 2GB
                training_args["gradient_accumulation_steps"] = max(
                    1, training_args.get("gradient_accumulation_steps", 1) * 2)
        else:
            # On CPU, use smaller batch size
            training_args["gradient_accumulation_steps"] = max(
                1, training_args.get("gradient_accumulation_steps", 1) * 4)
        return training_args
