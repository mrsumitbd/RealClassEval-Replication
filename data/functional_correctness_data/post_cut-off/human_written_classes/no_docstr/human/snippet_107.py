import torch

class KV_Cache:

    def __init__(self, num_layers: int=32, batch_size: int=1, max_length: int=32 * 1024, kv_heads: int=8, head_dim: int=128, dtype=torch.bfloat16, world_size: int=8) -> None:
        self.num_layers = num_layers
        self.batch_size = batch_size
        self.max_length = max_length
        self.kv_heads = kv_heads
        self.head_dim = head_dim
        self.dtype = dtype
        self.world_size = world_size
        self.k_cache = torch.zeros(num_layers, batch_size, max_length, kv_heads // world_size, head_dim, device='cuda', dtype=self.dtype)
        self.v_cache = torch.zeros(num_layers, batch_size, max_length, kv_heads // world_size, head_dim, device='cuda', dtype=self.dtype)
        self.kv_offset = torch.zeros(batch_size, dtype=torch.int32, device='cuda')

    def update_kv_cache(self, new_k_cache: torch.Tensor, new_v_cache: torch.Tensor, layer_idx: int):
        return (self.k_cache[layer_idx], self.v_cache[layer_idx], self.kv_offset)

    def rand_fill_kv_cache(self, offset: int):
        kv_shape = self.k_cache[:, :, :offset].size()
        k = torch.rand(kv_shape, device='cuda', dtype=self.dtype) / 10
        v = torch.rand(kv_shape, device='cuda', dtype=self.dtype) / 10
        self.k_cache[:, :, :offset].copy_(k)
        self.v_cache[:, :, :offset].copy_(v)

    def inc_offset(self):
        self.kv_offset += 1

    def clear(self):
        self.kv_offset.zero_()

    def get_kv_len(self):
        return self.kv_offset