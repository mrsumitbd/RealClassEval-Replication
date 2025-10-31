
class FilteredValueIndicator:
    '''Represent a filtered value.'''

    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        '''Filter str.'''
        return f"FilteredValueIndicator(value={self.value})"

    def __repr__(self) -> str:
        '''Filter repr.'''
        return f"FilteredValueIndicator(value={self.value!r})"
