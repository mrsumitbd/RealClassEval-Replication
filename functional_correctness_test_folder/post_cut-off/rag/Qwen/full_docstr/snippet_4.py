
import torch
import gc
from typing import Dict, Any


class MemoryManager:
    '''Simple memory manager that leverages PyTorch's built-in memory optimizations.'''

    def __init__(self):
        '''Initialize the memory manager.'''
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

    def get_memory_info(self) -> Dict[str, Any]:
        '''Get current memory usage information.'''
        if self.device.type == 'cuda':
            memory_info = torch.cuda.memory_summary(
                device=self.device.index, abbreviated=True)
            return {
                'memory_allocated': torch.cuda.memory_allocated(self.device.index),
                'max_memory_allocated': torch.cuda.max_memory_allocated(self.device.index),
                'memory_reserved': torch.cuda.memory_reserved(self.device.index),
                'max_memory_reserved': torch.cuda.max_memory_reserved(self.device.index),
                'memory_summary': memory_info
            }
        else:
            return {
                'memory_allocated': 0,
                'max_memory_allocated': 0,
                'memory_reserved': 0,
                'max_memory_reserved': 0,
                'memory_summary': 'No CUDA device available'
            }

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
        gc.collect()
        if self.device.type == 'cuda':
            torch.cuda.empty_cache()
            if force:
                torch.cuda.ipc_collect()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        '''Get recommended configurations for model training based on hardware capabilities.'''
        config = {
            'device': self.device.type,
            'pin_memory': self.device.type == 'cuda',
            'num_workers': 4 if self.device.type == 'cuda' else 0,
            'batch_size': 32 if self.device.type == 'cuda' else 16
        }
        if self.device.type == 'cuda':
            config['gradient_accumulation_steps'] = 2
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        model.to(self.device)
        if self.device.type == 'cuda':
            model = torch.nn.DataParallel(model)
        return model

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        training_args.device = self.device
        training_args.pin_memory = self.device.type == 'cuda'
        training_args.num_workers = 4 if self.device.type == 'cuda' else 0
        training_args.batch_size = 32 if self.device.type == 'cuda' else 16
        if self.device.type == 'cuda':
            training_args.gradient_accumulation_steps = 2
        return training_args
