class Image:
    """A class representing an image embedded in an audio file."""

    def __init__(self, name: str, data: bytes, mime_type: str | None=None) -> None:
        self.name = name
        self.data = data
        self.mime_type = mime_type
        self.description: str | None = None

    def __repr__(self) -> str:
        variables = vars(self).copy()
        data = variables.get('data')
        if data is not None:
            variables['data'] = data[:45] + b'..' if len(data) > 45 else data
        data_str = ', '.join((f'{k}={v!r}' for k, v in variables.items()))
        return f'{type(self).__name__}({data_str})'