class islice_extended:
    """An extension of :func:`itertools.islice` that supports negative values
    for *stop*, *start*, and *step*.

        >>> iterator = iter('abcdefgh')
        >>> list(islice_extended(iterator, -4, -1))
        ['e', 'f', 'g']

    Slices with negative values require some caching of *iterable*, but this
    function takes care to minimize the amount of memory required.

    For example, you can use a negative step with an infinite iterator:

        >>> from itertools import count
        >>> list(islice_extended(count(), 110, 99, -2))
        [110, 108, 106, 104, 102, 100]

    You can also use slice notation directly:

        >>> iterator = map(str, count())
        >>> it = islice_extended(iterator)[10:20:2]
        >>> list(it)
        ['10', '12', '14', '16', '18']

    """

    def __init__(self, iterable, *args):
        it = iter(iterable)
        if args:
            self._iterator = _islice_helper(it, slice(*args))
        else:
            self._iterator = it

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iterator)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return islice_extended(_islice_helper(self._iterator, key))
        raise TypeError('islice_extended.__getitem__ argument must be a slice')