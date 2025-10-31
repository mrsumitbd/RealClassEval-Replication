
class Cursor:

    def __init__(self, items=None):
        self.items = items if items is not None else []
        self.index = 0

    def count(self):
        '''Return the number of items in this cursor.'''
        return len(self.items)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < self.count():
            result = self.items[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
