import torch
import gc
import psutil
from typing import Dict, Any


class MemoryManager:
    '''Simple memory manager that leverages PyTorch's built-in memory optimizations.'''

    def __init__(self):
        '''Initialize the memory manager.'''
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

    def get_memory_info(self) -> Dict[str, Any]:
        '''Get current memory usage information.'''
        info = {}
        # CPU memory
        vm = psutil.virtual_memory()
        info['cpu_total'] = vm.total
        info['cpu_available'] = vm.available
        info['cpu_used'] = vm.used
        info['cpu_percent'] = vm.percent
        # CUDA memory
        if torch.cuda.is_available():
            info['cuda_device_count'] = torch.cuda.device_count()
            info['cuda'] = []
            for i in range(torch.cuda.device_count()):
                stats = {}
                stats['device'] = i
                stats['name'] = torch.cuda.get_device_name(i)
                stats['total'] = torch.cuda.get_device_properties(
                    i).total_memory
                stats['allocated'] = torch.cuda.memory_allocated(i)
                stats['reserved'] = torch.cuda.memory_reserved(i)
                stats['free'] = stats['reserved'] - stats['allocated']
                stats['max_allocated'] = torch.cuda.max_memory_allocated(i)
                stats['max_reserved'] = torch.cuda.max_memory_reserved(i)
                info['cuda'].append(stats)
        return info

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
            if force:
                for i in range(torch.cuda.device_count()):
                    torch.cuda.reset_peak_memory_stats(i)

    def get_optimal_training_config(self) -> Dict[str, Any]:
        '''Get recommended configurations for model training based on hardware capabilities.'''
        config = {}
        if torch.cuda.is_available():
            total_mem = torch.cuda.get_device_properties(
                self.device).total_memory
            # Heuristic: leave 10% for system, batch size based on 90% of memory
            config['device'] = str(self.device)
            config['mixed_precision'] = True
            config['pin_memory'] = True
            config['num_workers'] = min(
                8, psutil.cpu_count(logical=False) or 2)
            config['max_memory_bytes'] = int(total_mem * 0.9)
            # Suggest batch size (very rough estimate, depends on model)
            config['suggested_batch_size'] = max(
                1, int(config['max_memory_bytes'] // (1024**2 * 32)))  # 32MB per sample
        else:
            config['device'] = 'cpu'
            config['mixed_precision'] = False
            config['pin_memory'] = False
            config['num_workers'] = min(
                4, psutil.cpu_count(logical=False) or 1)
            config['max_memory_bytes'] = int(
                psutil.virtual_memory().available * 0.8)
            config['suggested_batch_size'] = max(
                1, int(config['max_memory_bytes'] // (1024**2 * 32)))
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        model = model.to(self.device)
        if torch.cuda.is_available():
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.enabled = True
            if hasattr(model, 'half'):
                try:
                    model = model.half()
                except Exception:
                    pass  # Not all models support .half()
        return model

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        if hasattr(training_args, 'pin_memory'):
            training_args.pin_memory = torch.cuda.is_available()
        if hasattr(training_args, 'num_workers'):
            training_args.num_workers = min(
                8, psutil.cpu_count(logical=False) or 2)
        if hasattr(training_args, 'device'):
            training_args.device = self.device
        if hasattr(training_args, 'fp16'):
            training_args.fp16 = torch.cuda.is_available()
        if hasattr(training_args, 'gradient_accumulation_steps'):
            # Try to increase grad accumulation if batch size is small
            if getattr(training_args, 'per_device_train_batch_size', 0) < 8:
                training_args.gradient_accumulation_steps = max(
                    1, 8 // max(1, getattr(training_args, 'per_device_train_batch_size', 1)))
        return training_args
