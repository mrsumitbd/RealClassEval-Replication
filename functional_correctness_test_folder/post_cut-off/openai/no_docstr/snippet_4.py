
import gc
import os
from typing import Any, Dict

import psutil
import torch
from transformers import TrainingArguments


class MemoryManager:
    """
    Utility class for monitoring and optimizing GPU/CPU memory usage during
    model training with Hugging Face Transformers.
    """

    def __init__(self):
        # Detect if CUDA is available
        self.cuda_available = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.cuda_available else "cpu")

    def get_memory_info(self) -> Dict[str, Any]:
        """
        Return a dictionary with system memory statistics.
        """
        mem = psutil.virtual_memory()
        info = {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent,
        }

        if self.cuda_available:
            gpu_info = torch.cuda.memory_stats()
            info.update(
                {
                    "gpu_total": torch.cuda.get_device_properties(self.device).total_memory,
                    "gpu_reserved": gpu_info["reserved_bytes.all.current"],
                    "gpu_allocated": gpu_info["allocated_bytes.all.current"],
                    "gpu_free": gpu_info["reserved_bytes.all.current"]
                    - gpu_info["allocated_bytes.all.current"],
                }
            )
        return info

    def cleanup_memory(self, force: bool = False) -> None:
        """
        Clean up memory by emptying CUDA cache and running garbage collection.
        If `force` is True, also clears all CUDA tensors.
        """
        if self.cuda_available:
            torch.cuda.empty_cache()
            if force:
                # Delete all CUDA tensors that are not referenced
                for obj in gc.get_objects():
                    try:
                        if torch.is_tensor(obj) and obj.is_cuda:
                            del obj
                    except Exception:
                        pass
        gc.collect()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        """
        Estimate an optimal batch size and gradient accumulation steps based on
        available GPU memory. This is a heuristic and may need tuning.
        """
        if not self.cuda_available:
            # Default CPU config
            return {"per_device_train_batch_size": 8, "gradient_accumulation_steps": 1}

        # Rough estimate: use 80% of free GPU memory for training
        gpu_props = torch.cuda.get_device_properties(self.device)
        free_mem = torch.cuda.memory_reserved(
            self.device) - torch.cuda.memory_allocated(self.device)
        target_mem = int(0.8 * free_mem)

        # Assume each sample requires ~50 MB of GPU memory (this is a placeholder)
        sample_mem = 50 * 1024 * 1024
        batch_size = max(1, target_mem // sample_mem)

        # Ensure batch size is a power of two for efficiency
        while batch_size % 2 == 0 and batch_size > 1:
            batch_size //= 2

        return {"per_device_train_batch_size": batch_size, "gradient_accumulation_steps": 1}

    def optimize_model_for_training(self, model):
        """
        Move the model to the appropriate device and optionally cast to half precision
        if the device supports it.
        """
        model.to(self.device)
        if self.cuda_available and torch.cuda.is_bf16_supported():
            # Use bfloat16 if available for better performance
            model.half()
        elif self.cuda_available and torch.cuda.is_available():
            # Fallback to float16
            model.half()
        return model

    def optimize_training_args(self, training_args: TrainingArguments) -> TrainingArguments:
        """
        Adjust training arguments based on available memory.
        """
        optimal = self.get_optimal_training_config()
        training_args.per_device_train_batch_size = optimal["per_device_train_batch_size"]
        training_args.gradient_accumulation_steps = optimal["gradient_accumulation_steps"]

        # Enable mixed precision if supported
        if self.cuda_available:
            training_args.fp16 = True
            training_args.bf16 = torch.cuda.is_bf16_supported()

        return training_args
