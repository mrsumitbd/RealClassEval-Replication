
class FilteredValueIndicator:
    def __init__(self, value=None, filtered=False):
        self.value = value
        self.filtered = filtered

    def __str__(self) -> str:
        if self.filtered:
            return f"Filtered({self.value})"
        else:
            return str(self.value)

    def __repr__(self) -> str:
        return f"FilteredValueIndicator(value={self.value!r}, filtered={self.filtered!r})"
