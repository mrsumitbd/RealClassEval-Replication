
class RepeatValueIndicator:

    def __init__(self, key: str) -> None:
        self.key = key
        self.last_value = None
        self.repeat_count = 0

    def __repr__(self) -> str:
        return f"RepeatValueIndicator(key='{self.key}', last_value={self.last_value}, repeat_count={self.repeat_count})"
