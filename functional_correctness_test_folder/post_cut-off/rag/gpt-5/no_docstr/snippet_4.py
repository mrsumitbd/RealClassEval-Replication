from typing import Dict, Any, Optional, Union
import gc
import math
import warnings

try:
    import torch
except Exception:  # pragma: no cover
    torch = None  # type: ignore[assignment]

try:
    import psutil
except Exception:  # pragma: no cover
    psutil = None  # type: ignore[assignment]


class MemoryManager:
    """Simple memory manager that leverages PyTorch's built-in memory optimizations."""

    def __init__(self):
        """Initialize the memory manager."""
        self.torch = torch
        self.psutil = psutil
        self.cuda_available = bool(
            self.torch and self.torch.cuda.is_available())
        self.mps_available = bool(
            self.torch and hasattr(self.torch, "backends") and getattr(
                self.torch.backends, "mps", None)
            and self.torch.backends.mps.is_available()
        )
        self.device_type = self._get_device_type()

    def _get_device_type(self) -> str:
        if self.cuda_available:
            return "cuda"
        if self.mps_available:
            return "mps"
        return "cpu"

    def _bytes_to_gib(self, b: Optional[int]) -> Optional[float]:
        if b is None:
            return None
        return round(b / (1024 ** 3), 3)

    def get_memory_info(self) -> Dict[str, Any]:
        """Get current memory usage information."""
        info: Dict[str, Any] = {
            "device": self.device_type, "cpu": {}, "cuda": [], "mps": {}}

        # CPU memory (system + process)
        if self.psutil:
            try:
                vm = self.psutil.virtual_memory()
                info["cpu"] = {
                    "total_bytes": int(vm.total),
                    "available_bytes": int(vm.available),
                    "used_bytes": int(vm.used),
                    "percent": float(vm.percent),
                    "total_gib": self._bytes_to_gib(int(vm.total)),
                    "available_gib": self._bytes_to_gib(int(vm.available)),
                    "used_gib": self._bytes_to_gib(int(vm.used)),
                }
                try:
                    proc = self.psutil.Process()
                    rss = int(proc.memory_info().rss)
                    info["cpu"]["process_rss_bytes"] = rss
                    info["cpu"]["process_rss_gib"] = self._bytes_to_gib(rss)
                except Exception:
                    pass
            except Exception:
                pass

        # CUDA GPUs
        if self.cuda_available and self.torch:
            try:
                num = self.torch.cuda.device_count()
                for idx in range(num):
                    try:
                        props = self.torch.cuda.get_device_properties(idx)
                        name = props.name
                        total = int(props.total_memory)
                    except Exception:
                        name = f"cuda:{idx}"
                        total = None  # type: ignore[assignment]
                    allocated = None
                    reserved = None
                    max_allocated = None
                    max_reserved = None
                    free_bytes = None
                    total_bytes = total
                    try:
                        allocated = int(self.torch.cuda.memory_allocated(idx))
                        reserved = int(self.torch.cuda.memory_reserved(idx))
                    except Exception:
                        pass
                    try:
                        max_allocated = int(
                            self.torch.cuda.max_memory_allocated(idx))
                        max_reserved = int(
                            self.torch.cuda.max_memory_reserved(idx))
                    except Exception:
                        pass
                    # mem_get_info may support per-device
                    try:
                        free_bytes, total_bytes = self.torch.cuda.mem_get_info(
                            idx)  # type: ignore[arg-type]
                        if total is None:
                            total = int(total_bytes)
                    except Exception:
                        pass

                    info["cuda"].append(
                        {
                            "index": idx,
                            "name": name,
                            "total_bytes": int(total) if total is not None else None,
                            "total_gib": self._bytes_to_gib(total) if total is not None else None,
                            "free_bytes": int(free_bytes) if free_bytes is not None else None,
                            "free_gib": self._bytes_to_gib(free_bytes) if free_bytes is not None else None,
                            "allocated_bytes": int(allocated) if allocated is not None else None,
                            "allocated_gib": self._bytes_to_gib(allocated) if allocated is not None else None,
                            "reserved_bytes": int(reserved) if reserved is not None else None,
                            "reserved_gib": self._bytes_to_gib(reserved) if reserved is not None else None,
                            "max_allocated_bytes": int(max_allocated) if max_allocated is not None else None,
                            "max_allocated_gib": self._bytes_to_gib(max_allocated) if max_allocated is not None else None,
                            "max_reserved_bytes": int(max_reserved) if max_reserved is not None else None,
                            "max_reserved_gib": self._bytes_to_gib(max_reserved) if max_reserved is not None else None,
                            "compute_capability": (
                                (getattr(props, "major", None), getattr(
                                    props, "minor", None)) if "props" in locals() else None
                            ),
                        }
                    )
            except Exception:
                pass

        # Apple MPS
        if self.mps_available and self.torch:
            try:
                mps_alloc = None
                mps_reserved = None
                driver_alloc = None
                if hasattr(self.torch, "mps"):
                    try:
                        # type: ignore[attr-defined]
                        mps_alloc = int(
                            self.torch.mps.current_allocated_memory())
                    except Exception:
                        pass
                    try:
                        # type: ignore[attr-defined]
                        mps_reserved = int(
                            self.torch.mps.current_reserved_memory())
                    except Exception:
                        pass
                    try:
                        # type: ignore[attr-defined]
                        driver_alloc = int(
                            self.torch.mps.driver_allocated_memory())
                    except Exception:
                        pass
                info["mps"] = {
                    "allocated_bytes": mps_alloc,
                    "allocated_gib": self._bytes_to_gib(mps_alloc) if mps_alloc is not None else None,
                    "reserved_bytes": mps_reserved,
                    "reserved_gib": self._bytes_to_gib(mps_reserved) if mps_reserved is not None else None,
                    "driver_allocated_bytes": driver_alloc,
                    "driver_allocated_gib": self._bytes_to_gib(driver_alloc) if driver_alloc is not None else None,
                }
            except Exception:
                pass

        return info

    def cleanup_memory(self, force: bool = False) -> None:
        """Free up memory by garbage collection and emptying CUDA cache."""
        # Python GC
        try:
            gc.collect()
        except Exception:
            pass

        # CUDA cleanup
        if self.cuda_available and self.torch:
            try:
                num = self.torch.cuda.device_count()
                for idx in range(num):
                    try:
                        self.torch.cuda.empty_cache()
                    except Exception:
                        pass
                    try:
                        if hasattr(self.torch.cuda, "ipc_collect"):
                            # type: ignore[attr-defined]
                            self.torch.cuda.ipc_collect()
                    except Exception:
                        pass
                    if force:
                        try:
                            self.torch.cuda.reset_peak_memory_stats(idx)
                        except Exception:
                            pass
                # Optional sync to ensure dealloc happens promptly
                try:
                    self.torch.cuda.synchronize()
                except Exception:
                    pass
            except Exception:
                pass

        # MPS cleanup
        if self.mps_available and self.torch:
            try:
                if hasattr(self.torch, "mps") and hasattr(self.torch.mps, "empty_cache"):
                    self.torch.mps.empty_cache()  # type: ignore[attr-defined]
            except Exception:
                pass

    def _detect_mixed_precision(self) -> str:
        if not self.torch:
            return "no"
        if self.cuda_available:
            try:
                # Prefer bf16 on Ampere (8.x) and newer
                majors = []
                for i in range(self.torch.cuda.device_count()):
                    props = self.torch.cuda.get_device_properties(i)
                    majors.append(getattr(props, "major", 0))
                if majors and min(majors) >= 8:
                    return "bf16"
            except Exception:
                pass
            return "fp16"
        if self.mps_available:
            # FP16 generally works well on MPS
            return "fp16"
        # CPU: conservative default
        return "no"

    def _estimate_recommended_batch_size(self, mem_info: Dict[str, Any]) -> int:
        if self.device_type == "cuda" and mem_info.get("cuda"):
            # Use the most constrained GPU
            free_gib_values = []
            for g in mem_info["cuda"]:
                fg = g.get("free_gib")
                # fallback to total - reserved if free not available
                if fg is None and g.get("total_gib") is not None and g.get("reserved_gib") is not None:
                    try:
                        fg = max(0.0, float(
                            g["total_gib"]) - float(g["reserved_gib"]))
                    except Exception:
                        fg = None
                if isinstance(fg, (int, float)):
                    free_gib_values.append(float(fg))
            free_gib = min(free_gib_values) if free_gib_values else 0.0
            # Heuristic mapping
            if free_gib < 3.5:
                return 1
            if free_gib < 7.5:
                return 2
            if free_gib < 12:
                return 4
            if free_gib < 24:
                return 8
            return 16
        # CPU/MPS based on available system RAM
        avail_gib = None
        cpu = mem_info.get("cpu") or {}
        if "available_gib" in cpu and isinstance(cpu["available_gib"], (int, float)):
            avail_gib = float(cpu["available_gib"])
        if avail_gib is None:
            return 4
        if avail_gib < 8:
            return 4
        if avail_gib < 16:
            return 8
        return 16

    def get_optimal_training_config(self) -> Dict[str, Any]:
        """Get recommended configurations for model training based on hardware capabilities."""
        mp = self._detect_mixed_precision()
        mem_info = self.get_memory_info()
        batch_size = self._estimate_recommended_batch_size(mem_info)

        tf32 = False
        if self.torch and self.cuda_available:
            # Enable TF32 when training on CUDA to improve throughput without large accuracy loss
            tf32 = True

        can_compile = bool(self.torch and hasattr(self.torch, "compile"))
        compile_mode = "max-autotune" if can_compile else None

        # Optimizer recommendation (safe default)
        optim = "adamw_torch"

        return {
            "device": self.device_type,
            "mixed_precision": mp,  # "bf16" | "fp16" | "no"
            "gradient_checkpointing": True,
            "tf32": tf32,
            "torch_compile": can_compile,
            "compile_mode": compile_mode,
            "recommended_per_device_train_batch_size": batch_size,
            "optimizer": optim,
        }

    def optimize_model_for_training(self, model):
        """Apply PyTorch's built-in memory optimizations for training."""
        if not self.torch:
            return model

        # Gradient checkpointing when supported
        try:
            if hasattr(model, "gradient_checkpointing_enable"):
                model.gradient_checkpointing_enable()
        except Exception:
            pass

        # TF32 toggles for CUDA
        if self.cuda_available:
            try:
                # type: ignore[attr-defined]
                self.torch.backends.cuda.matmul.allow_tf32 = True
            except Exception:
                pass
            try:
                # type: ignore[attr-defined]
                self.torch.backends.cudnn.allow_tf32 = True
            except Exception:
                pass

        # Matmul precision for better perf/memory trade-off on CPU/CUDA
        try:
            if hasattr(self.torch, "set_float32_matmul_precision"):
                self.torch.set_float32_matmul_precision(
                    "medium")  # type: ignore[attr-defined]
        except Exception:
            pass

        # cudnn autotune for convolutional models
        try:
            if hasattr(self.torch.backends, "cudnn"):
                # type: ignore[attr-defined]
                self.torch.backends.cudnn.benchmark = True
        except Exception:
            pass

        # Optional torch.compile in reduce-overhead or max-autotune mode
        try:
            if hasattr(self.torch, "compile"):
                # Use a conservative mode that tends to be robust
                # type: ignore[attr-defined]
                compiled = self.torch.compile(
                    model, mode="reduce-overhead", fullgraph=False)
                if compiled is not None:
                    model = compiled
        except Exception:
            # Fallback silently on older PyTorch or compilation failures
            pass

        return model

    def _set_arg(self, obj: Union[Dict[str, Any], Any], key: str, value: Any) -> None:
        if isinstance(obj, dict):
            obj[key] = value
        else:
            try:
                setattr(obj, key, value)
            except Exception:
                pass

    def _get_arg(self, obj: Union[Dict[str, Any], Any], key: str, default: Any = None) -> Any:
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    def optimize_training_args(self, training_args):
        """Configure training arguments for efficient memory usage."""
        if training_args is None:
            return training_args

        cfg = self.get_optimal_training_config()

        # Mixed precision flags (HF TrainingArguments use booleans for bf16/fp16)
        mp = cfg["mixed_precision"]
        if mp == "bf16":
            self._set_arg(training_args, "bf16", True)
            self._set_arg(training_args, "fp16", False)
        elif mp == "fp16":
            self._set_arg(training_args, "fp16", True)
            self._set_arg(training_args, "bf16", False)
        else:
            self._set_arg(training_args, "bf16", False)
            self._set_arg(training_args, "fp16", False)

        # Gradient checkpointing
        if self._get_arg(training_args, "gradient_checkpointing", None) is None:
            self._set_arg(training_args, "gradient_checkpointing",
                          cfg["gradient_checkpointing"])

        # TF32
        if self._get_arg(training_args, "tf32", None) is None:
            self._set_arg(training_args, "tf32", cfg["tf32"])

        # Optimizer
        if self._get_arg(training_args, "optim", None) is None:
            self._set_arg(training_args, "optim", cfg["optimizer"])

        # Torch compile flag for HF
        if self._get_arg(training_args, "torch_compile", None) is None:
            self._set_arg(training_args, "torch_compile", cfg["torch_compile"])
        # Optional compile mode if supported by downstream args
        if cfg["compile_mode"] and self._get_arg(training_args, "torch_compile_backend", None) is None:
            self._set_arg(training_args, "torch_compile_backend",
                          cfg["compile_mode"])

        # Per-device batch size recommendation if not explicitly set
        bsz = self._get_arg(training_args, "per_device_train_batch_size", None)
        if bsz in (None, 0):
            self._set_arg(training_args, "per_device_train_batch_size", int(
                cfg["recommended_per_device_train_batch_size"]))

        # Conservative defaults for memory efficiency
        if self._get_arg(training_args, "gradient_accumulation_steps", None) is None:
            self._set_arg(training_args, "gradient_accumulation_steps", 1)
        if self._get_arg(training_args, "ddp_find_unused_parameters", None) is None:
            self._set_arg(training_args, "ddp_find_unused_parameters", False)

        # Pin memory for CUDA dataloaders if not set
        if self.cuda_available and self._get_arg(training_args, "dataloader_pin_memory", None) is None:
            self._set_arg(training_args, "dataloader_pin_memory", True)

        # Limit CPU threads to avoid CPU RAM pressure if not set
        if self._get_arg(training_args, "dataloader_num_workers", None) is None:
            # Heuristic: fewer workers on constrained RAM
            num_workers = 2
            if self.psutil:
                try:
                    avail_gib = float(self.get_memory_info().get(
                        "cpu", {}).get("available_gib") or 0.0)
                    if avail_gib >= 16:
                        num_workers = 4
                except Exception:
                    pass
            self._set_arg(training_args, "dataloader_num_workers", num_workers)

        return training_args
