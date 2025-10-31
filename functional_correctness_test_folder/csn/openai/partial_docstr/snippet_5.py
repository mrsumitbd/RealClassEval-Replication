
from __future__ import annotations

from typing import Any, Dict, List, Optional

import jinja2


class ExtensionLoaderMixin:
    """Mixin providing sane loading of extensions specified in a given context.

    The context is being extracted from the keyword arguments before calling
    the next parent class in line of the child.
    """

    def __init__(
        self,
        *,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Jinja2 Environment object while loading extensions.

        Does the following:
        1. Establishes default_extensions (currently just a Time feature)
        2. Reads extensions set in the cookiecutter.json _extensions key.
        3. Attempts to load the extensions. Provides useful error if fails.
        """
        # Ensure context is a dict
        ctx: Dict[str, Any] = context or {}

        # Default extensions
        default_extensions: List[str] = ["jinja2_time.TimeExtension"]

        # Read extensions from context
        user_extensions = self._read_extensions(ctx)

        # Combine extensions
        extensions = list(dict.fromkeys(default_extensions + user_extensions))

        # Attempt to initialize the parent (e.g., jinja2.Environment)
        try:
            super().__init__(extensions=extensions, **kwargs)  # type: ignore
        except Exception as exc:
            # Provide a helpful error message
            raise RuntimeError(
                f"Failed to load Jinja2 extensions: {', '.join(extensions)}"
            ) from exc

    def _read_extensions(self, context: Dict[str, Any]) -> List[str]:
        """
        Return list of extensions as str to be passed on to the Jinja2 env.
        If context does not contain the relevant info, return an empty list instead.
        """
        extensions = context.get("_extensions")
        if isinstance(extensions, list):
            # Ensure all items are strings
            return [str(ext) for ext in extensions if isinstance(ext, (str, bytes))]
        return []
