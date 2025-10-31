import torch
from triton_dist.kernels.nvidia.reduce_scatter import ReduceScatter2DContext, create_reduce_scater_2d_ctx, reduce_scatter_2d_op
from typing import List, Optional
import dataclasses
from triton_dist.utils import dist_print, generate_data, nvshmem_barrier_all_on_stream, nvshmem_create_tensors, nvshmem_free_tensor_sync, perf_func, finalize_distributed, initialize_distributed

@dataclasses.dataclass
class GEMMReduceScatterTensorParallelContext:
    rs_ctx: ReduceScatter2DContext
    output_dtype: torch.dtype
    symm_gemm_out_bufs: List[torch.Tensor]
    rs_stream: torch.cuda.Stream
    num_gemm_sms: int
    BLOCK_M: int = 128
    BLOCK_N: int = 256
    BLOCK_K: int = 64
    GROUP_M: int = 8
    stages: int = 3

    def get_gemm_out_buf(self, input):
        M, _ = input.shape
        local_rank = self.rs_ctx.local_rank
        return self.symm_gemm_out_bufs[local_rank][:M]

    def finalize(self):
        self.rs_ctx.finalize()
        nvshmem_free_tensor_sync(self.symm_gemm_out_bufs[self.rs_ctx.local_rank])