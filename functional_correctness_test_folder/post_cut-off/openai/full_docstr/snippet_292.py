
from abc import ABC
from typing import Any, Callable

import torch.nn as nn


class BaseHook(ABC):
    '''
    Base class for registering and managing PyTorch forward hooks on model layers.
    This class is used to create specific hook classes, like `ResponseHook` and `ActivationHook`.
    '''

    def __init__(self, layer_key: str, hook_fn: Callable, agent: Any = None):
        '''
        :param layer_key: Dotted module path in model.named_modules().
        :type layer_key: str
        :param hook_fn: Callable with signature (module, input, output).
        :type hook_fn: Callable
        :param agent: Owning agent (may be None for generic hooks).
        :type agent: Any
        '''
        self.layer_key = layer_key
        self.hook_fn = hook_fn
        self.agent = agent
        self._handle: Any = None
        self._module: nn.Module | None = None

    def _hook(self, module: nn.Module, input: Any, output: Any):
        '''Placeholder hook (override in subclasses).'''
        # Default implementation simply forwards to the provided hook function.
        return self.hook_fn(module, input, output)

    def register(self, model: nn.Module) -> Any:
        '''
        Registers the hook on the given model using the layer_key.
        :param model: Model whose layer will be hooked.
        :type model: torch.nn.Module
        :return: The hook handle.
        :rtype: Any
        '''
        # Find the target module by its dotted name.
        for name, mod in model.named_modules():
            if name == self.layer_key:
                self._module = mod
                break
        else:
            raise ValueError(
                f"Layer key '{self.layer_key}' not found in the model.")

        # Register the forward hook.
        self._handle = self._module.register_forward_hook(self._hook)
        return self._handle

    def remove(self):
        '''
        Removes the hook if it is registered.
        '''
        if self._handle is not None:
            try:
                self._handle.remove()
            finally:
                self._handle = None
                self._module = None
