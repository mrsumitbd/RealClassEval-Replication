
from abc import ABC
from typing import Any, Callable, Optional


class BaseHook(ABC):
    '''
    Base class for registering and managing PyTorch forward hooks on model layers.
    This class is used to create specific hook classes, like `ResponseHook` and `ActivationHook`.
    '''

    def __init__(self, layer_key: str, hook_fn: Callable, agent: Any):
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
        self._handle: Optional[Any] = None
        self._module: Optional[Any] = None

    def _hook(self, module, input, output):
        '''Placeholder hook (override in subclasses).'''
        # Subclasses may override this method to provide custom behavior.
        # The base implementation simply forwards to the provided hook_fn.
        if self.hook_fn is not None:
            return self.hook_fn(module, input, output)

    def register(self, model: Any) -> Any:
        '''
        Registers the hook on the given model using the layer_key.
        :param model: Model whose layer will be hooked.
        :type model: torch.nn.Module
        :return: The hook handle.
        :rtype: Any
        '''
        # Find the target module by its dotted name.
        target_module = None
        for name, module in model.named_modules():
            if name == self.layer_key:
                target_module = module
                break
        if target_module is None:
            raise ValueError(
                f"Layer key '{self.layer_key}' not found in the model.")

        # Register the forward hook and store the handle.
        self._module = target_module
        self._handle = target_module.register_forward_hook(self._hook)
        return self._handle

    def remove(self) -> None:
        '''
        Removes the hook if it is registered.
        '''
        if self._handle is not None:
            try:
                # PyTorch hook handles expose a remove() method.
                self._handle.remove()
            except AttributeError:
                # Fallback: some older hook handles may be callable.
                try:
                    self._handle()
                except Exception:
                    pass
            finally:
                self._handle = None
                self._module = None
