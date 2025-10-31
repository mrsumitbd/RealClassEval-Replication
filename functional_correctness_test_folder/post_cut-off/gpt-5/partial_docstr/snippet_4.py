from typing import Any, Dict, Optional, Union
import gc
import os

try:
    import psutil  # type: ignore
except Exception:
    psutil = None

try:
    import torch  # type: ignore
    import torch.nn as nn  # type: ignore
except Exception:
    torch = None
    nn = None


class MemoryManager:
    def __init__(self):
        self._has_torch = torch is not None
        self._has_psutil = psutil is not None

    def get_memory_info(self) -> Dict[str, Any]:
        info: Dict[str, Any] = {}

        # System memory
        sys_mem = {}
        if self._has_psutil:
            vm = psutil.virtual_memory()
            sm = psutil.swap_memory()
            sys_mem = {
                "total": vm.total,
                "available": vm.available,
                "used": vm.used,
                "free": vm.free,
                "percent": vm.percent,
                "swap_total": sm.total,
                "swap_used": sm.used,
                "swap_free": sm.free,
                "swap_percent": sm.percent,
            }
        else:
            try:
                import shutil

                total, used, free = shutil.disk_usage("/")
            except Exception:
                total = used = free = 0
            sys_mem = {
                "total": None,
                "available": None,
                "used": None,
                "free": None,
                "percent": None,
                "swap_total": None,
                "swap_used": None,
                "swap_free": None,
                "swap_percent": None,
                "disk_total": total,
                "disk_used": used,
                "disk_free": free,
            }
        info["system"] = sys_mem

        # PyTorch / CUDA / MPS memory
        torch_mem: Dict[str, Any] = {"backend": None}
        if self._has_torch:
            torch_mem["backend"] = "cpu"
            # CUDA devices
            if torch.cuda.is_available():
                devices = []
                num = torch.cuda.device_count()
                for idx in range(num):
                    try:
                        props = torch.cuda.get_device_properties(idx)
                        name = props.name
                        total = props.total_memory
                    except Exception:
                        name = f"cuda:{idx}"
                        total = None

                    stat: Dict[str, Any] = {"index": idx, "name": name}
                    try:
                        # Newer API gives free/total directly from driver
                        free, total2 = torch.cuda.mem_get_info(idx)
                        stat.update(
                            {"total": total2, "free": free, "used": total2 - free})
                    except Exception:
                        stat.update(
                            {"total": total, "free": None, "used": None})

                    try:
                        reserved = torch.cuda.memory_reserved(idx)
                        allocated = torch.cuda.memory_allocated(idx)
                        max_reserved = torch.cuda.max_memory_reserved(idx)
                        max_allocated = torch.cuda.max_memory_allocated(idx)
                        stat.update(
                            {
                                "reserved": reserved,
                                "allocated": allocated,
                                "max_reserved": max_reserved,
                                "max_allocated": max_allocated,
                            }
                        )
                    except Exception:
                        pass
                    devices.append(stat)
                torch_mem["cuda"] = {"device_count": num, "devices": devices}
                torch_mem["backend"] = "cuda"

            # MPS (Apple Silicon)
            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                mps_info = {}
                try:
                    # No standard MPS memory API; expose availability
                    mps_info["available"] = True
                except Exception:
                    mps_info["available"] = True
                torch_mem["mps"] = mps_info
                if not torch.cuda.is_available():
                    torch_mem["backend"] = "mps"
        info["torch"] = torch_mem

        return info

    def cleanup_memory(self, force: bool = False) -> None:
        # Python garbage
        gc.collect()

        # PyTorch cleanup
        if self._has_torch:
            try:
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    torch.cuda.ipc_collect()
                    if force:
                        # Reset peak stats to help tracking subsequent usage
                        try:
                            for idx in range(torch.cuda.device_count()):
                                torch.cuda.reset_peak_memory_stats(idx)
                        except Exception:
                            torch.cuda.reset_peak_memory_stats()
                # MPS cache clean (PyTorch >= 2.0)
                if hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
                    torch.mps.empty_cache()
            except Exception:
                pass

    def get_optimal_training_config(self) -> Dict[str, Any]:
        cfg: Dict[str, Any] = {}

        # Determine device and precision
        device = "cpu"
        use_bf16 = False
        use_fp16 = False
        can_compile = False
        if self._has_torch:
            device = "cuda" if torch.cuda.is_available() else ("mps" if hasattr(
                torch.backends, "mps") and torch.backends.mps.is_available() else "cpu")
            can_compile = hasattr(torch, "compile")

            if device == "cuda":
                try:
                    if hasattr(torch.cuda, "is_bf16_supported") and torch.cuda.is_bf16_supported():
                        use_bf16 = True
                    else:
                        major, minor = torch.cuda.get_device_capability()
                        use_fp16 = major >= 7
                except Exception:
                    use_fp16 = True
            elif device == "mps":
                use_bf16 = False
                use_fp16 = False

        # Heuristic batch size by VRAM
        per_device_bs = 8
        if self._has_torch and device == "cuda":
            try:
                total_mem = torch.cuda.get_device_properties(0).total_memory
                # Simple heuristic
                if total_mem <= 4 * (1024**3):
                    per_device_bs = 2
                elif total_mem <= 8 * (1024**3):
                    per_device_bs = 4
                elif total_mem <= 16 * (1024**3):
                    per_device_bs = 8
                else:
                    per_device_bs = 16
            except Exception:
                pass
        elif self._has_torch and device == "mps":
            per_device_bs = 4

        # Workers heuristic
        num_workers = 0
        try:
            cpu_count = os.cpu_count() or 2
            num_workers = max(0, min(8, cpu_count - 1))
        except Exception:
            num_workers = 0

        cfg.update(
            {
                "device": device,
                "per_device_train_batch_size": per_device_bs,
                "per_device_eval_batch_size": max(1, per_device_bs // 2),
                "gradient_accumulation_steps": 1,
                "gradient_checkpointing": True,
                "bf16": use_bf16,
                "fp16": (use_fp16 and not use_bf16),
                "torch_compile": can_compile,
                "dataloader_num_workers": num_workers,
                "pin_memory": device == "cuda",
            }
        )
        return cfg

    def optimize_model_for_training(self, model):
        if not self._has_torch:
            return model

        # cuDNN optimizations for convolution workloads
        try:
            if torch.cuda.is_available() and hasattr(torch.backends, "cudnn"):
                torch.backends.cudnn.benchmark = True
                torch.backends.cudnn.enabled = True
        except Exception:
            pass

        # Matmul precision improvements (PyTorch 2.0+)
        try:
            if hasattr(torch, "set_float32_matmul_precision"):
                torch.set_float32_matmul_precision("high")
        except Exception:
            pass

        # Enable gradient checkpointing if supported
        try:
            if hasattr(model, "gradient_checkpointing_enable"):
                model.gradient_checkpointing_enable()
            elif hasattr(model, "enable_gradient_checkpointing"):
                model.enable_gradient_checkpointing()
        except Exception:
            pass

        # Channels-last memory format for Conv2d models
        try:
            use_channels_last = False
            if nn is not None:
                for m in model.modules():
                    if isinstance(m, nn.Conv2d):
                        use_channels_last = True
                        break
            if use_channels_last:
                model = model.to(memory_format=torch.channels_last)
        except Exception:
            pass

        return model

    def optimize_training_args(self, training_args: Union[Dict[str, Any], Any]):
        def set_arg(obj, key: str, value: Any):
            if isinstance(obj, dict):
                obj[key] = value
            else:
                if hasattr(obj, key):
                    try:
                        setattr(obj, key, value)
                    except Exception:
                        pass

        def get_arg(obj, key: str, default: Any = None) -> Any:
            if isinstance(obj, dict):
                return obj.get(key, default)
            return getattr(obj, key, default)

        cfg = self.get_optimal_training_config()

        # Batch sizes
        current_bs = get_arg(
            training_args, "per_device_train_batch_size", None)
        if not current_bs:
            set_arg(training_args, "per_device_train_batch_size",
                    cfg["per_device_train_batch_size"])
        current_bs_eval = get_arg(
            training_args, "per_device_eval_batch_size", None)
        if not current_bs_eval:
            set_arg(training_args, "per_device_eval_batch_size",
                    cfg["per_device_eval_batch_size"])

        # Precision
        if get_arg(training_args, "bf16", None) is None:
            set_arg(training_args, "bf16", cfg["bf16"])
        if get_arg(training_args, "fp16", None) is None:
            set_arg(training_args, "fp16", cfg["fp16"])

        # Gradient checkpointing
        if get_arg(training_args, "gradient_checkpointing", None) is None:
            set_arg(training_args, "gradient_checkpointing",
                    cfg["gradient_checkpointing"])

        # Torch compile
        if get_arg(training_args, "torch_compile", None) is None:
            set_arg(training_args, "torch_compile", cfg["torch_compile"])

        # Dataloader workers
        if get_arg(training_args, "dataloader_num_workers", None) is None:
            set_arg(training_args, "dataloader_num_workers",
                    cfg["dataloader_num_workers"])

        # Pin memory (HF TrainingArguments uses this field in DataLoader)
        if get_arg(training_args, "dataloader_pin_memory", None) is None:
            set_arg(training_args, "dataloader_pin_memory", cfg["pin_memory"])

        # Gradient accumulation default
        if get_arg(training_args, "gradient_accumulation_steps", None) is None:
            set_arg(training_args, "gradient_accumulation_steps",
                    cfg["gradient_accumulation_steps"])

        return training_args
