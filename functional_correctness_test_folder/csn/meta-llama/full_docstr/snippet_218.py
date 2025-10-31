
class RepeatValueIndicator:
    '''Represent a repeating value.'''

    def __init__(self, key: str) -> None:
        '''Init with key.'''
        self._key = key

    def __repr__(self) -> str:
        '''Return representation.'''
        return f'RepeatValueIndicator({self._key!r})'
