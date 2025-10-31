from typing import Optional
import torch
from dataclasses import dataclass

@dataclass
class ExternalTensorTrait:
    """Represents a 'trait' that can be applied to a Tensor to signal that
    it is to be loaded by name from an external archive at AOT execution time.
    """
    external_scope: str
    external_name: str

    @staticmethod
    def get(from_tensor: torch.Tensor) -> Optional['ExternalTensorTrait']:
        existing = getattr(from_tensor, '_turbine_external_tensor_trait', None)
        if existing is None:
            return None
        assert isinstance(existing, ExternalTensorTrait)
        return existing

    def set(self, to_tensor: torch.Tensor):
        to_tensor._turbine_external_tensor_trait = self