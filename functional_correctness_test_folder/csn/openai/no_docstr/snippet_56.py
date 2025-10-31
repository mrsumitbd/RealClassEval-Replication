
class Collection:
    def __init__(self, iterable=None):
        self._items = list(iterable) if iterable is not None else []

    def __len__(self) -> int:
        return len(self._items)

    def __delitem__(self, item):
        try:
            self._items.remove(item)
        except ValueError:
            raise KeyError(item)

    def __contains__(self, item) -> bool:
        return item in self._items
