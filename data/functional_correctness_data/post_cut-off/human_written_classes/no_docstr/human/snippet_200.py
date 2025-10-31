import pynvml
import os
import math

class Device:
    _nvml_affinity_elements = math.ceil(os.cpu_count() / 64)

    def __init__(self, device_idx: int):
        super().__init__()
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(device_idx)

    def get_name(self) -> str:
        return pynvml.nvmlDeviceGetName(self.handle)

    def get_cpu_affinity(self) -> list[int]:
        affinity_string = ''
        for j in pynvml.nvmlDeviceGetCpuAffinity(self.handle, Device._nvml_affinity_elements):
            affinity_string = f'{j:064b}' + affinity_string
        affinity_list = [int(x) for x in affinity_string]
        affinity_list.reverse()
        return [i for i, e in enumerate(affinity_list) if e != 0]