
from typing import Dict, Any
import psutil
import gc


class MemoryManager:

    def __init__(self):
        self.memory_info = self.get_memory_info()

    def get_memory_info(self) -> Dict[str, Any]:
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': memory.percent
        }

    def cleanup_memory(self, force: bool = False) -> None:
        gc.collect()
        if force:
            gc.collect(generation=2)

    def get_optimal_training_config(self) -> Dict[str, Any]:
        memory = self.get_memory_info()
        if memory['percent'] > 75:
            return {
                'batch_size': 8,
                'gradient_accumulation_steps': 4
            }
        elif memory['percent'] > 50:
            return {
                'batch_size': 16,
                'gradient_accumulation_steps': 2
            }
        else:
            return {
                'batch_size': 32,
                'gradient_accumulation_steps': 1
            }

    def optimize_model_for_training(self, model):
        model.half()  # Convert model to half precision
        model.to('cuda')  # Move model to GPU if available

    def optimize_training_args(self, training_args):
        training_args.fp16 = True  # Enable mixed precision training
        training_args.logging_dir = './logs'
        training_args.logging_steps = 10
        training_args.save_steps = 100
