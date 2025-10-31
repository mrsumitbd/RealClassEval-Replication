import torch
import gc
import psutil
from typing import Dict, Any


class MemoryManager:
    '''Simple memory manager that leverages PyTorch's built-in memory optimizations.'''

    def __init__(self):
        '''Initialize the memory manager.'''
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

    def get_memory_info(self) -> Dict[str, Any]:
        '''Get current memory usage information.'''
        info = {}
        if torch.cuda.is_available():
            info['cuda'] = {
                'allocated': torch.cuda.memory_allocated(self.device),
                'reserved': torch.cuda.memory_reserved(self.device),
                'max_allocated': torch.cuda.max_memory_allocated(self.device),
                'max_reserved': torch.cuda.max_memory_reserved(self.device),
                'free': torch.cuda.get_device_properties(self.device).total_memory - torch.cuda.memory_reserved(self.device),
                'total': torch.cuda.get_device_properties(self.device).total_memory,
            }
        info['cpu'] = {
            'rss': psutil.Process().memory_info().rss,
            'vms': psutil.Process().memory_info().vms,
            'available': psutil.virtual_memory().available,
            'used': psutil.virtual_memory().used,
            'total': psutil.virtual_memory().total,
        }
        return info

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
            if force:
                torch.cuda.reset_peak_memory_stats(self.device)

    def get_optimal_training_config(self) -> Dict[str, Any]:
        '''Get recommended configurations for model training based on hardware capabilities.'''
        config = {}
        if torch.cuda.is_available():
            total_mem = torch.cuda.get_device_properties(
                self.device).total_memory
            # Heuristic: batch size based on available memory (very rough estimate)
            if total_mem >= 24 * 1024 ** 3:
                batch_size = 64
            elif total_mem >= 12 * 1024 ** 3:
                batch_size = 32
            elif total_mem >= 6 * 1024 ** 3:
                batch_size = 16
            else:
                batch_size = 8
            config['device'] = 'cuda'
            config['batch_size'] = batch_size
            config['pin_memory'] = True
            config['num_workers'] = min(
                8, psutil.cpu_count(logical=False) or 2)
            config['amp'] = True
        else:
            config['device'] = 'cpu'
            config['batch_size'] = 8
            config['pin_memory'] = False
            config['num_workers'] = min(
                2, psutil.cpu_count(logical=False) or 1)
            config['amp'] = False
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        model = model.to(self.device)
        if torch.cuda.is_available():
            model = torch.compile(model, mode="default") if hasattr(
                torch, "compile") else model
        return model

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        optimal = self.get_optimal_training_config()
        for k, v in optimal.items():
            if hasattr(training_args, k):
                setattr(training_args, k, v)
            elif isinstance(training_args, dict):
                training_args[k] = v
        return training_args
