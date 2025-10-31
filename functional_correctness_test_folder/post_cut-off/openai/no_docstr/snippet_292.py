
from abc import ABC
from typing import Any, Callable, Union, List


class BaseHook(ABC):
    """
    A simple hook manager that can attach a forward hook to a specified layer
    of a PyTorch model. The hook function receives the module, its input and
    output, and can optionally interact with an agent object.
    """

    def __init__(self, layer_key: Union[str, int], hook_fn: Callable, agent: Any = None):
        """
        Parameters
        ----------
        layer_key : str | int
            Identifier of the target layer. If a string, it is interpreted as a
            dotted path (e.g., "layer1.0.conv1") relative to the model. If an
            integer, it is interpreted as the index in the model's ``children()``
            sequence.
        hook_fn : Callable
            Function to be called when the hook is triggered. It should accept
            three arguments: (module, input, output). It may also use the
            ``agent`` attribute if needed.
        agent : Any, optional
            An arbitrary object that can be used inside the hook function.
        """
        self.layer_key = layer_key
        self.hook_fn = hook_fn
        self.agent = agent
        self._handle = None
        self._module = None

    def _hook(self, module, input, output):
        """
        Internal wrapper that forwards the call to the user-provided hook function.
        """
        # The hook function may modify the output; we return whatever it returns.
        return self.hook_fn(module, input, output)

    def _get_module(self, model):
        """
        Resolve the target module from the model based on ``layer_key``.
        """
        if isinstance(self.layer_key, str):
            parts = self.layer_key.split(".")
            mod = model
            for part in parts:
                if part.isdigit():
                    idx = int(part)
                    mod = list(mod.children())[idx]
                else:
                    mod = getattr(mod, part)
            return mod
        elif isinstance(self.layer_key, int):
            return list(model.children())[self.layer_key]
        else:
            raise TypeError(
                f"Unsupported layer_key type: {type(self.layer_key)}")

    def register(self, model):
        """
        Register the hook on the specified layer of the model.
        """
        if self._handle is not None:
            raise RuntimeError("Hook is already registered.")
        self._module = self._get_module(model)
        self._handle = self._module.register_forward_hook(self._hook)

    def remove(self):
        """
        Remove the previously registered hook.
        """
        if self._handle is not None:
            self._handle.remove()
            self._handle = None
            self._module = None
