class Cursor:
    '''Interface that abstracts the cursor object returned from databases.'''

    def __init__(self, iterable=None):
        '''Declare a new cursor to iterate over runs.'''
        if iterable is None:
            self._items = []
        else:
            try:
                self._items = list(iterable)
            except TypeError:
                self._items = [iterable]

    def count(self):
        '''Return the number of items in this cursor.'''
        return len(self._items)

    def __iter__(self):
        '''Iterate over elements.'''
        return iter(self._items)
