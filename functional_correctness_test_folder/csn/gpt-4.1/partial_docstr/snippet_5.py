
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
        default_extensions = ['jinja2_time.TimeExtension']
        context = context or {}
        extensions = default_extensions + self._read_extensions(context)
        try:
            kwargs['extensions'] = extensions
            super().__init__(**kwargs)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load Jinja2 extensions: {extensions}. Error: {e}"
            ) from e

    def _read_extensions(self, context: dict[str, Any]) -> list[str]:
        '''Return list of extensions as str to be passed on to the Jinja2 env.
        If context does not contain the relevant info, return an empty
        list instead.
        '''
        exts = context.get('_extensions')
        if isinstance(exts, list) and all(isinstance(e, str) for e in exts):
            return exts
        return []
