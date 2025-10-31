
import torch
import gc
from typing import Dict, Any


class MemoryManager:
    '''Simple memory manager that leverages PyTorch's built-in memory optimizations.'''

    def __init__(self):
        '''Initialize the memory manager.'''
        pass

    def get_memory_info(self) -> Dict[str, Any]:
        '''Get current memory usage information.'''
        memory_info = {}
        if torch.cuda.is_available():
            memory_info['cuda_allocated'] = torch.cuda.memory_allocated()
            memory_info['cuda_cached'] = torch.cuda.memory_reserved()
        memory_info['cpu_allocated'] = torch.memory_allocated()
        memory_info['cpu_reserved'] = torch.memory_reserved()
        return memory_info

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        if force:
            torch.cuda.ipc_collect()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        '''Get recommended configurations for model training based on hardware capabilities.'''
        config = {
            'device': 'cuda' if torch.cuda.is_available() else 'cpu',
            'pin_memory': True if torch.cuda.is_available() else False,
            'num_workers': 4,
            'batch_size': 32
        }
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        if torch.cuda.is_available():
            model.cuda()
            model = torch.nn.DataParallel(model)
        model.train()

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        if 'device' not in training_args:
            training_args['device'] = 'cuda' if torch.cuda.is_available(
            ) else 'cpu'
        if 'pin_memory' not in training_args:
            training_args['pin_memory'] = True if torch.cuda.is_available(
            ) else False
        if 'num_workers' not in training_args:
            training_args['num_workers'] = 4
        if 'batch_size' not in training_args:
            training_args['batch_size'] = 32
        return training_args
