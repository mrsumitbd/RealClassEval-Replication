
class Collection:

    def __init__(self):
        self.items = []

    def __len__(self) -> int:
        return len(self.items)

    def __delitem__(self, item):
        if item in self.items:
            self.items.remove(item)

    def __contains__(self, item) -> bool:
        return item in self.items
