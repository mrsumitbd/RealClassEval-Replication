from triton_dist.utils import NVSHMEM_SIGNAL_DTYPE, has_fullmesh_nvlink, launch_cooperative_grid_options, nvshmem_barrier_all_on_stream, nvshmem_create_tensor, nvshmem_free_tensor_sync
import torch
from dataclasses import dataclass, field

@dataclass
class MoEReduceRSContext:
    max_M: int
    N: int
    num_experts: int
    topk: int
    dtype: torch.dtype
    rank: int
    num_ranks: int
    num_local_ranks: int
    n_chunks_max: int
    grid_barrier: torch.Tensor
    gemm_counter: torch.Tensor
    gemm_done_flag: torch.Tensor
    rs_counter: torch.Tensor
    symm_barrier: torch.Tensor = field(init=False)
    symm_reduce_scatter_buffer: torch.Tensor = field(init=False)
    local_rank: int = field(init=False)
    nnodes: int = field(init=False)
    reduce_stream: torch.cuda.Stream = field(default_factory=lambda: torch.cuda.Stream(priority=-1))

    def __post_init__(self):
        assert self.dtype in [torch.bfloat16, torch.float16], 'Currently only used for float16 or bfloat16'
        assert self.max_M % self.topk == 0, 'M must be divisible by topk'
        self.local_rank = self.rank % self.num_local_ranks
        self.nnodes = self.num_ranks // self.num_local_ranks
        self.symm_barrier = nvshmem_create_tensor((self.n_chunks_max * self.num_ranks,), NVSHMEM_SIGNAL_DTYPE)
        self.symm_barrier.zero_()
        ntokens = self.max_M // self.topk
        self.symm_reduce_scatter_buffer = nvshmem_create_tensor((ntokens, self.N), self.dtype)
        nvshmem_barrier_all_on_stream(torch.cuda.current_stream())
        torch.cuda.synchronize()

    def finalize(self):
        nvshmem_free_tensor_sync(self.symm_barrier)
        nvshmem_free_tensor_sync(self.symm_reduce_scatter_buffer)