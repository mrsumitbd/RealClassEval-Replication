
class RepeatValueIndicator:

    def __init__(self, key: str) -> None:
        self.key = key

    def __repr__(self) -> str:
        return f"RepeatValueIndicator(key={self.key!r})"
