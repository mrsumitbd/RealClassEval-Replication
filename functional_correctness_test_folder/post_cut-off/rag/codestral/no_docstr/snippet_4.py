
import torch
import gc
import psutil
from typing import Dict, Any


class MemoryManager:
    '''Simple memory manager that leverages PyTorch's built-in memory optimizations.'''

    def __init__(self):
        '''Initialize the memory manager.'''
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')

    def get_memory_info(self) -> Dict[str, Any]:
        '''Get current memory usage information.'''
        memory_info = {
            'cpu_total': psutil.virtual_memory().total,
            'cpu_available': psutil.virtual_memory().available,
            'cpu_percent': psutil.virtual_memory().percent,
            'gpu_total': torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else 0,
            'gpu_allocated': torch.cuda.memory_allocated() if torch.cuda.is_available() else 0,
            'gpu_cached': torch.cuda.memory_reserved() if torch.cuda.is_available() else 0
        }
        return memory_info

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            if force:
                torch.cuda.reset_max_memory_allocated()
                torch.cuda.reset_max_memory_cached()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        '''Get recommended configurations for model training based on hardware capabilities.'''
        config = {
            'batch_size': 32,
            'gradient_accumulation_steps': 1,
            'fp16': False,
            'gradient_checkpointing': False
        }

        if torch.cuda.is_available():
            total_memory = torch.cuda.get_device_properties(0).total_memory
            if total_memory > 16 * 1024**3:  # More than 16GB
                config['batch_size'] = 64
                config['fp16'] = True
            elif total_memory > 8 * 1024**3:  # More than 8GB
                config['batch_size'] = 32
                config['fp16'] = True
            else:
                config['batch_size'] = 16
                config['gradient_accumulation_steps'] = 2
                config['gradient_checkpointing'] = True

        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        if torch.cuda.is_available():
            model = model.to(self.device)
            model = torch.compile(model) if hasattr(
                torch, 'compile') else model
        return model

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        optimal_config = self.get_optimal_training_config()

        training_args.per_device_train_batch_size = optimal_config['batch_size']
        training_args.gradient_accumulation_steps = optimal_config['gradient_accumulation_steps']
        training_args.fp16 = optimal_config['fp16']

        if optimal_config['gradient_checkpointing']:
            training_args.gradient_checkpointing = True
            training_args.gradient_checkpointing_kwargs = {
                'use_reentrant': False}

        return training_args
