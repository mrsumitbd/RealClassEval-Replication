
class RepeatValueIndicator:

    def __init__(self, key: str) -> None:
        self.key = key
        self.prev_value = None
        self.repeat_count = 0

    def __repr__(self) -> str:
        '''Return representation.'''
        return f'RepeatValueIndicator(key={self.key}, prev_value={self.prev_value}, repeat_count={self.repeat_count})'
