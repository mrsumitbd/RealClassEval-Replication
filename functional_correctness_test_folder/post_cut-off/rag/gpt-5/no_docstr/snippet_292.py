from abc import ABC
from typing import Any, Callable, Optional
import inspect


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
        self.layer_key: str = layer_key
        self.hook_fn: Optional[Callable] = hook_fn
        self.agent: Any = agent
        self.handle: Any = None
        self.module: Any = None

    def _hook(self):
        '''Placeholder hook (override in subclasses).'''
        pass

    def register(self, model):
        '''
        Registers the hook on the given model using the layer_key.
        :param model: Model whose layer will be hooked.
        :type model: torch.nn.Module
        :return: The hook handle.
        :rtype: Any
        '''
        if self.handle is not None:
            self.remove()

        modules = dict(model.named_modules())
        if self.layer_key not in modules:
            raise KeyError(
                f'Layer "{self.layer_key}" not found in model.named_modules().')
        self.module = modules[self.layer_key]

        if self.hook_fn is not None:
            callback = self.hook_fn
        else:
            def callback(module, input, output):
                sig = inspect.signature(self._hook)
                params = list(sig.parameters.values())
                # Count required positional parameters (bound method excludes 'self')
                required_pos = [p for p in params if p.kind in (
                    p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD) and p.default is p.empty]
                args = (module, input, output)
                if any(p.kind == p.VAR_POSITIONAL for p in params):
                    return self._hook(*args)
                n = min(len(required_pos), 3)
                return self._hook(*args[:n])

        self.handle = self.module.register_forward_hook(callback)
        return self.handle

    def remove(self):
        '''
        Removes the hook if it is registered.
        '''
        if self.handle is not None:
            try:
                self.handle.remove()
            finally:
                self.handle = None
                self.module = None
