
import psutil
import gc
from typing import Dict, Any
import torch


class MemoryManager:

    def __init__(self):
        self.process = psutil.Process()

    def get_memory_info(self) -> Dict[str, Any]:
        mem_info = self.process.memory_info()
        return {
            'rss': mem_info.rss,
            'vms': mem_info.vms,
            'available': psutil.virtual_memory().available,
            'total': psutil.virtual_memory().total,
            'percent': psutil.virtual_memory().percent
        }

    def cleanup_memory(self, force: bool = False) -> None:
        gc.collect()
        if force:
            torch.cuda.empty_cache()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        mem_info = self.get_memory_info()
        available_mem = mem_info['available']
        # Assuming a simple heuristic where we use 80% of available memory
        optimal_batch_size = int(
            (available_mem * 0.8) / (1024 * 1024 * 1024))  # in GB
        return {
            'batch_size': optimal_batch_size,
            'gradient_accumulation_steps': 1 if optimal_batch_size > 16 else 2
        }

    def optimize_model_for_training(self, model):
        # Move model to GPU if available
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        # Enable gradient checkpointing if model supports it
        if hasattr(model, 'gradient_checkpointing_enable'):
            model.gradient_checkpointing_enable()

    def optimize_training_args(self, training_args):
        optimal_config = self.get_optimal_training_config()
        training_args.per_device_train_batch_size = optimal_config['batch_size']
        training_args.gradient_accumulation_steps = optimal_config['gradient_accumulation_steps']
        return training_args
