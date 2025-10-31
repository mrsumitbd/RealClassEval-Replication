
class NullFunc:

    def __call__(self, *args):
        return self

    def distance(self, other):
        return float('inf')
