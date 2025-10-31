from typing import Dict, Any, List, Optional, Union
import os
import sys
import gc
import platform


class MemoryManager:
    def __init__(self):
        self._torch = None
        self._psutil = None
        self._nvml = None
        self._init_libs()

    def _init_libs(self):
        try:
            import torch  # type: ignore
            self._torch = torch
        except Exception:
            self._torch = None
        try:
            import psutil  # type: ignore
            self._psutil = psutil
        except Exception:
            self._psutil = None
        try:
            import pynvml  # type: ignore
            self._nvml = pynvml
            try:
                self._nvml.nvmlInit()
            except Exception:
                self._nvml = None
        except Exception:
            self._nvml = None

    def __del__(self):
        try:
            if self._nvml is not None:
                try:
                    self._nvml.nvmlShutdown()
                except Exception:
                    pass
        except Exception:
            pass

    def get_memory_info(self) -> Dict[str, Any]:
        cpu_info = self._get_cpu_memory()
        gpu_info = self._get_gpu_memory()
        device = self._select_primary_device(gpu_info)
        return {
            "device": device,
            "cpu": cpu_info,
            "gpus": gpu_info,
            "platform": platform.platform(),
            "python": sys.version.split()[0],
        }

    def cleanup_memory(self, force: bool = False) -> None:
        gc.collect()
        torch = self._torch
        if torch is not None:
            try:
                if hasattr(torch, "cuda") and torch.cuda.is_available():
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
                            torch.cuda.synchronize()
                        except Exception:
                            pass
                # MPS (Apple Silicon)
                try:
                    if hasattr(torch, "mps") and torch.backends.mps.is_available():
                        try:
                            torch.mps.empty_cache()
                        except Exception:
                            pass
                except Exception:
                    pass
                # XLA cleanup is typically handled by runtime; skip
            except Exception:
                pass

    def get_optimal_training_config(self) -> Dict[str, Any]:
        mem = self.get_memory_info()
        gpus: List[Dict[str, Any]] = mem.get("gpus", [])
        torch = self._torch

        # Determine numerical GPU total memory (bytes)
        primary_gpu_mem = gpus[0]["total"] if gpus else 0
        total_cpu_mem = mem["cpu"]["total"]

        # Batch size heuristic
        bs = 1
        if primary_gpu_mem > 0:
            gb = primary_gpu_mem / (1024**3)
            if gb >= 40:
                bs = 32
            elif gb >= 24:
                bs = 16
            elif gb >= 12:
                bs = 8
            elif gb >= 8:
                bs = 4
            elif gb >= 6:
                bs = 2
            else:
                bs = 1
        else:
            # CPU training fallback
            gb = total_cpu_mem / (1024**3)
            if gb >= 64:
                bs = 8
            elif gb >= 32:
                bs = 4
            elif gb >= 16:
                bs = 2
            else:
                bs = 1

        # Gradient accumulation to target effective batch size ~32
        target_effective_bs = 32
        grad_accum = max(1, target_effective_bs // max(1, bs))

        # Precision selection
        use_bf16 = False
        use_fp16 = False
        use_tf32 = False

        if torch is not None:
            try:
                if hasattr(torch, "cuda") and torch.cuda.is_available():
                    # TF32 on Ampere+ improves throughput without precision loss for matmul
                    try:
                        # Enable tf32 only if compute capability supports it (Ampere+)
                        major, minor = torch.cuda.get_device_capability(0)
                        if major >= 8:
                            use_tf32 = True
                    except Exception:
                        pass
                    try:
                        if hasattr(torch.cuda, "is_bf16_supported") and torch.cuda.is_bf16_supported():
                            use_bf16 = True
                        else:
                            use_fp16 = True
                    except Exception:
                        use_fp16 = True
                elif hasattr(torch, "backends") and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                    # MPS prefers fp32/bf16 autocast at runtime; keep full precision by default
                    use_bf16 = False
                    use_fp16 = False
                else:
                    use_bf16 = False
                    use_fp16 = False
            except Exception:
                pass

        # Gradient checkpointing on tighter memory
        enable_gc = (primary_gpu_mem and primary_gpu_mem <=
                     16 * (1024**3)) or (primary_gpu_mem == 0)

        # DataLoader workers heuristic
        cpu_count = os.cpu_count() or 1
        num_workers = min(4, max(0, cpu_count - 1))

        return {
            "per_device_train_batch_size": bs,
            "gradient_accumulation_steps": grad_accum,
            "fp16": bool(use_fp16 and not use_bf16),
            "bf16": bool(use_bf16),
            "tf32": bool(use_tf32),
            "gradient_checkpointing": bool(enable_gc),
            "dataloader_num_workers": num_workers,
            "device": mem["device"],
            "memory": mem,
        }

    def optimize_model_for_training(self, model):
        cfg = self.get_optimal_training_config()
        torch = self._torch

        if torch is not None:
            device = cfg["device"]
            try:
                if device == "cuda" and torch.cuda.is_available():
                    model = model.to("cuda")
                elif device == "mps" and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                    model = model.to("mps")
                else:
                    model = model.to("cpu")
            except Exception:
                pass

            if cfg.get("gradient_checkpointing", False):
                try:
                    if hasattr(model, "gradient_checkpointing_enable"):
                        model.gradient_checkpointing_enable()
                except Exception:
                    pass

            try:
                if cfg.get("tf32", False) and hasattr(torch.backends, "cuda") and hasattr(torch.backends.cuda, "matmul"):
                    torch.backends.cuda.matmul.allow_tf32 = True
            except Exception:
                pass

            # Prefer leaving precision management to AMP/autocast in the training loop.

        return model

    def optimize_training_args(self, training_args):
        cfg = self.get_optimal_training_config()

        def set_field(obj, key: str, value):
            if obj is None:
                return
            try:
                if isinstance(obj, dict):
                    obj[key] = value
                else:
                    if hasattr(obj, key):
                        setattr(obj, key, value)
            except Exception:
                pass

        # Common fields for Hugging Face TrainingArguments or dict-like configs
        set_field(training_args, "per_device_train_batch_size",
                  cfg["per_device_train_batch_size"])
        set_field(training_args, "gradient_accumulation_steps",
                  cfg["gradient_accumulation_steps"])
        set_field(training_args, "fp16", cfg["fp16"])
        set_field(training_args, "bf16", cfg["bf16"])
        set_field(training_args, "dataloader_num_workers",
                  cfg["dataloader_num_workers"])

        # Optional extras commonly present in TrainingArguments
        # Enable TF32 when available
        if cfg.get("tf32", False):
            set_field(training_args, "tf32", True)

        # Enable gradient checkpointing if supported
        set_field(training_args, "gradient_checkpointing",
                  cfg["gradient_checkpointing"])

        # Set device-related flags if present in the object
        set_field(training_args, "lr_scheduler_type", getattr(training_args, "lr_scheduler_type", "linear")
                  if not isinstance(training_args, dict) else training_args.get("lr_scheduler_type", "linear"))
        return training_args

    # -----------------------
    # Helpers
    # -----------------------
    def _get_cpu_memory(self) -> Dict[str, int]:
        total = 0
        available = 0
        psutil = self._psutil
        if psutil is not None:
            try:
                vm = psutil.virtual_memory()
                total = int(vm.total)
                available = int(vm.available)
                return {"total": total, "available": available}
            except Exception:
                pass

        # Fallbacks without psutil
        try:
            if sys.platform == "linux":
                meminfo = {}
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        parts = line.split(":")
                        if len(parts) == 2:
                            key = parts[0].strip()
                            val = parts[1].strip().split()[0]
                            try:
                                meminfo[key] = int(val) * 1024
                            except Exception:
                                pass
                total = int(meminfo.get("MemTotal", 0))
                available = int(meminfo.get(
                    "MemAvailable", meminfo.get("MemFree", 0)))
                return {"total": total, "available": available}
            elif sys.platform == "darwin":
                # macOS: use sysctl
                import subprocess
                total_out = subprocess.check_output(
                    ["sysctl", "-n", "hw.memsize"]).strip()
                total = int(total_out)
                # Approximate available via vm_stat
                vm_out = subprocess.check_output(["vm_stat"]).decode("utf-8")
                page_size = 4096
                for line in vm_out.splitlines():
                    if "page size of" in line and "bytes" in line:
                        try:
                            page_size = int(line.split(
                                "page size of")[-1].split("bytes")[0].strip())
                        except Exception:
                            pass
                pages_free = 0
                pages_inactive = 0
                for line in vm_out.splitlines():
                    if line.strip().startswith("Pages free:"):
                        pages_free = int(line.split(":")[1].strip().strip(
                            ".").replace(".", "").replace(",", ""))
                    if line.strip().startswith("Pages inactive:"):
                        pages_inactive = int(line.split(":")[1].strip().strip(
                            ".").replace(".", "").replace(",", ""))
                available = (pages_free + pages_inactive) * page_size
                return {"total": total, "available": available}
            elif sys.platform == "win32":
                import ctypes

                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', ctypes.c_ulonglong),
                        ('ullAvailPhys', ctypes.c_ulonglong),
                        ('ullTotalPageFile', ctypes.c_ulonglong),
                        ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong),
                        ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('sullAvailExtendedVirtual', ctypes.c_ulonglong),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                total = int(stat.ullTotalPhys)
                available = int(stat.ullAvailPhys)
                return {"total": total, "available": available}
        except Exception:
            pass
        return {"total": int(total), "available": int(available)}

    def _get_gpu_memory(self) -> List[Dict[str, Any]]:
        gpus: List[Dict[str, Any]] = []
        torch = self._torch

        # Prefer Torch CUDA
        try:
            if torch is not None and hasattr(torch, "cuda") and torch.cuda.is_available():
                count = torch.cuda.device_count()
                for idx in range(count):
                    try:
                        props = torch.cuda.get_device_properties(idx)
                        total = int(props.total_memory)
                        # Used/Free via memory_allocated isn't total usage; try torch.cuda.mem_get_info if available
                        free = None
                        used = None
                        try:
                            free_bytes, total_bytes = torch.cuda.mem_get_info(
                                idx)
                            free = int(free_bytes)
                            total = int(total_bytes)
                            used = total - free
                        except Exception:
                            # Fallback: approximate with reserved
                            try:
                                used = int(torch.cuda.memory_reserved(idx))
                                free = max(0, total - used)
                            except Exception:
                                used = None
                                free = None
                        name = props.name
                        gpus.append({
                            "index": idx,
                            "name": name,
                            "total": total,
                            "free": free,
                            "used": used,
                            "backend": "torch.cuda",
                        })
                    except Exception:
                        pass
                if gpus:
                    return gpus
        except Exception:
            pass

        # NVML fallback
        try:
            if self._nvml is not None:
                nvml = self._nvml
                count = nvml.nvmlDeviceGetCount()
                for idx in range(count):
                    try:
                        handle = nvml.nvmlDeviceGetHandleByIndex(idx)
                        mem = nvml.nvmlDeviceGetMemoryInfo(handle)
                        name = nvml.nvmlDeviceGetName(handle)
                        gpus.append({
                            "index": idx,
                            "name": name.decode("utf-8") if isinstance(name, bytes) else str(name),
                            "total": int(mem.total),
                            "free": int(mem.free),
                            "used": int(mem.used),
                            "backend": "nvml",
                        })
                    except Exception:
                        pass
                if gpus:
                    return gpus
        except Exception:
            pass

        # Apple MPS does not expose discrete memory sizes easily; provide placeholder
        try:
            if torch is not None and hasattr(torch, "backends") and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                gpus.append({
                    "index": 0,
                    "name": "Apple MPS",
                    "total": 0,
                    "free": None,
                    "used": None,
                    "backend": "mps",
                })
                return gpus
        except Exception:
            pass

        return gpus

    def _select_primary_device(self, gpus: List[Dict[str, Any]]) -> str:
        torch = self._torch
        if torch is not None:
            try:
                if hasattr(torch, "cuda") and torch.cuda.is_available():
                    return "cuda"
            except Exception:
                pass
            try:
                if hasattr(torch, "backends") and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                    return "mps"
            except Exception:
                pass
        return "cpu"
