class RepeatValueIndicator:

    def __init__(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a str")
        self.key = key

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.key!r})"
