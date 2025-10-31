
from typing import Any, List


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
        self.default_extensions = ['jinja2_time.TimeExtension']
        extensions = self._read_extensions(context or {})
        all_extensions = self.default_extensions + extensions

        try:
            self.extensions = [__import__(ext, fromlist=[''])
                               for ext in all_extensions]
        except ImportError as e:
            raise ImportError(
                f"Failed to load extension(s): {', '.join(all_extensions)}") from e

        super().__init__(**kwargs)

    def _read_extensions(self, context: dict[str, Any]) -> List[str]:
        '''Return list of extensions as str to be passed on to the Jinja2 env.
        If context does not contain the relevant info, return an empty
        list instead.
        '''
        return context.get('_extensions', [])
