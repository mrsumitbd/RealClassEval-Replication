
class Cursor:

    def __init__(self, data=None):
        self.data = data if data is not None else []
        self.index = 0

    def count(self):
        return len(self.data)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < self.count():
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
