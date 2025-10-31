from abc import ABC
from typing import Any, Callable, Optional

try:
    import torch
    from torch.nn import Module
except Exception:  # Allow import even if torch isn't available at import time
    Module = Any  # type: ignore


class BaseHook(ABC):
    '''
    Base class for registering and managing PyTorch forward hooks on model layers.
    This class is used to create specific hook classes, like `ResponseHook` and `ActivationHook`.
    '''

    def __init__(self, layer_key: str, hook_fn: Optional[Callable], agent: Any):
        '''
        :param layer_key: Dotted module path in model.named_modules().
        :type layer_key: str
        :param hook_fn: Callable with signature (module, input, output).
        :type hook_fn: Callable
        :param agent: Owning agent (may be None for generic hooks).
        :type agent: Any
        '''
        self.layer_key: str = layer_key
        self.hook_fn: Optional[Callable] = hook_fn
        self.agent: Any = agent

        self._handle: Any = None
        self._module: Optional[Module] = None

    def _hook(self):
        '''Placeholder hook (override in subclasses).'''
        raise NotImplementedError(
            "Subclasses must override _hook() or provide hook_fn in __init__.")

    def register(self, model: Module):
        '''
        Registers the hook on the given model using the layer_key.
        :param model: Model whose layer will be hooked.
        :type model: torch.nn.Module
        :return: The hook handle.
        :rtype: Any
        '''
        if model is None:
            raise ValueError("model must not be None.")

        target_module: Optional[Module] = None

        if self.layer_key in (None, "", "."):
            target_module = model
        else:
            # Find the target module by name
            for name, module in model.named_modules():
                if name == self.layer_key:
                    target_module = module
                    break

        if target_module is None:
            raise KeyError(
                f"Layer '{self.layer_key}' not found in model.named_modules().")

        final_hook: Callable
        if callable(self.hook_fn):
            # expects signature (module, input, output)
            final_hook = self.hook_fn
        else:
            candidate = self._hook()
            if not callable(candidate):
                raise TypeError(
                    "_hook() must return a callable with signature (module, input, output).")
            final_hook = candidate

        self._module = target_module
        self._handle = target_module.register_forward_hook(final_hook)
        return self._handle

    def remove(self):
        if self._handle is not None:
            try:
                self._handle.remove()
            finally:
                self._handle = None
                self._module = None
