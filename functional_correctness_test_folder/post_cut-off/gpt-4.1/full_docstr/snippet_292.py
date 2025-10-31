
from abc import ABC, abstractmethod


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
        self.layer_key = layer_key
        self.hook_fn = hook_fn
        self.agent = agent
        self.handle = None
        self._registered_module = None

    def _hook(self):
        '''Placeholder hook (override in subclasses).'''
        return self.hook_fn

    def register(self, model):
        '''
        Registers the hook on the given model using the layer_key.
        :param model: Model whose layer will be hooked.
        :type model: torch.nn.Module
        :return: The hook handle.
        :rtype: Any
        '''
        module = dict(model.named_modules()).get(self.layer_key, None)
        if module is None:
            raise ValueError(
                f"Module with key '{self.layer_key}' not found in model.named_modules().")
        self._registered_module = module
        self.handle = module.register_forward_hook(self._hook())
        return self.handle

    def remove(self):
        '''
        Removes the hook if it is registered.
        '''
        if self.handle is not None:
            self.handle.remove()
            self.handle = None
            self._registered_module = None
