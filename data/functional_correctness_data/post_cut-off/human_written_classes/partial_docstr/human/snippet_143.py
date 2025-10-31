from flash_attn import flash_attn_with_kvcache
from torch import nn
from triton_dist.kernels.amd.all_gather_gemm import create_ag_gemm_intra_node_context, ag_gemm_intra_node
from triton_dist.kernels.amd.gemm_reduce_scatter import create_gemm_rs_intra_node_context, gemm_rs_intra_node
import torch
import torch.distributed

class TP_Attn:
    """
    Tensor Parallel Attention.
    QKV Projection: Column Parallelism on weights (sharded over head dimension).
    Output Projection: Row Parallelism on weights.
    """

    def __init__(self, rank=0, world_size=8, group=None):
        self.rank = rank
        self.world_size = world_size
        self.group = group
        self.head_dim = 128
        self.wqkv = None
        self.wo = None

    def _init_parameters(self, self_attn: nn.Module, verbose=False):
        self.q_size = self_attn.q_proj.weight.shape[0] // self.world_size
        self.kv_size = self_attn.k_proj.weight.shape[0] // self.world_size
        wq = shard_local(self_attn.q_proj.weight.detach(), self.world_size, 0, self.rank)
        wk = shard_local(self_attn.k_proj.weight.detach(), self.world_size, 0, self.rank)
        wv = shard_local(self_attn.v_proj.weight.detach(), self.world_size, 0, self.rank)
        self.wqkv = torch.cat((wq, wk, wv), dim=0).to('cuda', non_blocking=True)
        self.wo = shard_local(self_attn.o_proj.weight.detach(), self.world_size, 1, self.rank).to('cuda', non_blocking=True)
        self.ag_N_per_rank = self.wqkv.shape[0]
        self.K = self.wqkv.shape[1]
        self.dtype = self.wqkv.dtype
        if hasattr(self_attn, 'q_norm'):
            self.q_norm_eps = self_attn.q_norm.variance_epsilon
            self.q_norm_w = self_attn.q_norm.weight.detach().to('cuda', non_blocking=True)
        if hasattr(self_attn, 'k_norm'):
            self.k_norm_eps = self_attn.k_norm.variance_epsilon
            self.k_norm_w = self_attn.k_norm.weight.detach().to('cuda', non_blocking=True)
        if verbose:
            print(f'[RANK {self.rank}] Attn initialized with parameters: qkv ({self.wqkv.shape}, o ({self.wo.shape}))')

    def _init_ctx(self, max_M, ag_intranode_stream, BLOCK_M, BLOCK_N, BLOCK_K, stages, serial=False, ag_internode_stream=None):
        if serial:
            print(f'[RANK {self.rank}] Using serial mode for AG-GEMM.')
        self.ag_ctx = create_ag_gemm_intra_node_context(max_M=max_M, N=self.ag_N_per_rank, K=self.K, rank=self.rank, num_ranks=self.world_size, input_dtype=self.dtype, output_dtype=self.dtype, tp_group=self.group, ag_streams=ag_intranode_stream, serial=serial, autotune=True, BLOCK_M=BLOCK_M, BLOCK_N=BLOCK_N, BLOCK_K=BLOCK_K, stages=stages, M_PER_CHUNK=256)
        self.rs_ctx = create_gemm_rs_intra_node_context(max_M=max_M, N=self.K, rank=self.rank, num_ranks=self.world_size, output_dtype=self.dtype, tp_group=self.group, fuse_scatter=True)
        torch.cuda.synchronize()

    @torch.inference_mode()
    def apply_rotary_pos_emb(self, q: torch.Tensor, k: torch.Tensor, position_ids: torch.Tensor, cos_sin_cache: torch.Tensor):
        """Applies Rotary Position Embedding inplace."""
        bsz, seq, _ = q.shape
        q = q.view(bsz, seq, -1, self.head_dim)
        k = k.view(bsz, seq, -1, self.head_dim)
        q = apply_rotary_pos_emb(q, cos_sin_cache, position_ids).view(bsz, seq, -1, self.head_dim)
        k = apply_rotary_pos_emb(k, cos_sin_cache, position_ids).view(bsz, seq, -1, self.head_dim)
        return (q, k)

    @torch.inference_mode()
    def torch_fwd(self, x, position_ids, cos_sin_cache, kv_cache, layer_idx: int):
        """
        Reference PyTorch forward pass for attention with Tensor Parallelism.
        Activations related to head dimensions are sharded. Final output is AllReduced.
        x: input tensor, shape [batch_size, q_len, hidden_size_in] (replicated on each rank)
        """
        bsz, q_len, _ = x.size()
        qkv = torch.nn.functional.linear(x, self.wqkv)
        q, k, v = qkv.split([self.q_size, self.kv_size, self.kv_size], dim=-1)
        v = v.view(bsz, q_len, -1, self.head_dim)
        if hasattr(self, 'q_norm_eps'):
            q = layer_norm(q.contiguous().view(bsz, q_len, -1, self.head_dim), self.q_norm_eps, self.q_norm_w).view(bsz, q_len, -1)
        if hasattr(self, 'k_norm_eps'):
            k = layer_norm(k.contiguous().view(bsz, q_len, -1, self.head_dim), self.k_norm_eps, self.k_norm_w).view(bsz, q_len, -1)
        q, k = self.apply_rotary_pos_emb(q, k, position_ids, cos_sin_cache)
        k_cache, v_cache, kv_offset = kv_cache.update_kv_cache(k, v, layer_idx)
        out = flash_attn_with_kvcache(q=q, k_cache=k_cache, v_cache=v_cache, k=k, v=v, cache_seqlens=kv_offset, causal=True)
        out = torch.nn.functional.linear(out.view(bsz, q_len, -1), self.wo)
        if self.world_size > 1:
            torch.distributed.all_reduce(out, torch.distributed.ReduceOp.SUM, group=self.group)
        return out

    @torch.inference_mode()
    def dist_triton_fwd(self, x, position_ids, cos_sin_cache, kv_cache, layer_idx: int):
        """
        triton_dist forward pass.
        Input x is batch-sharded. Output is also batch-sharded.
        x: input tensor, shape [batch_size_per_rank, q_len, hidden_size_in]
        """
        bsz, q_len, d = x.size()
        qkv = ag_gemm_intra_node(x.view(-1, d), self.wqkv, transe_b=False, ctx=self.ag_ctx).view(bsz * self.world_size, q_len, -1)
        q, k, v = qkv.split([self.q_size, self.kv_size, self.kv_size], dim=-1)
        v = v.view(bsz * self.world_size, q_len, -1, self.head_dim)
        if hasattr(self, 'q_norm_eps'):
            q = layer_norm(q.contiguous().view(bsz * self.world_size, q_len, -1, self.head_dim), self.q_norm_eps, self.q_norm_w).view(bsz * self.world_size, q_len, -1)
        if hasattr(self, 'k_norm_eps'):
            k = layer_norm(k.contiguous().view(bsz * self.world_size, q_len, -1, self.head_dim), self.k_norm_eps, self.k_norm_w).view(bsz * self.world_size, q_len, -1)
        q, k = self.apply_rotary_pos_emb(q, k, position_ids, cos_sin_cache)
        k_cache, v_cache, kv_offset = kv_cache.update_kv_cache(k, v, layer_idx)
        out = flash_attn_with_kvcache(q=q, k_cache=k_cache, v_cache=v_cache, k=k, v=v, cache_seqlens=kv_offset, causal=True)
        out = gemm_rs_intra_node(out.view(bsz * self.world_size * q_len, -1), self.wo, self.rs_ctx).view(bsz, q_len, -1)
        return out

    def fwd(self, x: torch.Tensor, position_ids: torch.Tensor, cos_sin_cache: torch.Tensor, kv_cache, layer_idx: int):
        raise NotImplementedError('Please use torch_fwd or dist_triton_fwd instead.')