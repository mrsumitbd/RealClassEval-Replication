from dataclasses import dataclass

@dataclass
class STCMetrics:
    bytes_loaded: int = 0
    time_elapsed: float = 0.0
    total_open_elapsed: float = 0.0
    deferred_tensors: int = 0
    deferred_passes: int = 0
    direct_tensors: int = 0
    total_chunks: int = 0

    def bandwidth_total(self):
        return self.bytes_loaded / 1024 ** 3 / (self.total_open_elapsed + 1e-08)

    def bandwidth(self):
        return self.bytes_loaded / 1024 ** 3 / (self.time_elapsed + 1e-08)

    def print(self):
        print(f' -- Total size: {self.bytes_loaded:,} bytes, {self.bytes_loaded / 1024 ** 3:.2f} GB')
        print(f' -- Load time: {self.time_elapsed:.3f} seconds')
        print(f' -- Overhead: {self.total_open_elapsed - self.time_elapsed:.3f} seconds')
        print(f' -- Bandwidth: {self.bandwidth():.3f} GB/s  /  {self.bandwidth_total():.3f} GB/s')
        print(f' -- Deferred: {self.deferred_tensors:,} tensors in {self.deferred_passes:,} passes, {self.total_chunks:,} chunks')
        print(f' -- Direct: {self.direct_tensors:,} tensors')