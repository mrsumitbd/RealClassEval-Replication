
class NullFunc:

    def __call__(self, *args):

        return None

    def distance(self, other):

        if isinstance(other, NullFunc):
            return 0
        else:
            return float('inf')
