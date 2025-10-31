from triton_dist.utils import CUDA_CHECK, NVSHMEM_SIGNAL_DTYPE, supports_p2p_native_atomic, get_device_property, launch_cooperative_grid_options, nvshmem_barrier_all_on_stream, nvshmem_create_tensor, nvshmem_free_tensor_sync, requires, is_nvshmem_multimem_supported, has_tma
import dataclasses
import torch

@dataclasses.dataclass
class AllReduceContext:
    workspace_nbytes: int
    rank: int
    world_size: int
    local_world_size: int
    symm_scatter_buf: torch.Tensor
    symm_signal: torch.Tensor
    phase: int = 0
    grid_barrier: torch.Tensor = dataclasses.field(init=False)
    local_rank: int = dataclasses.field(init=False)
    node_id: int = dataclasses.field(init=False)
    nnodes: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.local_rank = self.rank % self.local_world_size
        self.node_id = self.rank // self.local_world_size
        assert self.world_size % self.local_world_size == 0
        self.nnodes = self.world_size // self.local_world_size
        self.grid_barrier = torch.zeros(1, dtype=torch.int32, device='cuda')

    def finalize(self):
        nvshmem_free_tensor_sync(self.symm_scatter_buf)
        nvshmem_free_tensor_sync(self.symm_signal)