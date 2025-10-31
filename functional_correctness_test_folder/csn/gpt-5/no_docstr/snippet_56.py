class Collection:
    def __init__(self, iterable=None):
        self._items = list(iterable) if iterable is not None else []

    def __len__(self) -> int:
        return len(self._items)

    def __delitem__(self, item):
        if isinstance(item, (int, slice)):
            del self._items[item]
        else:
            raise TypeError("Indices must be integers or slices")

    def __contains__(self, item) -> bool:
        return item in self._items
