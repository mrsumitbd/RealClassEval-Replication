
from typing import Any


class ExtensionLoaderMixin:

    def __init__(self, *, context: dict[str, Any] | None = None, **kwargs: Any) -> None:
        self.context = context if context is not None else {}
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _read_extensions(self, context: dict[str, Any]) -> list[str]:
        extensions = context.get("extensions")
        if isinstance(extensions, list) and all(isinstance(ext, str) for ext in extensions):
            return extensions
        return []
