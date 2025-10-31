import torch
import io
import pickle

class _TorchLoadUnpickler(pickle.Unpickler):
    """
    Subclass of pickle.Unpickler that intercepts 'torch.storage._load_from_bytes' calls
    and uses `torch.load(..., map_location=..., torch_load_kwargs=...)`.

    This way, we can use normal pickle when unpickling a skorch net but still benefit
    from torch.load to handle the map_location. Note that `with torch.device(...)` does
    not work for unpickling.

    """

    def __init__(self, *args, map_location, torch_load_kwargs, **kwargs):
        super().__init__(*args, **kwargs)
        self.map_location = map_location
        self.torch_load_kwargs = torch_load_kwargs

    def find_class(self, module, name):
        if module == 'torch.storage' and name == '_load_from_bytes':

            def _load_from_bytes(b):
                return torch.load(io.BytesIO(b), map_location=self.map_location, **self.torch_load_kwargs)
            return _load_from_bytes
        return super().find_class(module, name)