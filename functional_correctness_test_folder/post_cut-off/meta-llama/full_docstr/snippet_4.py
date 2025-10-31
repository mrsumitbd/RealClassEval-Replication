
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
        memory_info = {}
        if self.device.type == 'cuda':
            memory_info['cuda_allocated'] = torch.cuda.memory_allocated()
            memory_info['cuda_reserved'] = torch.cuda.memory_reserved()
            memory_info['cuda_max_allocated'] = torch.cuda.max_memory_allocated()
            memory_info['cuda_max_reserved'] = torch.cuda.max_memory_reserved()
        memory_info['cpu_allocated'] = gc.get_count()
        return memory_info

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
        gc.collect()
        if self.device.type == 'cuda':
            torch.cuda.empty_cache()
            if force:
                torch.cuda.ipc_collect()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        '''Get recommended configurations for model training based on hardware capabilities.'''
        config = {}
        if self.device.type == 'cuda':
            config['batch_size'] = 32  # default batch size
            # default gradient accumulation steps
            config['gradient_accumulation_steps'] = 1
            config['fp16'] = True  # use mixed precision training
        else:
            config['batch_size'] = 16  # default batch size for CPU
            # default gradient accumulation steps for CPU
            config['gradient_accumulation_steps'] = 2
            # do not use mixed precision training on CPU
            config['fp16'] = False
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        model.to(self.device)
        if self.device.type == 'cuda':
            # use data parallelism on multiple GPUs
            model = torch.nn.DataParallel(model)

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        if self.device.type == 'cuda':
            training_args['fp16'] = True  # use mixed precision training
            # use gradient checkpointing
            training_args['gradient_checkpointing'] = True
        else:
            # do not use mixed precision training on CPU
            training_args['fp16'] = False
            # do not use gradient checkpointing on CPU
            training_args['gradient_checkpointing'] = False
        return training_args
