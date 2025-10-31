
from abc import ABC


class BaseHook(ABC):

    def __init__(self, layer_key, hook_fn, agent):

        self.layer_key = layer_key
        self.hook_fn = hook_fn
        self.agent = agent
        self.hook_handle = None

    def _hook(self):

        self.hook_fn(self.agent)

    def register(self, model):

        layer = model
        for key in self.layer_key.split('.'):
            layer = getattr(layer, key)
        self.hook_handle = layer.register_forward_hook(self._hook)

    def remove(self):

        if self.hook_handle is not None:
            self.hook_handle.remove()
            self.hook_handle = None
