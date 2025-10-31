import torch
from triton_dist.models.kv_cache import KV_Cache
import torch.nn.functional as F

class DenseLLMLayer:
    """
    A single layer of DenseLLM, containing self-attention and MLP.
    This layer is designed to be used in a tensor parallel setting.
    It initializes the parameters and sets the forward pass method based on the mode.
    """

    def __init__(self, layer_idx, group) -> None:
        self.attn: TP_Attn = None
        self.mlp: TP_MLP = None
        self.input_norm_eps = None
        self.input_norm_w = None
        self.post_norm_eps = None
        self.post_norm_w = None
        self.layer_idx = layer_idx
        self.group = group

    def init_parameters(self, hf_layer, rank: int, world_size: int):
        self.mlp = TP_MLP(rank=rank, world_size=world_size, group=self.group)
        self.mlp._init_parameters(hf_layer.mlp)
        self.attn = TP_Attn(rank=rank, world_size=world_size, group=self.group)
        self.attn._init_parameters(hf_layer.self_attn)
        self.input_norm_eps = hf_layer.input_layernorm.variance_epsilon
        self.input_norm_w = hf_layer.input_layernorm.weight.detach().cuda()
        self.post_norm_eps = hf_layer.post_attention_layernorm.variance_epsilon
        self.post_norm_w = hf_layer.post_attention_layernorm.weight.detach().cuda()

    def set_fwd(self, mode: str='torch'):
        if mode == 'triton_dist':
            self.attn.fwd = self.attn.dist_triton_fwd
            self.mlp.fwd = self.mlp.dist_triton_fwd
        elif mode == 'torch':
            self.attn.fwd = self.attn.torch_fwd
            self.mlp.fwd = self.mlp.torch_fwd
        elif mode == 'triton_dist_AR':
            self.attn.fwd = self.attn.dist_triton_AR_fwd
            self.mlp.fwd = self.mlp.dist_triton_AR_fwd
        elif mode == 'triton_dist_gemm_ar':
            self.attn.fwd = self.attn.dist_triton_gemm_ar_fwd
            self.mlp.fwd = self.mlp.dist_triton_gemm_ar_fwd
        else:
            raise ValueError(f"Unsupported mode: {mode}, choose from ['dist_triton', 'torch']")

    @torch.inference_mode()
    def fwd(self, hidden_states: torch.Tensor, position_ids: torch.Tensor, cos_sin_cache: torch.Tensor, kv_cache: KV_Cache):
        residual = hidden_states
        hidden_states = layer_norm(hidden_states, self.input_norm_eps, self.input_norm_w)
        hidden_states = self.attn.fwd(hidden_states, position_ids, cos_sin_cache, kv_cache, self.layer_idx)
        hidden_states = residual + hidden_states
        residual = hidden_states
        hidden_states = layer_norm(hidden_states, self.post_norm_eps, self.post_norm_w)
        hidden_states = self.mlp.fwd(hidden_states)
        hidden_states = residual + hidden_states
        return hidden_states