from dataclasses import dataclass
from typing import Optional
import torch

@dataclass
class DeviceTensorTrait:
    """Represents a 'trait' that can be applied to a Tensor to signal that
    it is to be loaded to a speific device at execution time.
    """
    ordinal: int
    queues: Optional[list] = None

    @staticmethod
    def get(from_tensor: torch.Tensor) -> Optional['DeviceTensorTrait']:
        existing = getattr(from_tensor, '_turbine_device_tensor_trait', None)
        if existing is None:
            return None
        assert isinstance(existing, DeviceTensorTrait)
        return existing

    def set(self, to_tensor: torch.Tensor):
        to_tensor._turbine_device_tensor_trait = self