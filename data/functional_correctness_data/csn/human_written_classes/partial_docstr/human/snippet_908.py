class PrintableErrorField:
    """
    A glorified tuple with a kwarg in its constructor.
    Coerces name and value fields to unicode for output consistency
    """
    TEXT_PREFIX = 'Globus CLI Error:'

    def __init__(self, name: str, value: str | int | None, multiline: bool=False) -> None:
        self.multiline = multiline
        self.name = str(name)
        self.raw_value = str(value)
        self.value = self._format_value(self.raw_value)

    @property
    def _text_prefix_len(self) -> int:
        return len(self.TEXT_PREFIX)

    def _format_value(self, val: str) -> str:
        """
        formats a value to be good for textmode printing
        val must be unicode
        """
        name = self.name + ':'
        if not self.multiline or '\n' not in val:
            val = f'{name.ljust(self._text_prefix_len)} {val}'
        else:
            spacer = '\n' + ' ' * (self._text_prefix_len + 1)
            val = '{}{}{}'.format(name, spacer, spacer.join(val.split('\n')))
        return val