from typing import Optional, List, Dict, Generator
from contextlib import contextmanager
import os
import subprocess


class GPUManager:

    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        if gpu_indices is not None:
            if not isinstance(gpu_indices, list) or not all(isinstance(i, int) and i >= 0 for i in gpu_indices):
                raise ValueError(
                    "gpu_indices must be a list of non-negative integers or None")
            self.gpu_indices = list(dict.fromkeys(gpu_indices))
        else:
            self.gpu_indices = None
        self._original_cuda_visible_devices: Optional[str] = None

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        self._original_cuda_visible_devices = os.environ.get(
            "CUDA_VISIBLE_DEVICES", None)
        try:
            if self.gpu_indices is not None:
                os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(
                    str(i) for i in self.gpu_indices)
            yield
        finally:
            if self._original_cuda_visible_devices is None:
                os.environ.pop("CUDA_VISIBLE_DEVICES", None)
            else:
                os.environ["CUDA_VISIBLE_DEVICES"] = self._original_cuda_visible_devices
            self._original_cuda_visible_devices = None

    def _env_visible_indices(self) -> Optional[List[int]]:
        val = os.environ.get("CUDA_VISIBLE_DEVICES", None)
        if val is None:
            return None
        val = val.strip()
        if val == "":
            return []
        try:
            return [int(x) for x in val.split(",") if x.strip() != ""]
        except ValueError:
            return None

    def _indices_to_query(self) -> Optional[List[int]]:
        if self.gpu_indices is not None:
            return self.gpu_indices
        env_idxs = self._env_visible_indices()
        if env_idxs is not None:
            return env_idxs
        return None  # means all

    def get_memory_usage(self) -> Dict[int, int]:
        indices = self._indices_to_query()

        # Try pynvml first
        try:
            import pynvml  # type: ignore
            pynvml.nvmlInit()
            try:
                count = pynvml.nvmlDeviceGetCount()
                if indices is None:
                    query_indices = list(range(count))
                else:
                    query_indices = [i for i in indices if 0 <= i < count]
                usage: Dict[int, int] = {}
                for i in query_indices:
                    try:
                        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                        # Return MiB to be consistent and compact
                        usage[i] = int(mem.used // (1024 * 1024))
                    except Exception:
                        continue
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
            cmd = [
                "nvidia-smi",
                "--query-gpu=index,memory.used",
                "--format=csv,noheader,nounits",
            ]
            out = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, text=True)
            usage_all: Dict[int, int] = {}
            for line in out.strip().splitlines():
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 2:
                    continue
                try:
                    idx = int(parts[0])
                    used_mib = int(parts[1])
                    usage_all[idx] = used_mib
                except ValueError:
                    continue
            if indices is None:
                return usage_all
            return {i: usage_all[i] for i in indices if i in usage_all}
        except Exception:
            return {}
