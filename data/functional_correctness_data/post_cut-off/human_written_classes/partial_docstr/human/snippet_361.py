import torch
from typing import Any, Optional

class OffloadHandler:
    """A base class for CPU offload-handler."""

    def __init__(self) -> None:
        pass

    def tensor_push(self, tensor: torch.Tensor, **kwargs) -> Any:
        """Tensor push."""
        raise NotImplementedError('`tensor_push is not implented in OffloadHandler class. Inherit this class and implement your custom tensor_push.')

    def tensor_pop(self, tensor_tag: Any, **kwargs):
        """Tensor pop."""
        raise NotImplementedError('`tensor_pop is not implented in OffloadHandler class. Inherit this class and implement your custom tensor_pop.')