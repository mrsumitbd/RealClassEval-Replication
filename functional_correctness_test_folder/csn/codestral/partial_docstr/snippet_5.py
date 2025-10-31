
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
        self.extensions = self._read_extensions(context) if context else []
        self.extensions.extend(self.default_extensions)
        super().__init__(extensions=self.extensions, **kwargs)

    def _read_extensions(self, context: dict[str, Any]) -> list[str]:
        '''Return list of extensions as str to be passed on to the Jinja2 env.
        If context does not contain the relevant info, return an empty
        list instead.
        '''
        return context.get('_extensions', [])
