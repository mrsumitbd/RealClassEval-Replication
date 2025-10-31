
class Collection:
    def __init__(self):
        self._items = []

    def __len__(self) -> int:
        return len(self._items)

    def __delitem__(self, item):
        if item in self._items:
            self._items.remove(item)

    def __contains__(self, item) -> bool:
        return item in self._items
