from __future__ import annotations

import importlib
from typing import Any


class ExtensionLoaderMixin:
    '''Mixin providing sane loading of extensions specified in a given context.
    The context is being extracted from the keyword arguments before calling
    the next parent class in line of the child.
        '''

    def __init__(self, *, context: dict[str, Any] | None = None, **kwargs: Any) -> None:
        '''Initialize the Jinja2 Environment object while loading extensions.
        Does the following:
        1. Establishes default_extensions (currently just a Time feature)
        2. Reads extensions set in the cookiecutter.json _extensions key.
        3. Attempts to load the extensions. Provides useful error if fails.
        '''
        # default extensions
        default_extensions: list[str] = ['jinja2_time.TimeExtension']

        # pop possible stray context from kwargs to avoid passing it upstream
        kwargs.pop('context', None)

        # read additional extensions from context
        ctx = context or {}
        ctx_extensions = self._read_extensions(ctx)

        # combine, de-duplicate while preserving order
        combined: list[str] = []
        seen: set[str] = set()
        for ext in (*default_extensions, *ctx_extensions):
            if ext not in seen:
                seen.add(ext)
                combined.append(ext)

        # Validate that extensions can be imported, but keep passing strings to super
        for ext in combined:
            try:
                self._ensure_importable(ext)
            except Exception as exc:  # provide a helpful error message
                raise RuntimeError(
                    f"Failed loading Jinja2 extension '{ext}'. "
                    "Ensure it is installed and the import path is correct."
                ) from exc

        # hand off to the next class in MRO with extensions set
        super().__init__(extensions=combined, **kwargs)

    def _read_extensions(self, context: dict[str, Any]) -> list[str]:
        '''Return list of extensions as str to be passed on to the Jinja2 env.
        If context does not contain the relevant info, return an empty
        list instead.
        '''
        raw = context.get('_extensions', [])
        if raw is None:
            return []
        if isinstance(raw, str):
            return [raw] if raw else []
        if isinstance(raw, (list, tuple)):
            result: list[str] = []
            for item in raw:
                if not item:
                    continue
                if not isinstance(item, str):
                    raise TypeError(
                        f"Invalid extension entry {item!r} of type {type(item).__name__}; expected str."
                    )
                result.append(item)
            return result
        raise TypeError(
            f"Invalid _extensions value of type {type(raw).__name__}; expected str or list/tuple of str."
        )

    @staticmethod
    def _ensure_importable(path: str) -> None:
        # Accept paths like "pkg.mod:Class" or "pkg.mod.Class"
        module_name: str
        attr_name: str | None = None

        if ':' in path:
            module_name, attr_name = path.split(':', 1)
        elif '.' in path:
            # Try to split on last dot to separate module and attribute/class
            parts = path.rsplit('.', 1)
            if len(parts) == 2:
                module_name, attr_name = parts
            else:
                module_name = path
                attr_name = None
        else:
            # simple module import
            module_name = path

        module = importlib.import_module(module_name)
        if attr_name:
            # attribute may be a class symbol; ensure it exists
            getattr(module, attr_name)  # will raise AttributeError if missing
