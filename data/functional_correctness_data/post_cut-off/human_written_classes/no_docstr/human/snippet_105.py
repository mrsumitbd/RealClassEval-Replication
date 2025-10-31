import torch

class PagedKVCache:

    def __init__(self, PAGE_SIZE: int=1, num_layers: int=32, batch_size: int=1, max_length: int=1024, num_kv_heads: int=8, head_dim: int=128, dtype=torch.bfloat16) -> None:
        self.max_num_blocks_per_seq = (max_length + PAGE_SIZE - 1) // PAGE_SIZE
        self.num_layers = num_layers
        self.batch_size = batch_size
        self.max_length = max_length
        self.num_kv_heads = num_kv_heads
        self.head_dim = head_dim
        self.dtype = dtype
        MAX_NUM_KV_BLOCKS = self.max_num_blocks_per_seq * batch_size * num_layers
        self.key_cache = torch.randn(MAX_NUM_KV_BLOCKS, PAGE_SIZE, num_kv_heads, head_dim, dtype=dtype, device=torch.cuda.current_device())
        self.value_cache = torch.randn(MAX_NUM_KV_BLOCKS, PAGE_SIZE, num_kv_heads, head_dim, dtype=dtype, device=torch.cuda.current_device())
        self.block_tables = torch.randperm(MAX_NUM_KV_BLOCKS, dtype=torch.int32, device=torch.cuda.current_device()).reshape(num_layers, batch_size, self.max_num_blocks_per_seq)
        assert self.block_tables.numel() <= MAX_NUM_KV_BLOCKS * PAGE_SIZE
        self.kv_lens = torch.zeros(batch_size, dtype=torch.int32, device=torch.cuda.current_device())

    def inc_offset(self, seq_len: int):
        self.kv_lens += seq_len

    def get_layer_kv_cache(self, layer_idx: int):
        return (self.key_cache, self.value_cache, self.block_tables[layer_idx], self.kv_lens)