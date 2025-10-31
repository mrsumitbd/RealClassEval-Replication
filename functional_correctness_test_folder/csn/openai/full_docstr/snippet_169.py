
class Cursor:
    '''Interface that abstracts the cursor object returned from databases.'''

    def __init__(self, data=None):
        '''Declare a new cursor to iterate over runs.'''
        self._data = list(data) if data is not None else []

    def count(self):
        '''Return the number of items in this cursor.'''
        return len(self._data)

    def __iter__(self):
        '''Iterate over elements.'''
        return iter(self._data)
