class Memoized:
    """
    A kwargs-aware memoizer, better than the one in python :).

    Don't pass in too large kwargs, since this turns them into a tuple of
    tuples. Also, avoid mutable types (as usual for memoizers)

    What this does is to create a dictionary of {(*parameters):return value},
    and uses it as a cache for subsequent calls to the same method.
    It is especially useful for functions that don't rely on external variables
    and that are called often. It's a perfect match for our getSize etc...
    """

    def __init__(self, func) -> None:
        self.cache: dict = {}
        self.func = func
        self.__doc__ = self.func.__doc__
        self.__name__ = self.func.__name__

    def __call__(self, *args, **kwargs):
        args_plus = tuple(kwargs.items())
        key = (args, args_plus)
        try:
            if key not in self.cache:
                res = self.func(*args, **kwargs)
                self.cache[key] = res
            return self.cache[key]
        except TypeError:
            return self.func(*args, **kwargs)