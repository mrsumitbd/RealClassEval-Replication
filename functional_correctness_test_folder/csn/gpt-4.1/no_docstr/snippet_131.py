
class NullFunc:

    def __call__(self, *args):
        return None

    def distance(self, other):
        return 0 if isinstance(other, NullFunc) else float('inf')
