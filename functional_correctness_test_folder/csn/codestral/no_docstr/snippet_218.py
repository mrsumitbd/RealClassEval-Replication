
class RepeatValueIndicator:

    def __init__(self, key: str) -> None:
        self.key = key
        self.count = 0

    def __repr__(self) -> str:
        return f"RepeatValueIndicator(key='{self.key}', count={self.count})"
