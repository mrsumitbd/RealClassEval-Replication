import torch
from typing import TYPE_CHECKING, Any

class FastEmaModelUpdater:
    """
    This class is used to update target model~(EMA) given source model~(regular model) and beta.
    The method interaface mimic :class:`EMAModelTracker` and :class:`PowerEMATracker`.
    Different from two classes, this class does not maintain the EMA model weights as buffers. It expects the user to have two module with same architecture and weights shape.
    The class is proposed to work with FSDP model where above two classes are not working as expected. Besides, it is strange to claim model weights as buffers and do unnecessary name changing in :class:`EMAModelTracker` and :class:`PowerEMATracker`. Moeving forward, we should use this class instead of above two classes.
    """

    def __init__(self):
        self.is_cached = False

    @torch.no_grad()
    def copy_to(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module) -> None:
        for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters(), strict=False):
            tgt_params.data.copy_(src_params.data)

    @torch.no_grad()
    def update_average(self, src_model: torch.nn.Module, tgt_model: torch.nn.Module, beta: float=0.9999) -> None:
        target_list = []
        source_list = []
        for tgt_params, src_params in zip(tgt_model.parameters(), src_model.parameters(), strict=False):
            assert tgt_params.dtype == torch.float32, f'EMA model only works in FP32 dtype, got {tgt_params.dtype} instead.'
            target_list.append(tgt_params)
            source_list.append(src_params.data)
        torch._foreach_mul_(target_list, beta)
        torch._foreach_add_(target_list, source_list, alpha=1.0 - beta)

    @torch.no_grad()
    def cache(self, parameters: Any, is_cpu: bool=False) -> None:
        """Save the current parameters for restoring later.

        Args:
            parameters (iterable): Iterable of torch.nn.Parameter to be temporarily stored.
        """
        assert self.is_cached is False, 'EMA cache is already taken. Did you forget to restore it?'
        device = 'cpu' if is_cpu else 'cuda'
        self.collected_params = [param.clone().to(device) for param in parameters]
        self.is_cached = True

    @torch.no_grad()
    def restore(self, parameters: Any) -> None:
        """Restore the parameters in self.collected_params.

        Useful to validate the model with EMA parameters without affecting the
        original optimization process. Store the parameters before copy_to().
        After validation (or model saving), use this to restore the former parameters.

        Args:
            parameters (iterable): Iterable of torch.nn.Parameter to be updated with the stored parameters.
        """
        assert self.is_cached, 'EMA cache is not taken yet.'
        for c_param, param in zip(self.collected_params, parameters, strict=False):
            param.data.copy_(c_param.data.type_as(param.data))
        self.collected_params = []
        self.is_cached = False