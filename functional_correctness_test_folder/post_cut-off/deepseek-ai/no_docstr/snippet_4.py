
import psutil
import torch
from typing import Dict, Any


class MemoryManager:

    def __init__(self):
        pass

    def get_memory_info(self) -> Dict[str, Any]:
        memory_info = psutil.virtual_memory()
        return {
            "total": memory_info.total,
            "available": memory_info.available,
            "used": memory_info.used,
            "free": memory_info.free,
            "percent": memory_info.percent
        }

    def cleanup_memory(self, force: bool = False) -> None:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        if force:
            import gc
            gc.collect()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        memory_info = self.get_memory_info()
        config = {
            "batch_size": 32,
            "precision": "fp16",
            "gradient_accumulation_steps": 2
        }
        if memory_info["available"] < 4 * 1024 ** 3:  # Less than 4GB
            config["batch_size"] = 8
            config["gradient_accumulation_steps"] = 4
        elif memory_info["available"] < 8 * 1024 ** 3:  # Less than 8GB
            config["batch_size"] = 16
            config["gradient_accumulation_steps"] = 2
        return config

    def optimize_model_for_training(self, model):
        if torch.cuda.is_available():
            model = model.cuda()
        model.train()
        return model

    def optimize_training_args(self, training_args):
        optimal_config = self.get_optimal_training_config()
        training_args.batch_size = optimal_config["batch_size"]
        training_args.fp16 = optimal_config["precision"] == "fp16"
        training_args.gradient_accumulation_steps = optimal_config["gradient_accumulation_steps"]
        return training_args
