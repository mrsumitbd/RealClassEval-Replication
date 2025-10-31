
from __future__ import annotations

from typing import Any, Dict, List


class ExtensionLoaderMixin:
    '''Mixin providing sane loading of extensions specified in a given context.
    The context is being extracted from the keyword arguments before calling
    the next parent class in line of the child.
    '''

    def __init__(self, *, context: Dict[str, Any] | None = None, **kwargs: Any) -> None:
        '''Initialize the Jinja2 Environment object while loading extensions.
        Does the following:
        1. Establishes default_extensions (currently just a Time feature)
        2. Reads extensions set in the cookiecutter.json _extensions key.
        3. Attempts to load the extensions. Provides useful error if fails.
        '''
        if context is None:
            context = {}

        # 1. Default extensions (placeholder for a Time feature)
        default_extensions: List[str] = []

        # 2. Read extensions from context
        extensions = self._read_extensions(context)

        # 3. Combine and attempt to load extensions
        all_extensions = default_extensions + extensions
        loaded_extensions: List[str] = []

        for ext in all_extensions:
            try:
                # Import the extension module to ensure it is available
                __import__(ext, fromlist=[''])
                loaded_extensions.append(ext)
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to load extension '{ext}': {exc}") from exc

        # Pass the loaded extensions to the next parent class
        kwargs.setdefault('extensions', loaded_extensions)
        super().__init__(**kwargs)

    def _read_extensions(self, context: Dict[str, Any]) -> List[str]:
        '''Return list of extensions as str to be passed on to the Jinja2 env.
        If context does not contain the relevant info, return an empty
        list instead.
        '''
        ext = context.get('_extensions')
        if isinstance(ext, list) and all(isinstance(e, str) for e in ext):
            return ext
        return []
