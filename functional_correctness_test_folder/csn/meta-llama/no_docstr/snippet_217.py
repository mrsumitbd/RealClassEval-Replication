
class FilteredValueIndicator:

    def __init__(self, value, filter_status):
        """
        Initialize the FilteredValueIndicator object.

        Args:
        value (any): The value to be stored.
        filter_status (bool): The filter status of the value.
        """
        self.value = value
        self.filter_status = filter_status

    def __str__(self) -> str:
        """Return a string representation of the FilteredValueIndicator object."""
        status = "Filtered" if self.filter_status else "Not Filtered"
        return f"Value: {self.value}, Status: {status}"

    def __repr__(self) -> str:
        """Return a representation of the FilteredValueIndicator object that could be used to recreate it."""
        return f"FilteredValueIndicator({self.value}, {self.filter_status})"


# Example usage:
def main():
    indicator = FilteredValueIndicator(10, True)
    print(str(indicator))  # Output: Value: 10, Status: Filtered
    print(repr(indicator))  # Output: FilteredValueIndicator(10, True)


if __name__ == "__main__":
    main()
