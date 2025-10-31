
class Cursor:

    def __init__(self):
        self.items = []

    def count(self):
        '''Return the number of items in this cursor.'''
        return len(self.items)

    def __iter__(self):
        return iter(self.items)
