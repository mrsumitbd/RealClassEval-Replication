
import torch
import psutil
from typing import Dict, Any


class MemoryManager:

    def __init__(self):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

    def get_memory_info(self) -> Dict[str, Any]:
        memory_info = {
            "total_memory": psutil.virtual_memory().total,
            "available_memory": psutil.virtual_memory().available,
            "used_memory": psutil.virtual_memory().used,
            "gpu_memory": torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else 0,
            "gpu_memory_allocated": torch.cuda.memory_allocated() if torch.cuda.is_available() else 0,
            "gpu_memory_cached": torch.cuda.memory_reserved() if torch.cuda.is_available() else 0
        }
        return memory_info

    def cleanup_memory(self, force: bool = False) -> None:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            if force:
                torch.cuda.ipc_collect()
                torch.cuda.empty_cache()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        memory_info = self.get_memory_info()
        optimal_config = {
            "batch_size": min(32, int(memory_info["available_memory"] / (1024 ** 3) * 10)),
            "gradient_accumulation_steps": max(1, int(32 / min(32, int(memory_info["available_memory"] / (1024 ** 3) * 10)))),
            "fp16": memory_info["gpu_memory"] > 0,
            "fp16_opt_level": "O1" if memory_info["gpu_memory"] > 0 else "O0"
        }
        return optimal_config

    def optimize_model_for_training(self, model):
        if torch.cuda.is_available():
            model = model.to(self.device)
            model = torch.nn.DataParallel(model)
        return model

    def optimize_training_args(self, training_args):
        optimal_config = self.get_optimal_training_config()
        training_args.per_device_train_batch_size = optimal_config["batch_size"]
        training_args.gradient_accumulation_steps = optimal_config["gradient_accumulation_steps"]
        training_args.fp16 = optimal_config["fp16"]
        training_args.fp16_opt_level = optimal_config["fp16_opt_level"]
        return training_args
