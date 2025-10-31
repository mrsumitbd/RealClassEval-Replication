class RepeatValueIndicator:

    def __init__(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        self.key = key

    def __repr__(self) -> str:
        return f"RepeatValueIndicator(key={self.key!r})"
