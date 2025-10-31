
from typing import Any


class ExtensionLoaderMixin:

    def __init__(self, *, context: dict[str, Any] | None = None, **kwargs: Any) -> None:
        self.context = context if context is not None else {}
        self.extensions = self._read_extensions(self.context)

    def _read_extensions(self, context: dict[str, Any]) -> list[str]:
        extensions = context.get('extensions', [])
        if not isinstance(extensions, list):
            raise ValueError("Extensions must be a list")
        return [str(ext) for ext in extensions]
