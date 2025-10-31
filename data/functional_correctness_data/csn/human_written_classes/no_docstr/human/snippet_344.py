from collections.abc import Hashable

class memoized:

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        if not isinstance(args, Hashable):
            return self.func(*args, **kwargs)
        if args in self.cache:
            return self.cache[args]
        value = self.func(*args, **kwargs)
        if value is not None:
            self.cache[args] = value
        return value