
class FilteredValueIndicator:
    '''Represent a filtered value.'''

    def __init__(self, value, filter_name):
        """
        Initialize a FilteredValueIndicator instance.

        Args:
            value: The original value.
            filter_name (str): The name of the filter applied to the value.
        """
        self.value = value
        self.filter_name = filter_name

    def __str__(self) -> str:
        '''Filter str.'''
        return f"{self.value} (filtered by {self.filter_name})"

    def __repr__(self) -> str:
        '''Filter repr.'''
        return f"FilteredValueIndicator({repr(self.value)}, '{self.filter_name}')"
