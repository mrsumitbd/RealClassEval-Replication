
from typing import Optional, List, Dict, Generator
from contextlib import contextmanager
import subprocess
import os


class GPUManager:

    def __init__(self, gpu_indices: Optional[List[int]] = None) -> None:
        self.gpu_indices = gpu_indices
        self._original_cuda_visible_devices = None

    @contextmanager
    def manage_resources(self) -> Generator[None, None, None]:
        try:
            self._original_cuda_visible_devices = os.environ.get(
                "CUDA_VISIBLE_DEVICES")
            if self.gpu_indices is not None:
                os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(
                    str(i) for i in self.gpu_indices)
            yield
        finally:
            if self._original_cuda_visible_devices is not None:
                os.environ["CUDA_VISIBLE_DEVICES"] = self._original_cuda_visible_devices
            else:
                if "CUDA_VISIBLE_DEVICES" in os.environ:
                    del os.environ["CUDA_VISIBLE_DEVICES"]

    def get_memory_usage(self) -> Dict[int, int]:
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=index,memory.used",
                    "--format=csv,noheader,nounits"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                encoding="utf-8"
            )
            lines = result.stdout.strip().split('\n')
            usage = {}
            for line in lines:
                parts = [x.strip() for x in line.split(',')]
                if len(parts) == 2:
                    idx, mem = int(parts[0]), int(parts[1])
                    if self.gpu_indices is None or idx in self.gpu_indices:
                        usage[idx] = mem
            return usage
        except Exception:
            return {}
