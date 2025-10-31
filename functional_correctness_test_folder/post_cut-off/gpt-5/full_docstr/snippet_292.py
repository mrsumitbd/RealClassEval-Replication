from abc import ABC
from typing import Any, Callable, Optional


class BaseHook(ABC):
    '''
    Base class for registering and managing PyTorch forward hooks on model layers.
    This class is used to create specific hook classes, like `ResponseHook` and `ActivationHook`.
    '''

    def __init__(self, layer_key: str, hook_fn: Callable[[Any, Any, Any], Any], agent: Any):
        '''
        :param layer_key: Dotted module path in model.named_modules().
        :type layer_key: str
        :param hook_fn: Callable with signature (module, input, output).
        :type hook_fn: Callable
        :param agent: Owning agent (may be None for generic hooks).
        :type agent: Any
        '''
        if not isinstance(layer_key, str):
            raise TypeError("layer_key must be a string")
        if not callable(hook_fn):
            raise TypeError("hook_fn must be callable")

        self.layer_key: str = layer_key
        self.hook_fn: Callable[[Any, Any, Any], Any] = hook_fn
        self.agent: Any = agent

        self._handle: Optional[Any] = None
        self._model: Optional[Any] = None
        self._module: Optional[Any] = None

    def _hook(self) -> Callable[[Any, Any, Any], Any]:
        '''Placeholder hook (override in subclasses).'''
        def _wrapped(module, inputs, output):
            return self.hook_fn(module, inputs, output)
        return _wrapped

    def register(self, model):
        '''
        Registers the hook on the given model using the layer_key.
        :param model: Model whose layer will be hooked.
        :type model: torch.nn.Module
        :return: The hook handle.
        :rtype: Any
        '''
        if self._handle is not None:
            self.remove()

        target_module = None
        for name, module in model.named_modules():
            if name == self.layer_key:
                target_module = module
                break

        if target_module is None:
            raise KeyError(
                f"Layer '{self.layer_key}' not found in model.named_modules().")

        handle = target_module.register_forward_hook(self._hook())
        self._handle = handle
        self._model = model
        self._module = target_module
        return handle

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
                self._model = None
