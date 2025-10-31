
import torch
import gc
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
            'total_memory': torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else None,
            'allocated_memory': torch.cuda.memory_allocated() if torch.cuda.is_available() else None,
            'cached_memory': torch.cuda.memory_reserved() if torch.cuda.is_available() else None,
            'free_memory': torch.cuda.memory_reserved() - torch.cuda.memory_allocated() if torch.cuda.is_available() else None
        }
        return memory_info

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            if force:
                torch.cuda.ipc_collect()
                torch.cuda.empty_cache()

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
                config['gradient_checkpointing'] = True
            elif total_memory > 8 * 1024**3:  # More than 8GB
                config['batch_size'] = 32
                config['fp16'] = True
                config['gradient_checkpointing'] = True
            else:  # Less than or equal to 8GB
                config['batch_size'] = 16
                config['gradient_accumulation_steps'] = 2

        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        if torch.cuda.is_available():
            model = model.to(self.device)
            model = torch.compile(model)  # Requires PyTorch 2.0 or later
        return model

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        optimal_config = self.get_optimal_training_config()
        training_args.per_device_train_batch_size = optimal_config['batch_size']
        training_args.gradient_accumulation_steps = optimal_config['gradient_accumulation_steps']
        training_args.fp16 = optimal_config['fp16']
        training_args.gradient_checkpointing = optimal_config['gradient_checkpointing']
        return training_args
