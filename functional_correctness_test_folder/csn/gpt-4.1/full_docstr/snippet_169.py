
class Cursor:
    '''Interface that abstracts the cursor object returned from databases.'''

    def __init__(self, items=None):
        '''Declare a new cursor to iterate over runs.'''
        if items is None:
            self._items = []
        else:
            self._items = list(items)

    def count(self):
        '''Return the number of items in this cursor.'''
        return len(self._items)

    def __iter__(self):
        '''Iterate over elements.'''
        return iter(self._items)
