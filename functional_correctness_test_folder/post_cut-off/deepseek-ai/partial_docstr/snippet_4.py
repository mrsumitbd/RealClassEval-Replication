
import torch
from typing import Dict, Any


class MemoryManager:

    def __init__(self):
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')

    def get_memory_info(self) -> Dict[str, Any]:
        if self.device.type == 'cuda':
            memory_info = {
                'total_memory': torch.cuda.get_device_properties(self.device).total_memory,
                'allocated_memory': torch.cuda.memory_allocated(self.device),
                'cached_memory': torch.cuda.memory_reserved(self.device),
                'device_name': torch.cuda.get_device_name(self.device)
            }
        else:
            memory_info = {
                'device': 'CPU',
                'message': 'No GPU memory information available'
            }
        return memory_info

    def cleanup_memory(self, force: bool = False) -> None:
        if self.device.type == 'cuda':
            if force:
                torch.cuda.empty_cache()
            else:
                if torch.cuda.memory_allocated(self.device) > 0:
                    torch.cuda.empty_cache()

    def get_optimal_training_config(self) -> Dict[str, Any]:
        config = {
            'mixed_precision': True,
            'gradient_accumulation_steps': 2,
            'batch_size': 32 if self.device.type == 'cuda' else 8,
            'device': str(self.device)
        }
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        if self.device.type == 'cuda':
            model = model.to(self.device)
            model = torch.compile(model) if hasattr(
                torch, 'compile') else model
        return model

    def optimize_training_args(self, training_args):
        if 'batch_size' not in training_args:
            training_args['batch_size'] = self.get_optimal_training_config()[
                'batch_size']
        if 'device' not in training_args:
            training_args['device'] = str(self.device)
        return training_args
