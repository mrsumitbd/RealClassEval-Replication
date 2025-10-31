from collections import deque as _deque

class deque(_deque):

    def copy(self):
        if hasattr(_deque, 'copy'):
            return _deque.copy(self)
        else:
            return deque((x for x in self))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [x for x in self][key]
        else:
            return _deque.__getitem__(self, key)

    def reversed(self):
        tmp = self.copy()
        tmp.reverse()
        return tmp