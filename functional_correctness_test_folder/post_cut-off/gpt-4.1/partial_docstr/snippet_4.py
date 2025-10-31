
import gc
import torch
import psutil
from typing import Dict, Any


class MemoryManager:

    def __init__(self):
        pass

    def get_memory_info(self) -> Dict[str, Any]:
        mem = psutil.virtual_memory()
        info = {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "free": mem.free,
            "percent": mem.percent
        }
        if torch.cuda.is_available():
            info["cuda"] = {
                "total": torch.cuda.get_device_properties(0).total_memory,
                "reserved": torch.cuda.memory_reserved(0),
                "allocated": torch.cuda.memory_allocated(0),
                "free": torch.cuda.memory_reserved(0) - torch.cuda.memory_allocated(0)
            }
        return info

    def cleanup_memory(self, force: bool = False) -> None:
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        if force:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        config = {
            "batch_size": 32,
            "gradient_accumulation_steps": 1,
            "fp16": torch.cuda.is_available(),
            "pin_memory": torch.cuda.is_available(),
            "num_workers": 4 if psutil.cpu_count(logical=False) else 2
        }
        if torch.cuda.is_available():
            total_mem = torch.cuda.get_device_properties(0).total_memory
            if total_mem < 8 * 1024 ** 3:
                config["batch_size"] = 8
            elif total_mem < 16 * 1024 ** 3:
                config["batch_size"] = 16
            else:
                config["batch_size"] = 32
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        if hasattr(torch, "compile"):
            try:
                model = torch.compile(model)
            except Exception:
                pass
        if hasattr(model, "to"):
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = model.to(device)
        return model

    def optimize_training_args(self, training_args):
        if hasattr(training_args, "fp16") and torch.cuda.is_available():
            training_args.fp16 = True
        if hasattr(training_args, "pin_memory") and torch.cuda.is_available():
            training_args.pin_memory = True
        if hasattr(training_args, "batch_size"):
            total_mem = torch.cuda.get_device_properties(
                0).total_memory if torch.cuda.is_available() else 0
            if total_mem < 8 * 1024 ** 3:
                training_args.batch_size = min(training_args.batch_size, 8)
            elif total_mem < 16 * 1024 ** 3:
                training_args.batch_size = min(training_args.batch_size, 16)
            else:
                training_args.batch_size = min(training_args.batch_size, 32)
        return training_args
