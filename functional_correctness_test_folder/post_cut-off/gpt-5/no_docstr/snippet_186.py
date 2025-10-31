from __future__ import annotations

import importlib
from typing import Any, Type


class UnifiedAuthFactory:
    @staticmethod
    def _load_class(class_path: str) -> Type[Any]:
        if ":" in class_path:
            module_path, class_name = class_path.split(":", 1)
        else:
            parts = class_path.rsplit(".", 1)
            if len(parts) != 2:
                raise ValueError(
                    f"Invalid provider path '{class_path}'. Expected 'module:Class' or 'module.Class'."
                )
            module_path, class_name = parts
        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError as e:
            raise ValueError(
                f"Could not import module '{module_path}' for provider '{class_path}'.") from e
        try:
            cls = getattr(module, class_name)
        except AttributeError as e:
            raise ValueError(
                f"Module '{module_path}' does not define '{class_name}'.") from e
        if not isinstance(cls, type):
            raise ValueError(
                f"Resolved object '{class_name}' from '{module_path}' is not a class.")
        return cls

    @staticmethod
    def _instantiate(class_or_callable: Any, kwargs: dict) -> Any:
        try:
            return class_or_callable(**kwargs)
        except TypeError:
            # Some providers may use alternate constructors like .from_env or .from_settings
            for alt in ("from_env", "from_settings", "create", "build"):
                factory = getattr(class_or_callable, alt, None)
                if callable(factory):
                    return factory(**kwargs)
            raise

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> "ModelAuthProvider":
        # If a class is explicitly provided, prefer it.
        cls = kwargs.pop("cls", None)
        if isinstance(cls, type):
            return UnifiedAuthFactory._instantiate(cls, kwargs)

        # If a callable factory is provided, use it.
        factory = kwargs.pop("factory", None)
        if callable(factory):
            return factory(**kwargs)

        # Otherwise, resolve from a fully-qualified class path.
        resolved_cls = UnifiedAuthFactory._load_class(provider)
        return UnifiedAuthFactory._instantiate(resolved_cls, kwargs)

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> "StorageAuthProvider":
        cls = kwargs.pop("cls", None)
        if isinstance(cls, type):
            return UnifiedAuthFactory._instantiate(cls, kwargs)

        factory = kwargs.pop("factory", None)
        if callable(factory):
            return factory(**kwargs)

        resolved_cls = UnifiedAuthFactory._load_class(provider)
        return UnifiedAuthFactory._instantiate(resolved_cls, kwargs)
