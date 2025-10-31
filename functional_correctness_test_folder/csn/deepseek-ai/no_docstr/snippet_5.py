
from typing import Any, Dict, List


class ExtensionLoaderMixin:

    def __init__(self, *, context: Dict[str, Any] | None = None, **kwargs: Any) -> None:
        self.context = context if context is not None else {}
        self.kwargs = kwargs

    def _read_extensions(self, context: Dict[str, Any]) -> List[str]:
        return []
