
from typing import Dict, Any
import torch
import gc


class MemoryManager:
    '''Simple memory manager that leverages PyTorch's built-in memory optimizations.'''

    def __init__(self):
        '''Initialize the memory manager.'''
        self.has_cuda = torch.cuda.is_available()
        if self.has_cuda:
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")

    def get_memory_info(self) -> Dict[str, Any]:
        '''Get current memory usage information.'''
        info = {}
        if self.has_cuda:
            info['cuda'] = {
                'allocated': torch.cuda.memory_allocated(),
                'reserved': torch.cuda.memory_reserved(),
                'max_allocated': torch.cuda.max_memory_allocated(),
                'max_reserved': torch.cuda.max_memory_reserved(),
                'device_count': torch.cuda.device_count(),
                'device_name': torch.cuda.get_device_name(self.device),
            }
        else:
            info['cuda'] = None
        # CPU memory info is not as detailed in PyTorch, but we can provide process info
        import psutil
        import os
        process = psutil.Process(os.getpid())
        info['cpu'] = {
            'rss': process.memory_info().rss,
            'vms': process.memory_info().vms,
        }
        return info

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
        gc.collect()
        if self.has_cuda:
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
            if force:
                torch.cuda.reset_peak_memory_stats()
                torch.cuda.reset_accumulated_memory_stats()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        '''Get recommended configurations for model training based on hardware capabilities.'''
        config = {}
        if self.has_cuda:
            total_mem = torch.cuda.get_device_properties(
                self.device).total_memory
            # Heuristic: batch size based on available memory
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
            config['mixed_precision'] = True
        else:
            config['device'] = 'cpu'
            config['batch_size'] = 4
            config['pin_memory'] = False
            config['num_workers'] = 0
            config['mixed_precision'] = False
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        if self.has_cuda:
            model = model.to(self.device)
            # Enable cudnn benchmark for faster training if input sizes are constant
            torch.backends.cudnn.benchmark = True
            # Enable cudnn deterministic for reproducibility if needed
            torch.backends.cudnn.deterministic = False
        else:
            model = model.to('cpu')
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
