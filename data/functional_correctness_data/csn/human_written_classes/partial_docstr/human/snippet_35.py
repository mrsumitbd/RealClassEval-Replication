class Default:
    """
    It is used to replace `None` or `object()` as a sentinel
    that represents a default value. Sometimes we want to set
    a value to `None` so we cannot use `None` to represent the
    default value, and `object()` is hard to be typed.
    """

    def __repr__(self):
        return '<Default>'

    def __str__(self) -> str:
        return self.__repr__()