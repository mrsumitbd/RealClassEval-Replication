import torch
import dataclasses
from triton_dist.utils import nvshmem_barrier_all_on_stream, nvshmem_create_tensor, nvshmem_free_tensor_sync, launch_cooperative_grid_options

@dataclasses.dataclass
class GemmARContext:
    symm_gemm_out_buf: torch.Tensor
    symm_ar_out_buf: torch.Tensor
    gemm_barrier_buf: torch.Tensor
    multi_st_barrier_buf: torch.Tensor
    grid_barrier_buf: torch.Tensor
    NUM_COMM_SMS: int
    ar_stream: torch.cuda.Stream

    def finalize(self):
        nvshmem_free_tensor_sync(self.symm_gemm_out_buf)
        nvshmem_free_tensor_sync(self.symm_ar_out_buf)
        nvshmem_free_tensor_sync(self.gemm_barrier_buf)
        nvshmem_free_tensor_sync(self.multi_st_barrier_buf)

    def get_gemm_out_buf(self, input, weight):
        M, N = (input.shape[0], weight.shape[0])
        assert self.symm_gemm_out_buf.numel() >= M * N
        return self.symm_gemm_out_buf.reshape(-1)[:M * N].reshape(M, N)