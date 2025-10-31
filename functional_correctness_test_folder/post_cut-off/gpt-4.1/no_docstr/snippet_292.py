
from abc import ABC


class BaseHook(ABC):

    def __init__(self, layer_key, hook_fn, agent):
        self.layer_key = layer_key
        self.hook_fn = hook_fn
        self.agent = agent
        self.hook_handle = None
        self.layer = None

    def _hook(self):
        # This method is intended to be used as the hook function for the layer.
        def wrapper(module, input, output):
            return self.hook_fn(module, input, output, self.agent)
        return wrapper

    def register(self, model):
        # Find the layer in the model using the layer_key
        # layer_key can be a string representing the attribute path
        keys = self.layer_key.split('.')
        layer = model
        for key in keys:
            layer = getattr(layer, key)
        self.layer = layer
        self.hook_handle = self.layer.register_forward_hook(self._hook())

    def remove(self):
        if self.hook_handle is not None:
            self.hook_handle.remove()
            self.hook_handle = None
