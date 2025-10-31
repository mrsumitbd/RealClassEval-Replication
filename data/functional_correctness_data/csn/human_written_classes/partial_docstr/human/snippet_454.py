from pathlib import PurePath

class RealPathlibPathModule:
    """Patches `pathlib.Path` by passing all calls to RealPathlibModule."""
    real_pathlib = None

    @classmethod
    def __instancecheck__(cls, instance):
        return isinstance(instance, PurePath)

    def __init__(self):
        if self.real_pathlib is None:
            self.__class__.real_pathlib = RealPathlibModule()

    def __call__(self, *args, **kwargs):
        return RealPath(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.real_pathlib.Path, name)