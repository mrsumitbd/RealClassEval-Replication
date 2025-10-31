
import psutil
import torch
from typing import Dict, Any


class MemoryManager:

    def __init__(self):
        self.memory_info = {}
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

    def get_memory_info(self) -> Dict[str, Any]:
        self.memory_info = {
            'total_memory': psutil.virtual_memory().total,
            'available_memory': psutil.virtual_memory().available,
            'used_memory': psutil.virtual_memory().used,
            'gpu_memory': torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else 0,
            'gpu_memory_used': torch.cuda.memory_allocated(0) if torch.cuda.is_available() else 0
        }
        return self.memory_info

    def cleanup_memory(self, force: bool = False) -> None:
        if force:
            torch.cuda.empty_cache()
        else:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        memory_info = self.get_memory_info()
        optimal_config = {
            'batch_size': min(32, int(memory_info['available_memory'] / (1024 ** 3) * 10)),
            'gradient_accumulation_steps': max(1, int(32 / min(32, int(memory_info['available_memory'] / (1024 ** 3) * 10)))),
            'fp16': memory_info['gpu_memory'] > 0
        }
        return optimal_config

    def optimize_model_for_training(self, model):
        if torch.cuda.is_available():
            model = model.to(self.device)
            if self.memory_info['gpu_memory'] > 0:
                model = model.half()
        return model

    def optimize_training_args(self, training_args):
        optimal_config = self.get_optimal_training_config()
        training_args.per_device_train_batch_size = optimal_config['batch_size']
        training_args.gradient_accumulation_steps = optimal_config['gradient_accumulation_steps']
        training_args.fp16 = optimal_config['fp16']
        return training_args
