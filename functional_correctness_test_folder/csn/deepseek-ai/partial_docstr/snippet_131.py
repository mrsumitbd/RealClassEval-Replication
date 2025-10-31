
class NullFunc:

    def __call__(self, *args):
        pass

    def distance(self, other):
        if isinstance(other, NullFunc):
            return 0.0
        else:
            return 1e12
