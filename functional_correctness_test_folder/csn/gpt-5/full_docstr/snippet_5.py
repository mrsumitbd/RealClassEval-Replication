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
        default_extensions: list[str] = ["jinja2_time.TimeExtension"]

        ctx_extensions = self._read_extensions(context or {})

        existing = kwargs.get("extensions", [])
        if existing is None:
            existing = []
        if not isinstance(existing, (list, tuple)):
            raise TypeError(
                "extensions must be a list or tuple if provided in kwargs")

        combined: list[str] = []
        for ext in list(default_extensions) + list(ctx_extensions) + list(existing):
            if isinstance(ext, str):
                if ext not in combined:
                    combined.append(ext)
            else:
                raise TypeError(
                    f"Extension identifiers must be strings, got {type(ext).__name__}")

        load_errors: list[str] = []
        for ext in combined:
            try:
                module_name, _, attr = ext.rpartition(".")
                if not module_name or not attr:
                    raise ImportError(
                        f"Invalid extension path '{ext}'. Expected 'package.module.ClassName'.")
                module = importlib.import_module(module_name)
                getattr(module, attr)
            except Exception as exc:
                load_errors.append(f"{ext}: {exc}")

        if load_errors:
            msg = "Could not load Jinja2 extensions:\n- " + \
                "\n- ".join(load_errors)
            raise RuntimeError(msg)

        kwargs["extensions"] = combined
        super().__init__(**kwargs)

    def _read_extensions(self, context: dict[str, Any]) -> list[str]:
        '''Return list of extensions as str to be passed on to the Jinja2 env.
        If context does not contain the relevant info, return an empty
        list instead.
        '''
        # Try at top-level
        value = context.get("_extensions")
        # Or nested under 'cookiecutter' key (common in Cookiecutter context)
        if value is None and isinstance(context.get("cookiecutter"), dict):
            value = context["cookiecutter"].get("_extensions")

        if value is None:
            return []

        if isinstance(value, (list, tuple)):
            result: list[str] = []
            for item in value:
                if isinstance(item, str):
                    result.append(item)
                else:
                    # Coerce to string representation to avoid crashing on non-strings
                    result.append(str(item))
            return result

        # If malformed, ignore and return empty to be lenient
        return []
