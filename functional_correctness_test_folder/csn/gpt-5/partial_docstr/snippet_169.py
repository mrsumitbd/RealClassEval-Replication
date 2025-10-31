class Cursor:

    def __init__(self):
        self._items = []

    def count(self):
        '''Return the number of items in this cursor.'''
        return len(self._items)

    def __iter__(self):
        return iter(self._items)
