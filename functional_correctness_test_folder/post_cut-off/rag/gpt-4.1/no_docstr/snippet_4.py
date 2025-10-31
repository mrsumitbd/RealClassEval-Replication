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
                'allocated': torch.cuda.memory_allocated(),
                'reserved': torch.cuda.memory_reserved(),
                'max_allocated': torch.cuda.max_memory_allocated(),
                'max_reserved': torch.cuda.max_memory_reserved(),
                'device_count': torch.cuda.device_count(),
                'device_name': torch.cuda.get_device_name(self.device),
            }
        info['cpu'] = {
            'virtual_memory': dict(psutil.virtual_memory()._asdict()),
            'swap_memory': dict(psutil.swap_memory()._asdict()),
        }
        return info

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
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
        '''Get recommended configurations for model training based on hardware capabilities.'''
        config = {}
        if torch.cuda.is_available():
            total_mem = torch.cuda.get_device_properties(
                self.device).total_memory
            # Recommend batch size based on available memory (very rough estimate)
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
            config['num_workers'] = 4
            config['amp'] = True
        else:
            mem = psutil.virtual_memory().total
            if mem >= 32 * 1024 ** 3:
                batch_size = 32
            elif mem >= 16 * 1024 ** 3:
                batch_size = 16
            else:
                batch_size = 8
            config['device'] = 'cpu'
            config['batch_size'] = batch_size
            config['pin_memory'] = False
            config['num_workers'] = 2
            config['amp'] = False
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        if torch.cuda.is_available():
            model = model.to(self.device)
            model = torch.compile(model) if hasattr(
                torch, "compile") else model
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.enabled = True
        else:
            model = model.to(self.device)
        return model

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        if hasattr(training_args, 'pin_memory'):
            training_args.pin_memory = torch.cuda.is_available()
        if hasattr(training_args, 'num_workers'):
            training_args.num_workers = 4 if torch.cuda.is_available() else 2
        if hasattr(training_args, 'batch_size'):
            optimal = self.get_optimal_training_config()
            training_args.batch_size = optimal['batch_size']
        if hasattr(training_args, 'amp'):
            training_args.amp = torch.cuda.is_available()
        return training_args
