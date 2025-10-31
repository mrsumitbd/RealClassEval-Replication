
class Collection:
    def __init__(self):
        self._items = []

    def __len__(self) -> int:
        return len(self._items)

    def __delitem__(self, item):
        if isinstance(item, int):
            del self._items[item]
        else:
            self._items.remove(item)

    def __contains__(self, item) -> bool:
        return item in self._items
