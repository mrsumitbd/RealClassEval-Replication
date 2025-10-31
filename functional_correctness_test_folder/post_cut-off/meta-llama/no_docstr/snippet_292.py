
from abc import ABC
import torch


class BaseHook(ABC):
    """
    Base class for hooks.
    """

    def __init__(self, layer_key, hook_fn, agent):
        """
        Initialize the hook.

        Args:
        - layer_key (str): The key of the layer to hook.
        - hook_fn (function): The function to be called when the hook is triggered.
        - agent (object): The agent that is using this hook.
        """
        self.layer_key = layer_key
        self.hook_fn = hook_fn
        self.agent = agent
        self.hook_handle = None

    def _hook(self, module, input, output):
        """
        The actual hook function that will be registered.

        Args:
        - module (torch.nn.Module): The module that the hook is registered to.
        - input (tuple): The input to the module.
        - output (torch.Tensor): The output of the module.
        """
        self.hook_fn(module, input, output, self.agent)

    def register(self, model):
        """
        Register the hook to the given model.

        Args:
        - model (torch.nn.Module): The model to register the hook to.
        """
        module = dict(model.named_modules())[self.layer_key]
        self.hook_handle = module.register_forward_hook(self._hook)

    def remove(self):
        """
        Remove the hook.
        """
        if self.hook_handle is not None:
            self.hook_handle.remove()
            self.hook_handle = None
