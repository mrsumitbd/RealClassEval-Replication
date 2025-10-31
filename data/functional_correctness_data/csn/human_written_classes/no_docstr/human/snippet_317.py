from itertools import starmap

class SingleProcessPool:

    def map(self, func, iterable):
        return list(map(func, iterable))

    def starmap(self, func, iterable):
        return list(starmap(func, iterable))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass