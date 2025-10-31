from typing import Optional, List, Dict, Generator
from contextlib import contextmanager
import os
import subprocess


class GPUManager:
    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        self.gpu_indices: Optional[List[int]] = None
        if gpu_indices is not None:
            if not isinstance(gpu_indices, list) or not all(isinstance(i, int) and i >= 0 for i in gpu_indices):
                raise ValueError(
                    "gpu_indices must be a list of non-negative integers")
            # Remove duplicates while preserving order
            seen = set()
            ordered_unique = []
            for i in gpu_indices:
                if i not in seen:
                    seen.add(i)
                    ordered_unique.append(i)
            self.gpu_indices = ordered_unique

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        prev_value = os.environ.get("CUDA_VISIBLE_DEVICES", None)
        try:
            if self.gpu_indices is not None:
                os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(
                    str(i) for i in self.gpu_indices)
            yield
        finally:
            if prev_value is None:
                os.environ.pop("CUDA_VISIBLE_DEVICES", None)
            else:
                os.environ["CUDA_VISIBLE_DEVICES"] = prev_value

    def get_memory_usage(self) -> Dict[int, int]:
        # Try pynvml first
        try:
            import pynvml  # type: ignore

            try:
                pynvml.nvmlInit()
                count = pynvml.nvmlDeviceGetCount()
                usage: Dict[int, int] = {}
                for i in range(count):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    usage[i] = int(mem.used // (1024 ** 2))  # MiB
                return usage
            finally:
                try:
                    pynvml.nvmlShutdown()
                except Exception:
                    pass
        except Exception:
            pass

        # Fallback to nvidia-smi
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=index,memory.used",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            usage: Dict[int, int] = {}
            for line in result.stdout.strip().splitlines():
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 2:
                    continue
                idx_str, mem_str = parts
                try:
                    idx = int(idx_str)
                    mem = int(mem_str)
                    usage[idx] = mem
                except ValueError:
                    continue
            return usage
        except Exception:
            return {}
