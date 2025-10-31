from typing import Dict, Any, Optional
import gc
import warnings

try:
    import torch
except Exception as e:  # pragma: no cover
    torch = None  # type: ignore

try:
    import psutil
except Exception:
    psutil = None  # type: ignore


class MemoryManager:
    """Simple memory manager that leverages PyTorch's built-in memory optimizations."""

    def __init__(self):
        """Initialize the memory manager."""
        self._has_torch = torch is not None
        self._has_psutil = psutil is not None

    def get_memory_info(self) -> Dict[str, Any]:
        """Get current memory usage information."""
        info: Dict[str, Any] = {"cpu": {}, "cuda": [], "mps": {}}

        # CPU memory via psutil
        if self._has_psutil:
            vmem = psutil.virtual_memory()  # type: ignore[attr-defined]
            info["cpu"] = {
                "total_bytes": int(vmem.total),
                "available_bytes": int(vmem.available),
                "used_bytes": int(vmem.used),
                "percent": float(vmem.percent),
            }
        else:
            info["cpu"] = {
                "total_bytes": None,
                "available_bytes": None,
                "used_bytes": None,
                "percent": None,
            }

        if not self._has_torch:
            return info

        # CUDA memory (per device)
        if torch.cuda.is_available():  # type: ignore[union-attr]
            try:
                # type: ignore[union-attr]
                device_count = torch.cuda.device_count()
            except Exception:
                device_count = 0

            for i in range(device_count):
                try:
                    props = torch.cuda.get_device_properties(
                        i)  # type: ignore[union-attr]
                    name = props.name
                    total_prop = int(getattr(props, "total_memory", 0))
                except Exception:
                    name = f"cuda:{i}"
                    total_prop = 0

                free_bytes = None
                total_bytes = None
                try:
                    with torch.cuda.device(i):  # type: ignore[union-attr]
                        free_bytes, total_bytes = torch.cuda.mem_get_info(
                            i)  # type: ignore[arg-type, union-attr]
                except Exception:
                    # Fallback to device properties for total if mem_get_info isn't available
                    total_bytes = total_prop if total_prop > 0 else None

                try:
                    # type: ignore[union-attr]
                    allocated = int(torch.cuda.memory_allocated(i))
                    # type: ignore[union-attr]
                    reserved = int(torch.cuda.memory_reserved(i))
                    # type: ignore[union-attr]
                    max_allocated = int(torch.cuda.max_memory_allocated(i))
                    # type: ignore[union-attr]
                    max_reserved = int(torch.cuda.max_memory_reserved(i))
                except Exception:
                    # type: ignore[assignment]
                    allocated = reserved = max_allocated = max_reserved = None

                info["cuda"].append(
                    {
                        "device_index": i,
                        "device_name": name,
                        "total_bytes": int(total_bytes) if total_bytes is not None else None,
                        "free_bytes": int(free_bytes) if free_bytes is not None else None,
                        "allocated_bytes": allocated,
                        "reserved_bytes": reserved,
                        "max_allocated_bytes": max_allocated,
                        "max_reserved_bytes": max_reserved,
                    }
                )

        # Apple MPS memory
        try:
            # type: ignore[union-attr]
            mps_available = hasattr(
                torch, "backends") and torch.backends.mps.is_available()
        except Exception:
            mps_available = False

        if mps_available:
            mps_info: Dict[str, Optional[int]] = {}
            try:
                # Available in recent PyTorch
                # type: ignore[attr-defined]
                current_alloc = getattr(
                    torch.mps, "current_allocated_memory", None)
                # type: ignore[attr-defined]
                driver_alloc = getattr(
                    torch.mps, "driver_allocated_memory", None)
                if callable(current_alloc):
                    mps_info["current_allocated_bytes"] = int(current_alloc())
                else:
                    mps_info["current_allocated_bytes"] = None
                if callable(driver_alloc):
                    mps_info["driver_allocated_bytes"] = int(driver_alloc())
                else:
                    mps_info["driver_allocated_bytes"] = None
            except Exception:
                mps_info["current_allocated_bytes"] = None
                mps_info["driver_allocated_bytes"] = None
            info["mps"] = mps_info

        return info

    def cleanup_memory(self, force: bool = False) -> None:
        """Free up memory by garbage collection and emptying CUDA cache."""
        # Python GC
        try:
            gc.collect()
        except Exception:
            pass

        if not self._has_torch:
            return

        # CUDA cleanup
        if torch.cuda.is_available():  # type: ignore[union-attr]
            try:
                torch.cuda.empty_cache()  # type: ignore[union-attr]
                torch.cuda.ipc_collect()  # type: ignore[union-attr]
                if force:
                    # Best-effort deeper cleanup
                    # type: ignore[union-attr]
                    for i in range(torch.cuda.device_count()):
                        try:
                            torch.cuda.reset_peak_memory_stats(
                                i)  # type: ignore[union-attr]
                            # type: ignore[union-attr]
                            with torch.cuda.device(i):
                                # type: ignore[union-attr]
                                torch.cuda.empty_cache()
                        except Exception:
                            continue
                    try:
                        torch.cuda.synchronize()  # type: ignore[union-attr]
                    except Exception:
                        pass
            except Exception:
                pass

        # MPS cleanup (if available)
        try:
            # type: ignore[union-attr]
            if hasattr(torch, "backends") and torch.backends.mps.is_available():
                # type: ignore[attr-defined]
                empty_cache = getattr(torch.mps, "empty_cache", None)
                if callable(empty_cache):
                    empty_cache()
        except Exception:
            pass

    def get_optimal_training_config(self) -> Dict[str, Any]:
        """Get recommended configurations for model training based on hardware capabilities."""
        device = "cpu"
        cuda = False
        mps = False

        # type: ignore[union-attr]
        if self._has_torch and torch.cuda.is_available():
            device = "cuda"
            cuda = True
        else:
            try:
                # type: ignore[union-attr]
                if self._has_torch and hasattr(torch, "backends") and torch.backends.mps.is_available():
                    device = "mps"
                    mps = True
            except Exception:
                pass

        mixed_precision = "no"
        tf32 = False
        batch_size = 1
        grad_ckpt = False
        pin_memory = False
        torch_compile_flag = False

        # Torch compile availability
        try:
            # type: ignore[union-attr]
            torch_compile_flag = hasattr(torch, "compile")
        except Exception:
            torch_compile_flag = False

        if cuda:
            try:
                props = torch.cuda.get_device_properties(
                    0)  # type: ignore[union-attr]
                total_mem = int(getattr(props, "total_memory", 0))
                vram_gb = total_mem / (1024 ** 3) if total_mem else 0.0
            except Exception:
                total_mem = 0
                vram_gb = 0.0

            # Mixed precision preference: bf16 if supported, else fp16
            try:
                # type: ignore[union-attr]
                bf16_supported = bool(
                    getattr(torch.cuda, "is_bf16_supported", lambda: False)())
            except Exception:
                bf16_supported = False
            mixed_precision = "bf16" if bf16_supported else "fp16"

            # Heuristic for batch size
            if vram_gb >= 40:
                batch_size = 32
            elif vram_gb >= 24:
                batch_size = 16
            elif vram_gb >= 16:
                batch_size = 8
            elif vram_gb >= 12:
                batch_size = 4
            elif vram_gb >= 8:
                batch_size = 2
            else:
                batch_size = 1

            # Gradient checkpointing if VRAM is modest
            grad_ckpt = vram_gb < 24

            # Pinned memory only matters for CUDA
            pin_memory = True

            # Enable TF32 on Ampere or newer (compute capability >= 8.0)
            try:
                major_cc, _ = torch.cuda.get_device_capability(
                    0)  # type: ignore[union-attr]
                tf32 = major_cc >= 8
            except Exception:
                tf32 = False

        elif mps:
            # MPS supports fp16 autocast; use fp16
            mixed_precision = "fp16"
            # Heuristic using system RAM
            sys_ram_gb = 0.0
            if self._has_psutil:
                try:
                    # type: ignore[attr-defined]
                    sys_ram_gb = float(
                        psutil.virtual_memory().total) / (1024 ** 3)
                except Exception:
                    sys_ram_gb = 0.0
            batch_size = 2 if sys_ram_gb >= 32 else 1
            grad_ckpt = True
            pin_memory = False  # pin_memory is CUDA-specific

        else:
            # CPU fallbacks
            mixed_precision = "no"
            batch_size = 1
            grad_ckpt = True
            pin_memory = False

        return {
            "device": device,
            "mixed_precision": mixed_precision,  # 'bf16' | 'fp16' | 'no'
            "per_device_train_batch_size": batch_size,
            "gradient_checkpointing": grad_ckpt,
            "dataloader_pin_memory": pin_memory,
            "torch_compile": torch_compile_flag,
            "tf32": tf32,
        }

    def optimize_model_for_training(self, model):
        """Apply PyTorch's built-in memory optimizations for training."""
        if not self._has_torch or model is None:
            return model

        # Enable gradient checkpointing if model supports it and it is recommended
        try:
            cfg = self.get_optimal_training_config()
        except Exception:
            cfg = {
                "gradient_checkpointing": False,
                # type: ignore[union-attr]
                "device": "cuda" if (self._has_torch and torch.cuda.is_available()) else "cpu",
            }

        if cfg.get("gradient_checkpointing", False):
            try:
                if hasattr(model, "gradient_checkpointing_enable") and callable(getattr(model, "gradient_checkpointing_enable")):
                    # type: ignore[attr-defined]
                    model.gradient_checkpointing_enable()
            except Exception:
                pass

        # Channels-last memory format can reduce memory for conv nets on CUDA
        try:
            if cfg.get("device") == "cuda":
                # type: ignore[union-attr]
                model = model.to(memory_format=torch.channels_last)
        except Exception:
            pass

        # Set matmul precision for speed/memory trade-off
        try:
            # type: ignore[union-attr]
            set_prec = getattr(torch, "set_float32_matmul_precision", None)
            if callable(set_prec):
                # "high" enables TF32 on supported GPUs; "medium" is safer if precision issues occur
                set_prec("high")
        except Exception:
            pass

        # cudnn benchmark may choose better kernels (potentially improved memory behavior)
        try:
            if hasattr(torch.backends, "cudnn"):  # type: ignore[union-attr]
                # type: ignore[union-attr]
                torch.backends.cudnn.benchmark = True
        except Exception:
            pass

        # Optionally compile model if available (may reduce overhead and memory fragmentation)
        try:
            # type: ignore[union-attr]
            if hasattr(torch, "compile") and callable(getattr(torch, "compile")):
                # Use a conservative mode focused on reducing overhead
                # type: ignore[union-attr]
                model = torch.compile(model, mode="reduce-overhead")
        except Exception:
            # If compilation fails for any reason, continue with the original model
            pass

        return model

    def optimize_training_args(self, training_args):
        """Configure training arguments for efficient memory usage."""
        if training_args is None:
            return None

        cfg = self.get_optimal_training_config()

        def _set(obj, key: str, value: Any):
            try:
                if isinstance(obj, dict):
                    obj[key] = value
                elif hasattr(obj, key):
                    setattr(obj, key, value)
            except Exception:
                pass

        # Mixed precision flags (HF-style names)
        mp = cfg.get("mixed_precision", "no")
        _set(training_args, "fp16", mp == "fp16")
        _set(training_args, "bf16", mp == "bf16")

        # Gradient checkpointing
        _set(training_args, "gradient_checkpointing", bool(
            cfg.get("gradient_checkpointing", False)))

        # Batch size
        _set(training_args, "per_device_train_batch_size",
             int(cfg.get("per_device_train_batch_size", 1)))

        # Pin memory (only relevant for CUDA)
        _set(training_args, "dataloader_pin_memory", bool(
            cfg.get("dataloader_pin_memory", False)))

        # Torch compile
        _set(training_args, "torch_compile", bool(
            cfg.get("torch_compile", False)))
        if bool(cfg.get("torch_compile", False)):
            # Backend selection; 'inductor' is default on most platforms
            _set(training_args, "torch_compile_backend", "inductor")

        # TF32
        _set(training_args, "tf32", bool(cfg.get("tf32", False)))

        # Set global torch flags to match args when possible
        if self._has_torch:
            try:
                # type: ignore[union-attr]
                if bool(cfg.get("tf32", False)) and hasattr(torch.backends, "cuda") and hasattr(torch.backends.cuda, "matmul"):
                    # type: ignore[union-attr]
                    torch.backends.cuda.matmul.allow_tf32 = True
                # type: ignore[union-attr]
                if hasattr(torch.backends, "cudnn"):
                    torch.backends.cudnn.allow_tf32 = bool(
                        cfg.get("tf32", False))  # type: ignore[union-attr]
            except Exception:
                pass

        return training_args
