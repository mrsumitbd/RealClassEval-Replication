class FilteredValueIndicator:
    def __init__(self, value, filtered: bool = False):
        self.value = value
        self.filtered = filtered

    def __str__(self) -> str:
        """Return the string representation of the value if not filtered,
        otherwise return a placeholder indicating the value is filtered."""
        return str(self.value) if not self.filtered else "Filtered"

    def __repr__(self) -> str:
        """Return an unambiguous representation of the object."""
        return f"{self.__class__.__name__}(value={self.value!r}, filtered={self.filtered})"
