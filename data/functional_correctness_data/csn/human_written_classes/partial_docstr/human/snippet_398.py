class OutputMode:
    """(sway only) A mode for an output

    :ivar width: The width of the output in this mode.
    :vartype width: int
    :ivar height: The height of the output in this mode.
    :vartype height: int
    :vartype refresh: The refresh rate of the output in this mode.
    :vartype refresh: int
    """

    def __init__(self, data):
        self.width = data['width']
        self.height = data['height']
        self.refresh = data['refresh']

    def __getitem__(self, item):
        if not hasattr(self, item):
            raise KeyError(item)
        return getattr(self, item)

    @classmethod
    def _parse_list(cls, data):
        return [cls(d) for d in data]