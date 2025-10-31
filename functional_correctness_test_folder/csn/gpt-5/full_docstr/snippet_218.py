class RepeatValueIndicator:
    '''Represent a repeating value.'''

    def __init__(self, key: str) -> None:
        '''Init with key.'''
        if not isinstance(key, str):
            raise TypeError("key must be a str")
        if not key:
            raise ValueError("key cannot be empty")
        self.key = key

    def __repr__(self) -> str:
        '''Return representation.'''
        return f"RepeatValueIndicator({self.key!r})"
