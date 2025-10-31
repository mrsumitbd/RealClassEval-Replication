class Cursor:
    def __init__(self, items=None):
        """Create a new cursor optionally initialized with an iterable of items."""
        self._items = list(items) if items is not None else []

    def count(self):
        """Return the number of items in this cursor."""
        return len(self._items)

    def __iter__(self):
        """Return an iterator over the cursor's items."""
        return iter(self._items)
