
import torch
import psutil
import gc
from typing import Dict, Any


class MemoryManager:

    def __init__(self):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

    def get_memory_info(self) -> Dict[str, Any]:
        mem_info = {}
        mem_info['cpu_memory_total'] = psutil.virtual_memory().total / \
            (1024.0 ** 3)
        mem_info['cpu_memory_available'] = psutil.virtual_memory().available / \
            (1024.0 ** 3)
        mem_info['cpu_memory_used'] = psutil.virtual_memory().used / \
            (1024.0 ** 3)
        if self.device.type == 'cuda':
            mem_info['gpu_memory_total'] = torch.cuda.get_device_properties(
                self.device).total_memory / (1024.0 ** 3)
            mem_info['gpu_memory_allocated'] = torch.cuda.memory_allocated(
                self.device) / (1024.0 ** 3)
            mem_info['gpu_memory_reserved'] = torch.cuda.memory_reserved(
                self.device) / (1024.0 ** 3)
        return mem_info

    def cleanup_memory(self, force: bool = False) -> None:
        gc.collect()
        if self.device.type == 'cuda':
            torch.cuda.empty_cache()
            if force:
                torch.cuda.ipc_collect()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        config = {}
        config['device'] = self.device
        if self.device.type == 'cuda':
            config['batch_size'] = 32  # adjust based on GPU memory
        else:
            config['batch_size'] = 16  # adjust based on CPU memory
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        model.to(self.device)
        if self.device.type == 'cuda':
            torch.cuda.amp.autocast(enabled=True)
            model = torch.compile(model, mode="reduce-overhead")

    def optimize_training_args(self, training_args):
        if self.device.type == 'cuda':
            training_args['fp16'] = True  # enable mixed precision training
            # adjust based on GPU memory
            training_args['gradient_accumulation_steps'] = 2
        else:
            training_args['fp16'] = False
        return training_args
