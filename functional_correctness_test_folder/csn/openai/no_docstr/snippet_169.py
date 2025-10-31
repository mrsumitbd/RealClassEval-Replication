class Cursor:
    def __init__(self):
        self._items = []

    def count(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    # Optional helper to add items to the cursor
    def add(self, item):
        self._items.append(item)
