
class ExtensionLoaderMixin:

    def __init__(self, *, context: dict[str, Any] | None = None, **kwargs: Any) -> None:
        self.context = context if context is not None else {}
        self.kwargs = kwargs

    def _read_extensions(self, context: dict[str, Any]) -> list[str]:
        extensions = []
        for key, value in context.items():
            if key.startswith('extension_'):
                extensions.append(value)
        return extensions
