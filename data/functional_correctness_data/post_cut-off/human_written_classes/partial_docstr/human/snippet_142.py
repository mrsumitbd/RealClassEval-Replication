from triton_dist.utils import NVSHMEM_SIGNAL_DTYPE, nvshmem_free_tensor_sync, nvshmem_create_tensor
import torch

class AllToAllContext:

    def __init__(self, max_m: int, hidden: int, rank: int, num_tot_experts: int, WORLD_SIZE: int, experts_per_rank: int, dtype=torch.bfloat16, scale_dtype=torch.float):
        """
        max_m: max number of tokens per rank
        """
        self.send_buf = nvshmem_create_tensor((max_m, hidden), dtype)
        self.recv_buf = nvshmem_create_tensor((WORLD_SIZE * max_m * 2, hidden), dtype)
        self.scale_send_buf = nvshmem_create_tensor((max_m,), scale_dtype)
        self.scale_recv_buf = nvshmem_create_tensor((WORLD_SIZE * max_m * 2,), scale_dtype)
        self.split_send_buf = nvshmem_create_tensor((num_tot_experts,), torch.int32)
        self.split_recv_buf = nvshmem_create_tensor((num_tot_experts * 2,), torch.int32)
        self.signal_buf = nvshmem_create_tensor((WORLD_SIZE * 2,), NVSHMEM_SIGNAL_DTYPE)
        self.max_m = max_m
        self.hidden = hidden
        self.dtype = dtype
        self.scale_dtype = scale_dtype
        self.ele_size = dtype_size_in_bytes(self.dtype)
        self.scale_ele_size = dtype_size_in_bytes(self.scale_dtype)
        self.num_tot_experts = num_tot_experts
        self.experts_per_rank = experts_per_rank
        self.WORLD_SIZE = WORLD_SIZE
        self.rank = rank
        self.call_count = 1
        self.MOD_VALUE = 1000000

    def finalize(self):
        nvshmem_free_tensor_sync(self.send_buf)
        nvshmem_free_tensor_sync(self.recv_buf)
        nvshmem_free_tensor_sync(self.scale_send_buf)
        nvshmem_free_tensor_sync(self.scale_recv_buf)
        nvshmem_free_tensor_sync(self.split_send_buf)
        nvshmem_free_tensor_sync(self.split_recv_buf)
        nvshmem_free_tensor_sync(self.signal_buf)