from abc import ABC
import re
import weakref
from collections.abc import Iterable

try:
    import torch.nn as nn  # noqa: F401
except Exception:  # pragma: no cover
    nn = None


class BaseHook(ABC):
    def __init__(self, layer_key, hook_fn, agent):
        self.layer_key = layer_key
        self.hook_fn = hook_fn
        self.agent = agent
        self._handles = []
        self._model_ref = None
        self._registered = False

    def _hook(self):
        def _wrapped(module, inputs, output):
            return self.hook_fn(module, inputs, output, self.agent)
        return _wrapped

    def register(self, model):
        if self._registered:
            return
        if not hasattr(model, "named_modules"):
            raise TypeError(
                "Model must be a torch.nn.Module or expose named_modules().")

        self._model_ref = weakref.ref(model)
        hook = self._hook()

        keys = self.layer_key
        if keys is None:
            keys = [None]

        if isinstance(keys, Iterable) and not isinstance(keys, (str, bytes)):
            key_list = list(keys)
        else:
            key_list = [keys]

        patterns = []
        for k in key_list:
            if k is None:
                patterns.append(("all", None))
            elif callable(k):
                patterns.append(("callable", k))
            elif isinstance(k, re.Pattern):
                patterns.append(("regex", k))
            elif isinstance(k, str):
                patterns.append(("string", k))
            else:
                raise TypeError(
                    f"Unsupported layer_key element type: {type(k)}")

        for name, module in model.named_modules():
            match = False
            for kind, spec in patterns:
                if kind == "all":
                    match = True
                elif kind == "callable":
                    try:
                        match = bool(spec(name, module))
                    except Exception:
                        match = False
                elif kind == "regex":
                    match = spec.search(name) is not None
                elif kind == "string":
                    match = name == spec or spec in name
                if match:
                    break

            if match and hasattr(module, "register_forward_hook"):
                handle = module.register_forward_hook(hook)
                self._handles.append(handle)

        self._registered = True

    def remove(self):
        for h in self._handles:
            try:
                h.remove()
            except Exception:
                pass
        self._handles.clear()
        self._registered = False
        self._model_ref = None
