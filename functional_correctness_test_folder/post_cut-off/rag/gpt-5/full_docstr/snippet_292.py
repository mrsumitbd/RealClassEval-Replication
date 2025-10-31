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
        self.layer_key: str = layer_key
        self.hook_fn: Optional[Callable[[Any, Any, Any], Any]] = hook_fn
        self.agent: Any = agent
        self._handle: Optional[Any] = None
        self._module: Optional[Any] = None

    def _hook(self, module, inputs, output):
        '''Placeholder hook (override in subclasses).'''
        if self.hook_fn is not None:
            return self.hook_fn(module, inputs, output)
        return None

    def _resolve_module_from_key(self, model: Any, key: str) -> Optional[Any]:
        # First, try exact match from named_modules
        try:
            modules = dict(model.named_modules())
        except Exception:
            modules = {}
        if key in modules:
            return modules[key]

        # Try DataParallel/DistributedDataParallel style prefix handling
        if hasattr(model, "module"):
            # Build named_modules for the inner module too
            try:
                inner_modules = dict(model.module.named_modules())
            except Exception:
                inner_modules = {}
            if key in inner_modules:
                return inner_modules[key]
            prefixed = f"module.{key}"
            if prefixed in modules:
                return modules[prefixed]
            if prefixed in inner_modules:
                return inner_modules[prefixed]

        # Try attribute traversal on model
        try:
            obj = model
            for part in key.split("."):
                obj = getattr(obj, part)
            return obj
        except Exception:
            pass

        # Try attribute traversal on model.module
        if hasattr(model, "module"):
            try:
                obj = model.module
                for part in key.split("."):
                    obj = getattr(obj, part)
                return obj
            except Exception:
                pass

        return None

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

        module = self._resolve_module_from_key(model, self.layer_key)
        if module is None:
            raise KeyError(
                f'Layer "{self.layer_key}" not found in model.named_modules().')

        def wrapper(mod, inputs, output):
            return self._hook(mod, inputs, output)

        handle = module.register_forward_hook(wrapper)
        self._handle = handle
        self._module = module
        return handle

    def remove(self):
        '''
        Removes the hook if it is registered.
        '''
        handle = self._handle
        if handle is not None:
            try:
                handle.remove()
            finally:
                self._handle = None
                self._module = None
