from typing_extensions import override
import pickle

class UnpicklerWrapper(pickle.Unpickler):

    @override
    def find_class(self, mod_name, name):

        class DummyClass:

            def __init__(self, *args, **kwargs):
                pass
        if mod_name.startswith('megatron') or mod_name.startswith('glm'):
            return DummyClass
        return super().find_class(mod_name, name)