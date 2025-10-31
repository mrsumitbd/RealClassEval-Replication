import torch
from typing import Dict, Any
import os
import psutil
import gc

class MemoryManager:
    """Simple memory manager that leverages PyTorch's built-in memory optimizations."""

    def __init__(self):
        """Initialize the memory manager."""
        self.cuda_available = torch.cuda.is_available()
        self.process = psutil.Process(os.getpid())

    def get_memory_info(self) -> Dict[str, Any]:
        """Get current memory usage information."""
        info = {'ram_used_percent': psutil.virtual_memory().percent, 'ram_used_gb': psutil.virtual_memory().used / 1024 ** 3, 'ram_available_gb': psutil.virtual_memory().available / 1024 ** 3, 'ram_total_gb': psutil.virtual_memory().total / 1024 ** 3}
        if self.cuda_available:
            try:
                info.update({'vram_used_gb': torch.cuda.memory_allocated() / 1024 ** 3, 'vram_reserved_gb': torch.cuda.memory_reserved() / 1024 ** 3, 'vram_total_gb': torch.cuda.get_device_properties(0).total_memory / 1024 ** 3})
            except RuntimeError as e:
                logger.warning(f'Error getting CUDA memory info: {str(e)}')
                self.cuda_available = False
        return info

    def cleanup_memory(self, force: bool=False) -> None:
        """Free up memory by garbage collection and emptying CUDA cache."""
        gc.collect()
        if self.cuda_available:
            torch.cuda.empty_cache()
        if force:
            info = self.get_memory_info()
            logger.info(f"Memory after cleanup: RAM: {info['ram_used_gb']:.2f}GB / {info['ram_total_gb']:.2f}GB, VRAM: {info.get('vram_used_gb', 0):.2f}GB / {info.get('vram_total_gb', 0):.2f}GB")

    def get_optimal_training_config(self) -> Dict[str, Any]:
        """Get recommended configurations for model training based on hardware capabilities."""
        config = {'device_map': 'auto', 'fp16': False, 'bf16': False, 'gradient_checkpointing': True, 'gradient_accumulation_steps': 1}
        if self.cuda_available:
            capability = torch.cuda.get_device_capability()
            if capability[0] >= 8:
                config['bf16'] = True
            elif capability[0] >= 7:
                config['fp16'] = True
            vram_gb = self.get_memory_info().get('vram_total_gb', 0)
            if vram_gb < 8:
                config['gradient_accumulation_steps'] = 4
            elif vram_gb < 16:
                config['gradient_accumulation_steps'] = 2
        return config

    def optimize_model_for_training(self, model):
        """Apply PyTorch's built-in memory optimizations for training."""
        if hasattr(model, 'gradient_checkpointing_enable'):
            logger.info('Enabling gradient checkpointing for memory efficiency')
            model.gradient_checkpointing_enable()
        if hasattr(model, 'config'):
            try:
                model.config.use_memory_efficient_attention = True
            except:
                pass
            if self.cuda_available and torch.cuda.get_device_capability()[0] >= 8:
                try:
                    model.config.attn_implementation = 'flash_attention_2'
                except:
                    pass
        return model

    def optimize_training_args(self, training_args):
        """Configure training arguments for efficient memory usage."""
        if not training_args:
            return None
        config = self.get_optimal_training_config()
        if not getattr(training_args, 'fp16', False) and (not getattr(training_args, 'bf16', False)):
            training_args.fp16 = config['fp16']
            training_args.bf16 = config['bf16']
        if not getattr(training_args, 'gradient_checkpointing', False):
            training_args.gradient_checkpointing = config['gradient_checkpointing']
        if training_args.gradient_accumulation_steps == 1:
            training_args.gradient_accumulation_steps = config['gradient_accumulation_steps']
        logger.info('Training configuration optimized for memory efficiency:')
        logger.info(f'  Mixed precision: FP16={training_args.fp16}, BF16={training_args.bf16}')
        logger.info(f'  Gradient checkpointing: {training_args.gradient_checkpointing}')
        logger.info(f'  Gradient accumulation steps: {training_args.gradient_accumulation_steps}')
        return training_args