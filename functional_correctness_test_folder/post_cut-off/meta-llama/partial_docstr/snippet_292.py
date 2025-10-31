
from abc import ABC
import torch


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
        self.hook_handle = None

    def _hook(self, module, input, output):
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
        module = dict(model.named_modules())[self.layer_key]
        self.hook_handle = module.register_forward_hook(self._hook)
        return self.hook_handle

    def remove(self):
        if self.hook_handle is not None:
            self.hook_handle.remove()
            self.hook_handle = None
