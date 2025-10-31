from typing import Dict, Any, Optional
import gc
import os
import math
import multiprocessing

try:
    import psutil  # Optional, for CPU mem info
except Exception:
    psutil = None

try:
    import torch
except Exception:  # Fallback stub if torch isn't available
    torch = None


class MemoryManager:
    '''Simple memory manager that leverages PyTorch's built-in memory optimizations.'''

    def __init__(self):
        '''Initialize the memory manager.'''
        self.torch_available = torch is not None
        self.cuda_available = bool(
            self.torch_available and torch.cuda.is_available())
        self.mps_available = bool(
            self.torch_available
            and hasattr(torch.backends, "mps")
            and torch.backends.mps.is_available()
        )

    def get_memory_info(self) -> Dict[str, Any]:
        '''Get current memory usage information.'''
        info: Dict[str, Any] = {
            "framework": "torch" if self.torch_available else "none",
            "devices": [],
            "cpu": {},
        }

        # CPU memory
        if psutil is not None:
            vm = psutil.virtual_memory()
            info["cpu"] = {
                "total": int(vm.total),
                "available": int(vm.available),
                "used": int(vm.used),
                "percent": float(vm.percent),
            }

        # CUDA devices
        if self.cuda_available:
            num_devices = torch.cuda.device_count()
            for idx in range(num_devices):
                props = torch.cuda.get_device_properties(idx)
                name = props.name
                total_mem = int(props.total_memory)
                free_mem, total_reported = torch.cuda.mem_get_info(idx)
                # Runtime memory stats
                alloc = int(torch.cuda.memory_allocated(idx))
                reserved = int(torch.cuda.memory_reserved(idx))
                max_alloc = int(torch.cuda.max_memory_allocated(idx))
                max_reserved = int(torch.cuda.max_memory_reserved(idx))

                info["devices"].append({
                    "type": "cuda",
                    "index": idx,
                    "name": name,
                    "capability": f"{props.major}.{props.minor}",
                    "total_memory": total_mem,
                    "total_memory_reported": int(total_reported),
                    "free_memory": int(free_mem),
                    "allocated": alloc,
                    "reserved": reserved,
                    "max_allocated": max_alloc,
                    "max_reserved": max_reserved,
                })

        # MPS device (Apple)
        if self.mps_available:
            # PyTorch doesn't expose detailed MPS mem metrics. Provide capability flag.
            info["devices"].append({
                "type": "mps",
                "index": 0,
                "name": "Apple MPS",
                "capability": "N/A",
            })

        # CPU-only device
        if not self.cuda_available and not self.mps_available:
            info["devices"].append({
                "type": "cpu",
                "index": 0,
                "name": "CPU",
                "capability": "N/A",
            })

        return info

    def cleanup_memory(self, force: bool = False) -> None:
        '''Free up memory by garbage collection and emptying CUDA cache.'''
        # Python GC
        gc.collect()

        if not self.torch_available:
            return

        # CUDA clean-up
        if self.cuda_available:
            try:
                torch.cuda.empty_cache()
            except Exception:
                pass
            try:
                torch.cuda.ipc_collect()
            except Exception:
                pass
            if force:
                try:
                    for i in range(torch.cuda.device_count()):
                        torch.cuda.synchronize(i)
                except Exception:
                    pass
                try:
                    torch.cuda.reset_peak_memory_stats()
                except Exception:
                    pass

        # MPS has implicit memory management; no explicit cache empty function

    def get_optimal_training_config(self) -> Dict[str, Any]:
        '''Get recommended configurations for model training based on hardware capabilities.'''
        config: Dict[str, Any] = {}

        use_cuda = self.cuda_available
        use_mps = self.mps_available

        # Mixed precision policy
        mixed_precision = "no"
        if use_cuda:
            bf16_supported = False
            try:
                bf16_supported = bool(
                    getattr(torch.cuda, "is_bf16_supported", lambda: False)())
            except Exception:
                # Heuristic via compute capability (>= 8.0 often supports bf16)
                try:
                    props = torch.cuda.get_device_properties(0)
                    bf16_supported = props.major >= 8
                except Exception:
                    bf16_supported = False
            mixed_precision = "bf16" if bf16_supported else "fp16"
        elif use_mps:
            # fp16 often works on MPS; leave room for user override
            mixed_precision = "fp16"
        else:
            mixed_precision = "no"

        # TF32
        allow_tf32 = False
        if use_cuda:
            try:
                props = torch.cuda.get_device_properties(0)
                allow_tf32 = props.major >= 8  # Ampere+ (8.x) recommended
            except Exception:
                allow_tf32 = False

        # torch.compile availability
        can_compile = bool(self.torch_available and hasattr(torch, "compile"))

        # Data loader workers
        cpu_count = max(1, (multiprocessing.cpu_count() if hasattr(
            multiprocessing, "cpu_count") else 1))
        num_workers = max(0, min(4, cpu_count - 1))

        # Pin memory if using CUDA
        pin_memory = bool(use_cuda)

        # Gradient checkpointing default on for memory savings
        gradient_checkpointing = True

        # Gradient accumulation (heuristic)
        grad_accum = 1
        if use_cuda:
            try:
                props = torch.cuda.get_device_properties(0)
                vram_gb = props.total_memory / (1024 ** 3)
                # Increase accumulation on small GPUs
                if vram_gb < 8:
                    grad_accum = 4
                elif vram_gb < 12:
                    grad_accum = 2
                else:
                    grad_accum = 1
            except Exception:
                grad_accum = 1
        elif use_mps:
            grad_accum = 2

        # Optimizer choice
        optim = "adamw_torch"

        config.update({
            "device": "cuda" if use_cuda else ("mps" if use_mps else "cpu"),
            "mixed_precision": mixed_precision,  # "bf16", "fp16", or "no"
            "tf32": allow_tf32,
            "gradient_checkpointing": gradient_checkpointing,
            "torch_compile": can_compile,
            # safe/beneficial for many conv nets on CUDA
            "channels_last": bool(use_cuda),
            "dataloader_pin_memory": pin_memory,
            "dataloader_num_workers": num_workers,
            "gradient_accumulation_steps": grad_accum,
            "optim": optim,
        })
        return config

    def optimize_model_for_training(self, model):
        '''Apply PyTorch's built-in memory optimizations for training.'''
        if not self.torch_available:
            return model

        # Enable TF32 if recommended
        cfg = self.get_optimal_training_config()
        try:
            if cfg.get("tf32", False) and hasattr(torch.backends, "cuda"):
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
        except Exception:
            pass

        # Use channels_last if beneficial (mostly conv nets); safe to set, no-op for non-4D
        try:
            if cfg.get("channels_last", False):
                model = model.to(memory_format=torch.channels_last)
        except Exception:
            pass

        # Enable gradient checkpointing if model supports it
        try:
            if cfg.get("gradient_checkpointing", False):
                if hasattr(model, "gradient_checkpointing_enable"):
                    model.gradient_checkpointing_enable()
                elif hasattr(model, "enable_input_require_grads"):
                    # Some HF models need inputs to require grads
                    model.enable_input_require_grads()
        except Exception:
            pass

        # torch.compile for training if available
        try:
            if cfg.get("torch_compile", False):
                model = torch.compile(model)
        except Exception:
            # Fallback silently if compilation fails
            pass

        return model

    def optimize_training_args(self, training_args):
        '''Configure training arguments for efficient memory usage.'''
        cfg = self.get_optimal_training_config()

        def set_arg(obj, key, value):
            if isinstance(obj, dict):
                obj[key] = value
            else:
                if hasattr(obj, key):
                    setattr(obj, key, value)

        # Mixed precision settings (cover common libraries like HF)
        mp = cfg["mixed_precision"]
        if mp == "bf16":
            set_arg(training_args, "bf16", True)
            set_arg(training_args, "fp16", False)
            set_arg(training_args, "bf16_full_eval", True)
        elif mp == "fp16":
            set_arg(training_args, "fp16", True)
            set_arg(training_args, "bf16", False)
            set_arg(training_args, "fp16_full_eval", True)
        else:
            set_arg(training_args, "fp16", False)
            set_arg(training_args, "bf16", False)

        # TF32
        set_arg(training_args, "tf32", bool(cfg.get("tf32", False)))

        # Gradient checkpointing
        set_arg(training_args, "gradient_checkpointing",
                bool(cfg.get("gradient_checkpointing", True)))

        # Gradient accumulation
        set_arg(training_args, "gradient_accumulation_steps",
                int(cfg.get("gradient_accumulation_steps", 1)))

        # torch.compile
        set_arg(training_args, "torch_compile",
                bool(cfg.get("torch_compile", False)))

        # Optimizer
        set_arg(training_args, "optim", cfg.get("optim", "adamw_torch"))

        # DataLoader settings
        set_arg(training_args, "dataloader_pin_memory",
                bool(cfg.get("dataloader_pin_memory", False)))
        set_arg(training_args, "dataloader_num_workers",
                int(cfg.get("dataloader_num_workers", 0)))

        # Device
        set_arg(training_args, "device", cfg.get("device", "cpu"))

        return training_args
