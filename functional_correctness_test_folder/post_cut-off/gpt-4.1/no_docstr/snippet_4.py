
import gc
import sys
import os
from typing import Dict, Any

try:
    import psutil
except ImportError:
    psutil = None


class MemoryManager:

    def __init__(self):
        pass

    def get_memory_info(self) -> Dict[str, Any]:
        info = {}
        if psutil:
            vm = psutil.virtual_memory()
            info['total'] = vm.total
            info['available'] = vm.available
            info['used'] = vm.used
            info['free'] = vm.free
            info['percent'] = vm.percent
        else:
            info['total'] = None
            info['available'] = None
            info['used'] = None
            info['free'] = None
            info['percent'] = None
        info['python_process_memory'] = self._get_process_memory()
        return info

    def _get_process_memory(self):
        if psutil:
            process = psutil.Process(os.getpid())
            return process.memory_info().rss
        else:
            return None

    def cleanup_memory(self, force: bool = False) -> None:
        gc.collect()
        if force:
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    torch.cuda.ipc_collect()
            except ImportError:
                pass

    def get_optimal_training_config(self) -> Dict[str, Any]:
        mem_info = self.get_memory_info()
        total = mem_info.get('total', 0)
        available = mem_info.get('available', 0)
        # Heuristic: batch size and num_workers based on available memory
        if available and available > 0:
            if available > 16 * 1024 ** 3:
                batch_size = 64
                num_workers = 8
            elif available > 8 * 1024 ** 3:
                batch_size = 32
                num_workers = 4
            elif available > 4 * 1024 ** 3:
                batch_size = 16
                num_workers = 2
            else:
                batch_size = 8
                num_workers = 1
        else:
            batch_size = 8
            num_workers = 1
        return {
            'batch_size': batch_size,
            'num_workers': num_workers
        }

    def optimize_model_for_training(self, model):
        try:
            import torch
            if torch.cuda.is_available():
                model = model.cuda()
                model = model.half()
            else:
                model = model.float()
        except ImportError:
            pass
        return model

    def optimize_training_args(self, training_args):
        config = self.get_optimal_training_config()
        if hasattr(training_args, 'batch_size'):
            training_args.batch_size = config['batch_size']
        if hasattr(training_args, 'num_workers'):
            training_args.num_workers = config['num_workers']
        if isinstance(training_args, dict):
            training_args['batch_size'] = config['batch_size']
            training_args['num_workers'] = config['num_workers']
        return training_args
