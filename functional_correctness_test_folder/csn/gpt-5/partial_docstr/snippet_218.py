class RepeatValueIndicator:

    __slots__ = ("key",)

    def __init__(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if not key:
            raise ValueError("key must be non-empty")
        self.key = key

    def __repr__(self) -> str:
        '''Return representation.'''
        return f"{self.__class__.__name__}({self.key!r})"
