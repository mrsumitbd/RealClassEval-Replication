from typing import Any
import importlib


class ClassWithInitArgs:
    '''
    Wrapper class that stores constructor arguments for deferred instantiation.
    This class is particularly useful for remote class instantiation where
    the actual construction needs to happen at a different time or location.
    '''

    def __init__(self, cls, *args, **kwargs) -> None:
        '''Initialize the ClassWithInitArgs instance.
        Args:
            cls: The class to be instantiated later
            *args: Positional arguments for the class constructor
            **kwargs: Keyword arguments for the class constructor
        '''
        if not callable(cls) and not isinstance(cls, str):
            raise TypeError(
                "cls must be a class/callable or an import path string")
        self._cls = cls if callable(cls) else None
        self._cls_path = cls if isinstance(cls, str) else None
        self._args = args
        self._kwargs = kwargs

    def _resolve_class(self):
        if self._cls is not None:
            return self._cls

        path = self._cls_path
        if not isinstance(path, str) or not path:
            raise ValueError("Invalid class path for resolution")

        if ":" in path:
            module_path, qualname = path.split(":", 1)
        else:
            module_path, sep, qualname = path.rpartition(".")
            if not sep:
                raise ValueError(
                    "Invalid class path. Expected 'module.submodule:Class' or 'module.submodule.Class'"
                )

        module = importlib.import_module(module_path)
        obj = module
        for part in qualname.split("."):
            obj = getattr(obj, part)

        if not callable(obj):
            raise TypeError(
                f"Resolved object {obj!r} from '{path}' is not callable")
        self._cls = obj
        return obj

    def __call__(self) -> Any:
        '''Instantiate the stored class with the stored arguments.'''
        cls_obj = self._resolve_class()
        return cls_obj(*self._args, **self._kwargs)
