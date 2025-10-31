class immutableattr:
    """An immutable attribute of a class.

    Parameters
    ----------
    attr : any
        The attribute.
    """

    def __init__(self, attr):
        self._attr = attr

    def __get__(self, instance, owner):
        return self._attr