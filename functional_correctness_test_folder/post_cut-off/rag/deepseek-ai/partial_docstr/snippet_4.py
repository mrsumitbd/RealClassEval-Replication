
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
            memory_info['cuda_reserved'] = torch.cuda.memory_reserved()
            memory_info['cuda_max_allocated'] = torch.cuda.max_memory_allocated()
            memory_info['cuda_max_reserved'] = torch.cuda.max_memory_reserved()
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
        config = {}
        if torch.cuda.is_available():
            config['device'] = 'cuda'
            config['mixed_precision'] = True
            config['gradient_accumulation_steps'] = 2
        else:
            config['device'] = 'cpu'
            config['mixed_precision'] = False
            config['gradient_accumulation_steps'] = 1
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        if torch.cuda.is_available():
            model = model.cuda()
            model = torch.nn.DataParallel(
                model) if torch.cuda.device_count() > 1 else model
        return model

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        if torch.cuda.is_available():
            training_args['use_cuda'] = True
            training_args['fp16'] = True
        else:
            training_args['use_cuda'] = False
            training_args['fp16'] = False
        return training_args
