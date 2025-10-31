from typing import Any
import torch
import torch.distributed as dist
from torch.distributed.tensor import DTensor

class DTensorFastEmaModelUpdater:
    """
    Similar as FastEmaModelUpdater
    """

    def __init__(self):
        self.is_cached = False

    @torch.no_grad()
    def copy_to(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module) -> None:
        for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters(), strict=False):
            if isinstance(tgt_params, DTensor) and isinstance(src_params, DTensor):
                tgt_params.to_local().data.copy_(src_params.to_local().data)
            else:
                tgt_params.to_local().data.copy_(src_params.to_local().data)

    @torch.no_grad()
    def update_average(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module, beta: float=0.9999) -> None:
        target_list = []
        source_list = []
        for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters(), strict=False):
            assert tgt_params.dtype == torch.float32, f'EMA model only works in FP32 dtype, got {tgt_params.dtype} instead.'
            if isinstance(tgt_params, DTensor) and isinstance(src_params, DTensor):
                target_list.append(tgt_params.to_local())
                source_list.append(src_params.to_local().data)
            else:
                target_list.append(tgt_params)
                source_list.append(src_params.data)
        torch._foreach_mul_(target_list, beta)
        torch._foreach_add_(target_list, source_list, alpha=1.0 - beta)

    @torch.no_grad()
    def cache(self, parameters: Any, is_cpu: bool=False) -> None:
        assert self.is_cached is False, 'EMA cache is already taken. Did you forget to restore it?'
        device = 'cpu' if is_cpu else 'cuda'
        self.collected_params = [param.to_local().clone().to(device) for param in parameters]
        self.is_cached = True

    @torch.no_grad()
    def restore(self, parameters: Any) -> None:
        assert self.is_cached, 'EMA cache is not taken yet.'
        for c_param, param in zip(self.collected_params, parameters, strict=False):
            param.to_local().copy_(c_param.data.type_as(param.data))
        self.collected_params = []
        self.is_cached = False