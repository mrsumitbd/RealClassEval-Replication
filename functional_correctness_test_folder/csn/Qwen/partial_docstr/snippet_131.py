
class NullFunc:

    def __call__(self, *args):
        pass

    def distance(self, other):
        return 0.0 if isinstance(other, NullFunc) else float('inf')
