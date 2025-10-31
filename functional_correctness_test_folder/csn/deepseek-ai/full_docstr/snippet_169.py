
class Cursor:
    '''Interface that abstracts the cursor object returned from databases.'''

    def __init__(self):
        '''Declare a new cursor to iterate over runs.'''
        self._items = []

    def count(self):
        '''Return the number of items in this cursor.'''
        return len(self._items)

    def __iter__(self):
        '''Iterate over elements.'''
        return iter(self._items)
