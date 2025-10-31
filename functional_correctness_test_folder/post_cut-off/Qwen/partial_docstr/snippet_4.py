
from typing import Dict, Any
import torch
import gc


class MemoryManager:

    def __init__(self):
        self.memory_info = {}

    def get_memory_info(self) -> Dict[str, Any]:
        self.memory_info['allocated'] = torch.cuda.memory_allocated(
        ) if torch.cuda.is_available() else 0
        self.memory_info['cached'] = torch.cuda.memory_reserved(
        ) if torch.cuda.is_available() else 0
        self.memory_info['available'] = torch.cuda.get_device_properties(
            0).total_memory - self.memory_info['cached'] if torch.cuda.is_available() else 0
        return self.memory_info

    def cleanup_memory(self, force: bool = False) -> None:
        if force:
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None

    def get_optimal_training_config(self) -> Dict[str, Any]:
        return {
            'batch_size': 32,
            'gradient_accumulation_steps': 2,
            'fp16': True if torch.cuda.is_available() else False,
            'num_workers': 4
        }

    def optimize_model_for_training(self, model):
        if torch.cuda.is_available():
            model = model.to('cuda')
        model = torch.nn.DataParallel(model)
        torch.backends.cudnn.benchmark = True
        return model

    def optimize_training_args(self, training_args):
        training_args.gradient_accumulation_steps = 2
        training_args.fp16 = True if torch.cuda.is_available() else False
        training_args.num_workers = 4
        return training_args
