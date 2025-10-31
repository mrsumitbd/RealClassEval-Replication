
from abc import ABC, abstractmethod


class BaseHook(ABC):

    def __init__(self, layer_key, hook_fn, agent):
        self.layer_key = layer_key
        self.hook_fn = hook_fn
        self.agent = agent
        self.hook = None

    @abstractmethod
    def _hook(self):
        pass

    def register(self, model):
        if hasattr(model, self.layer_key):
            layer = getattr(model, self.layer_key)
            self.hook = layer.register_forward_hook(self.hook_fn)
        else:
            raise AttributeError(
                f"Model does not have the attribute {self.layer_key}")

    def remove(self):
        if self.hook is not None:
            self.hook.remove()
            self.hook = None
