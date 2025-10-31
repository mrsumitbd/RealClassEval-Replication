from abc import ABC
from typing import Any, Callable, Optional


class BaseHook(ABC):
    '''
    Base class for registering and managing PyTorch forward hooks on model layers.
    This class is used to create specific hook classes, like `ResponseHook` and `ActivationHook`.
    '''

    def __init__(self, layer_key, hook_fn, agent):
        '''
        :param layer_key: Dotted module path in model.named_modules().
        :type layer_key: str
        :param hook_fn: Callable with signature (module, input, output).
        :type hook_fn: Callable
        :param agent: Owning agent (may be None for generic hooks).
        :type agent: Any
        '''
        if not isinstance(layer_key, str) or not layer_key and layer_key != '':
            raise ValueError(
                'layer_key must be a string (may be empty string for the root module)')
        if hook_fn is None or not callable(hook_fn):
            raise ValueError(
                'hook_fn must be a callable with signature (module, input, output)')
        self.layer_key: str = layer_key
        self.hook_fn: Callable = hook_fn
        self.agent: Any = agent
        self._handle: Optional[Any] = None
        self._model: Optional[Any] = None
        self._module: Optional[Any] = None

    def _hook(self):
        '''Placeholder hook (override in subclasses).'''
        if self.hook_fn is None:
            raise NotImplementedError('No hook function provided.')

        def _fn(module, input, output):
            return self.hook_fn(module, input, output)
        return _fn

    def register(self, model):
        '''
        Registers the hook on the given model using the layer_key.
        :param model: Model whose layer will be hooked.
        :type model: torch.nn.Module
        :return: The hook handle.
        :rtype: Any
        '''
        if model is None:
            raise ValueError('model must not be None')
        # If already registered, remove existing hook before re-registering
        if self._handle is not None:
            self.remove()

        modules = dict(model.named_modules())
        if self.layer_key not in modules:
            raise KeyError(
                f"Layer '{self.layer_key}' not found in model.named_modules().")
        target = modules[self.layer_key]

        hook_callable = self._hook()
        handle = target.register_forward_hook(hook_callable)

        self._handle = handle
        self._model = model
        self._module = target
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
                self._model = None
                self._module = None
