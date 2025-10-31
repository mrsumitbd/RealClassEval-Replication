
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
        # 1. Default extensions
        default_extensions = ['jinja2_time.TimeExtension']

        # 2. Read extensions from context
        context = context or {}
        user_extensions = self._read_extensions(context)

        # 3. Combine and attempt to load
        all_extensions = default_extensions + user_extensions

        # Try to import each extension to check if it can be loaded
        for ext in all_extensions:
            try:
                module_name, _, class_name = ext.rpartition('.')
                if not module_name or not class_name:
                    raise ImportError(f"Invalid extension format: '{ext}'")
                module = __import__(module_name, fromlist=[class_name])
                getattr(module, class_name)
            except Exception as e:
                raise ImportError(
                    f"Failed to load Jinja2 extension '{ext}': {e}"
                ) from e

        # Store extensions for use by subclasses
        self.extensions = all_extensions

        # Call next parent in MRO
        super().__init__(**kwargs)

    def _read_extensions(self, context: dict[str, Any]) -> list[str]:
        '''Return list of extensions as str to be passed on to the Jinja2 env.
        If context does not contain the relevant info, return an empty
        list instead.
        '''
        exts = context.get('_extensions')
        if isinstance(exts, list):
            return [str(e) for e in exts if isinstance(e, str)]
        return []
