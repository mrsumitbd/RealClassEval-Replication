from typing import Dict, Any, Optional, List, Union
import gc
import math
import os

try:
    import psutil  # type: ignore
except Exception:
    psutil = None  # type: ignore

try:
    import torch  # type: ignore
except Exception as e:  # pragma: no cover
    raise RuntimeError(
        "MemoryManager requires PyTorch to be installed.") from e


class MemoryManager:
    """Simple memory manager that leverages PyTorch's built-in memory optimizations."""

    def __init__(self):
        """Initialize the memory manager."""
        self._has_cuda: bool = torch.cuda.is_available()
        # type: ignore[attr-defined]
        self._has_mps: bool = hasattr(
            torch.backends, "mps") and torch.backends.mps.is_available()
        self._device: torch.device = torch.device(
            "cuda" if self._has_cuda else ("mps" if self._has_mps else "cpu"))
        # Pre-compute capabilities
        self._bf16_supported: bool = bool(getattr(
            torch.cuda, "is_bf16_supported", lambda: False)()) if self._has_cuda else False
        # TF32 support implied on Ampere+ and recent PyTorch
        self._tf32_supported: bool = False
        if self._has_cuda:
            try:
                major, _ = torch.cuda.get_device_capability()
                self._tf32_supported = major >= 8
            except Exception:
                self._tf32_supported = False

    def get_memory_info(self) -> Dict[str, Any]:
        """Get current memory usage information."""
        info: Dict[str, Any] = {
            "device": str(self._device),
            "cuda_available": self._has_cuda,
            "mps_available": self._has_mps,
        }

        # Python process memory (RSS/VMS)
        if psutil is not None:
            try:
                p = psutil.Process(os.getpid())
                with p.oneshot():
                    mem = p.memory_info()
                info["process_memory_mb"] = {
                    "rss_mb": int(mem.rss / (1024 * 1024)),
                    "vms_mb": int(mem.vms / (1024 * 1024)),
                }
            except Exception:
                info["process_memory_mb"] = None
        else:
            info["process_memory_mb"] = None

        # CPU available memory
        if psutil is not None:
            try:
                vm = psutil.virtual_memory()
                info["system_memory_mb"] = {
                    "total_mb": int(vm.total / (1024 * 1024)),
                    "available_mb": int(vm.available / (1024 * 1024)),
                    "percent": float(vm.percent),
                }
            except Exception:
                info["system_memory_mb"] = None
        else:
            info["system_memory_mb"] = None

        # CUDA memory per device
        if self._has_cuda:
            cuda_devices: List[Dict[str, Any]] = []
            try:
                for idx in range(torch.cuda.device_count()):
                    props = torch.cuda.get_device_properties(idx)
                    free_b, total_b = torch.cuda.mem_get_info(idx)
                    allocated_b = torch.cuda.memory_allocated(idx)
                    reserved_b = torch.cuda.memory_reserved(idx)
                    max_alloc_b = torch.cuda.max_memory_allocated(idx)
                    max_res_b = torch.cuda.max_memory_reserved(idx)
                    cuda_devices.append(
                        {
                            "device_id": idx,
                            "name": props.name,
                            "total_mb": int(total_b / (1024 * 1024)),
                            "free_mb": int(free_b / (1024 * 1024)),
                            "used_mb": int((total_b - free_b) / (1024 * 1024)),
                            "allocated_mb": int(allocated_b / (1024 * 1024)),
                            "reserved_mb": int(reserved_b / (1024 * 1024)),
                            "max_allocated_mb": int(max_alloc_b / (1024 * 1024)),
                            "max_reserved_mb": int(max_res_b / (1024 * 1024)),
                            "capability": f"{props.major}.{props.minor}",
                            "multi_processor_count": props.multi_processor_count,
                        }
                    )
            except Exception:
                cuda_devices = []
            info["cuda_devices"] = cuda_devices

        # MPS memory (best-effort)
        if self._has_mps:
            mps_info: Dict[str, Any] = {}
            try:
                # type: ignore[attr-defined]
                if hasattr(torch, "mps") and hasattr(torch.mps, "current_allocated_memory"):
                    mps_info["current_allocated_mb"] = int(
                        torch.mps.current_allocated_memory() / (1024 * 1024))  # type: ignore[attr-defined]
                # type: ignore[attr-defined]
                if hasattr(torch, "mps") and hasattr(torch.mps, "driver_allocated_memory"):
                    mps_info["driver_allocated_mb"] = int(
                        torch.mps.driver_allocated_memory() / (1024 * 1024))  # type: ignore[attr-defined]
            except Exception:
                pass
            info["mps"] = mps_info or None

        return info

    def cleanup_memory(self, force: bool = False) -> None:
        """Free up memory by garbage collection and emptying CUDA cache."""
        try:
            gc.collect()
        except Exception:
            pass

        # CUDA cleanup
        if self._has_cuda:
            try:
                torch.cuda.empty_cache()
            except Exception:
                pass
            try:
                if force:
                    # More aggressive cleanup
                    if hasattr(torch.cuda, "ipc_collect"):
                        torch.cuda.ipc_collect()  # type: ignore[attr-defined]
                    for idx in range(torch.cuda.device_count()):
                        torch.cuda.reset_peak_memory_stats(idx)
            except Exception:
                pass

        # MPS cleanup
        if self._has_mps:
            try:
                # type: ignore[attr-defined]
                if hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
                    torch.mps.empty_cache()  # type: ignore[attr-defined]
            except Exception:
                pass

    def get_optimal_training_config(self) -> Dict[str, Any]:
        """Get recommended configurations for model training based on hardware capabilities."""
        device = "cuda" if self._has_cuda else (
            "mps" if self._has_mps else "cpu")

        # Precision recommendation
        precision: str = "fp32"
        autocast_dtype: Optional[str] = None
        use_amp = False

        if device == "cuda":
            if self._bf16_supported:
                precision = "bf16"
                autocast_dtype = "bfloat16"
                use_amp = True
            else:
                precision = "fp16"
                autocast_dtype = "float16"
                use_amp = True
        elif device == "mps":
            # MPS mixed precision most commonly via float16 autocast
            precision = "fp16"
            autocast_dtype = "float16"
            use_amp = True
        else:
            precision = "fp32"
            autocast_dtype = None
            use_amp = False

        # Channels-last is primarily beneficial on CUDA for conv-heavy models
        channels_last = device == "cuda"

        # TF32 recommendation on Ampere+
        tf32 = bool(self._tf32_supported)

        # torch.compile availability (PyTorch 2.0+)
        can_compile = hasattr(torch, "compile")

        # Suggest a rough micro-batch size tier based on free VRAM
        suggested_micro_batch_size = None
        if device == "cuda":
            try:
                free_b, total_b = torch.cuda.mem_get_info()
                free_gb = free_b / (1024 ** 3)
                if free_gb >= 22:
                    suggested_micro_batch_size = 64
                elif free_gb >= 12:
                    suggested_micro_batch_size = 32
                elif free_gb >= 8:
                    suggested_micro_batch_size = 16
                elif free_gb >= 4:
                    suggested_micro_batch_size = 8
                else:
                    suggested_micro_batch_size = 4
            except Exception:
                suggested_micro_batch_size = None

        return {
            "device": device,
            "precision": precision,
            "use_amp": use_amp,
            "autocast_dtype": autocast_dtype,
            "channels_last": channels_last,
            "tf32": tf32,
            "can_compile": can_compile,
            "suggested_micro_batch_size": suggested_micro_batch_size,
        }

    def optimize_model_for_training(self, model):
        """Apply PyTorch's built-in memory optimizations for training."""
        # Move to device
        try:
            model = model.to(self._device)
        except Exception:
            pass

        # Channels-last for CUDA (beneficial for convolutional nets)
        if self._has_cuda:
            try:
                model = model.to(memory_format=torch.channels_last)
            except Exception:
                pass

        # Enable cudnn/cublas optimizations and TF32 where applicable
        try:
            if self._has_cuda:
                # type: ignore[attr-defined]
                torch.backends.cudnn.benchmark = True
                if self._tf32_supported:
                    # type: ignore[attr-defined]
                    torch.backends.cuda.matmul.allow_tf32 = True
                    # type: ignore[attr-defined]
                    torch.backends.cudnn.allow_tf32 = True
            # Set matmul precision for CPU/GPU
            if hasattr(torch, "set_float32_matmul_precision"):
                torch.set_float32_matmul_precision("high")
        except Exception:
            pass

        # Gradient checkpointing if supported by the model (commonly on HF models)
        try:
            if hasattr(model, "gradient_checkpointing_enable") and callable(getattr(model, "gradient_checkpointing_enable")):
                model.gradient_checkpointing_enable()
        except Exception:
            pass

        # torch.compile where available (PyTorch 2.0+)
        try:
            if hasattr(torch, "compile"):
                # Use a conservative mode for training memory usage
                # type: ignore[attr-defined]
                model = torch.compile(model, mode="reduce-overhead")
        except Exception:
            # If compile fails, keep the original model
            pass

        return model

    def optimize_training_args(self, training_args):
        """Configure training arguments for efficient memory usage."""
        cfg = self.get_optimal_training_config()

        def set_arg(obj: Any, key: str, value: Any) -> None:
            if isinstance(obj, dict):
                obj[key] = value
            else:
                if hasattr(obj, key):
                    setattr(obj, key, value)

        def get_arg(obj: Any, key: str, default: Any = None) -> Any:
            if isinstance(obj, dict):
                return obj.get(key, default)
            return getattr(obj, key, default)

        # Mixed precision flags (HF TrainingArguments-compatible)
        if cfg["precision"] == "bf16":
            set_arg(training_args, "bf16", True)
            set_arg(training_args, "fp16", False)
        elif cfg["precision"] == "fp16":
            set_arg(training_args, "bf16", False)
            set_arg(training_args, "fp16", True)
        else:
            set_arg(training_args, "bf16", False)
            set_arg(training_args, "fp16", False)

        # TF32 flag if present
        if get_arg(training_args, "tf32", None) is not None:
            set_arg(training_args, "tf32", bool(cfg["tf32"]))

        # Pin memory and workers (when using DataLoader)
        if get_arg(training_args, "dataloader_pin_memory", None) is not None:
            set_arg(training_args, "dataloader_pin_memory",
                    self._has_cuda or self._has_mps)
        if get_arg(training_args, "dataloader_num_workers", None) is not None:
            cpu_count = os.cpu_count() or 1
            # Leave some headroom
            workers = max(0, min(8, cpu_count - 1))
            set_arg(training_args, "dataloader_num_workers", workers)

        # Gradient checkpointing if supported by the args
        if get_arg(training_args, "gradient_checkpointing", None) is not None:
            set_arg(training_args, "gradient_checkpointing", True)

        # torch.compile flag if available in args
        if get_arg(training_args, "torch_compile", None) is not None:
            set_arg(training_args, "torch_compile", bool(
                cfg["can_compile"] and (self._has_cuda or self._has_mps)))

        # Suggested micro-batch size if per_device_train_batch_size is present and not explicitly set
        if get_arg(training_args, "per_device_train_batch_size", None) is not None and cfg["suggested_micro_batch_size"] is not None:
            # Only set if batch size not already specified by user (e.g., is None or 0)
            if not get_arg(training_args, "per_device_train_batch_size"):
                set_arg(training_args, "per_device_train_batch_size",
                        int(cfg["suggested_micro_batch_size"]))

        # Prefer fused optimizer on CUDA if available in args
        if get_arg(training_args, "optim", None) is not None and self._has_cuda:
            # Set to torch fused variant if not set
            if not get_arg(training_args, "optim"):
                set_arg(training_args, "optim", "adamw_torch_fused")

        return training_args
