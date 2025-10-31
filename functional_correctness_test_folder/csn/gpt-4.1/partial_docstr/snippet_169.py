
class Cursor:

    def __init__(self):
        self._items = []
        self._index = 0

    def count(self):
        '''Return the number of items in this cursor.'''
        return len(self._items)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._items):
            item = self._items[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration
