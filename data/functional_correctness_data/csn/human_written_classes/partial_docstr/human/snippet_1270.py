class _AVWXProp:
    """
    Represents a property of AVWX result (simple descriptor)
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, _):
        if obj is None:
            return self
        return obj.data[self.func.__name__]