import collections
import operator
import bisect

class SorteDeque(collections.deque):
    """A deque subclass that tries to maintain sorted ordering using bisect"""

    def insort(self, item):
        i = bisect.bisect_left(self, item)
        self.rotate(-i)
        self.appendleft(item)
        self.rotate(i)

    def resort(self, item):
        if item in self:
            i = bisect.bisect_left(self, item)
            if i == len(self) or self[i] is not item:
                self.remove(item)
                self.insort(item)
        else:
            self.insort(item)

    def check(self):
        """re-sort any items in self that are not sorted"""
        for unsorted in iter((self[i] for i in range(len(self) - 2) if not operator.le(self[i], self[i + 1]))):
            self.resort(unsorted)