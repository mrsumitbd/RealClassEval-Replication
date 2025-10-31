
from typing import Any, Dict, List, Optional


class ExtensionLoaderMixin:

    def __init__(self, *, context: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        self.context = context if context is not None else {}
        super().__init__(**kwargs)

    def _read_extensions(self, context: Dict[str, Any]) -> List[str]:
        extensions = context.get('extensions', [])
        if not isinstance(extensions, list):
            raise ValueError("Extensions must be a list")
        return extensions
