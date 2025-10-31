class FilteredValueIndicator:
    '''Represent a filtered value.'''

    def __init__(self, value, filtered: bool = False):
        self.value = value
        self.filtered = filtered

    def __str__(self) -> str:
        '''Filter str.'''
        return str(self.value)

    def __repr__(self) -> str:
        '''Filter repr.'''
        return f"{self.__class__.__name__}(value={self.value!r}, filtered={self.filtered!r})"
