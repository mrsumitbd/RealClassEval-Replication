class NullFunc:
    def __call__(self, *args, **kwargs):
        return None

    def distance(self, other):
        return 0 if isinstance(other, NullFunc) else 1
