
class NullFunc:

    def __call__(self, *args):
        return None

    def distance(self, other):
        return float('inf')
