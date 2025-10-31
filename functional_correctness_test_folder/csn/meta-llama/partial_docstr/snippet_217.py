
class FilteredValueIndicator:

    def __init__(self, value, filter_name):
        """
        Initialize the FilteredValueIndicator.

        Args:
        value (any): The value to be represented.
        filter_name (str): The name of the filter applied to the value.
        """
        self.value = value
        self.filter_name = filter_name

    def __str__(self) -> str:
        '''Filter str.'''
        return f"{self.filter_name}: {self.value}"

    def __repr__(self) -> str:
        return f"FilteredValueIndicator(value={repr(self.value)}, filter_name='{self.filter_name}')"
