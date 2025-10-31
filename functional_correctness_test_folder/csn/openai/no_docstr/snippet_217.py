class FilteredValueIndicator:
    def __init__(self, value, filtered: bool = False):
        self.value = value
        self.filtered = filtered

    def __str__(self) -> str:
        return str(self.value) if not self.filtered else "Filtered"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value!r}, filtered={self.filtered!r})"
