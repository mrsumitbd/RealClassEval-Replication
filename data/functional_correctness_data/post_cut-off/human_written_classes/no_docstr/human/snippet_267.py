from typing import List, Optional, Type
import importlib
import torch.nn as nn

class ModelRegistry:

    @staticmethod
    def load_model_cls(model_arch: str, value=False) -> Optional[Type[nn.Module]]:
        if model_arch not in _MODELS:
            return None
        megatron = 'megatron'
        module_name, model_cls_name = _MODELS[model_arch]
        if not value:
            model_cls_name = model_cls_name[0]
        elif value:
            model_cls_name = model_cls_name[1]
        module = importlib.import_module(f'siirl.models.{module_name}.{megatron}.modeling_{module_name}_megatron')
        return getattr(module, model_cls_name, None)

    @staticmethod
    def get_supported_archs() -> List[str]:
        return list(_MODELS.keys())